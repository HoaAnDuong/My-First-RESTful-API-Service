import sqlite3
import flask
from flask import Flask

connection = sqlite3.connect("database.db",check_same_thread=False) #if check_same_thread = True, sqlite3 won't work
cursor = connection.cursor()
app = Flask(__name__)

table_list = [item[0] for item in cursor.execute("select name from sqlite_schema where type = 'table';").fetchall()]
print(table_list)

forbidden_letter = []
for i in range(0,128):
    if i < 48 or (i > 57 and i <65) or (i > 90 and i < 97) or i > 122:
        forbidden_letter.append(chr(i))

print(forbidden_letter)
def id_check(id):
    try:
        for i in forbidden_letter:
            if i in id:
                return False
        return True
    except:
        return False

def get_json(table_name,has_status=False):
    json = {}
    column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
    query = "select "
    for i in range(0,len(column_list)-has_status):
        if i!=0:
            query += ", "
        query += column_list[i]
    query += f" from {table_name}"
    if has_status:
        query += " where Status = 'available'"
    data = cursor.execute(query).fetchall()
    if data == []:
        return {}
    else:
        json[table_name.lower()] = [dict(zip(column_list, row)) for row in data]
        return json
def get_json_via_id(table_name,id,has_status=False,table_name_singular = None):
    try:
        if id_check(id) == False:
            raise Exception()
        json = {}
        column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
        query = "select "
        for i in range(0, len(column_list) - has_status):
            if i != 0:
                query += ", "
            query += column_list[i]
        query += f" from {table_name} where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
        if has_status:
            query += " and Status = 'available'"
        data = cursor.execute(query).fetchall()
        if data == []:
            raise Exception("ID not found")
        else:
            data = data[0]
            json = dict(zip(column_list,data))
            return json
    except Exception as e:
        return {}


def post_json(table_name,json,has_status = False):
    column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
    cursor.execute("begin transaction")
    try:
        query = f"insert into {table_name} values("
        for i in range(0, len(column_list) - has_status):
            if i != 0:
                query += ", "
            query += f"'{json[column_list[i]]}'"
        if has_status:
            query += ", 'available'"
        query+=")"
        cursor.execute(query)
        cursor.execute("commit")
        return {"message": "Success", "posted": json}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
def delete_json(table_name,id,has_status=False,table_name_singular = None):
    cursor.execute("begin transaction")
    if id_check(id) == False:
        cursor.execute("rollback")
        return {"message": "Failed","exception":"Illegal ID"}
    json = get_json_via_id(table_name, id, has_status,table_name_singular)
    if json == {}:
        cursor.execute("rollback")
        return {"message": "Failed","exception":"ID not found"}
    if has_status:
        try:
            query = f"update {table_name} set Status = 'unavailable' where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
            cursor.execute(query)
            cursor.execute("commit")
            return {"message":"Success","deleted":json}
        except Exception as e:
            cursor.execute("commit")
            return {"message":"Failed","exception":f"{type(e)}:{e}"}
    else:
        try:
            query = f"delete from {table_name} where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
            cursor.execute(query)
            cursor.execute("commit")
            return {"message":"Success","deleted":json}
        except Exception as e:
            cursor.execute("rollback")
            return {"message":"Failed","exception":f"{type(e)}:{e}"}

def put_json(table_name,id,json,has_status=False,table_name_singular = None):
    cursor.execute("begin transaction")
    if id_check(id) == False:
        cursor.execute("rollback")
        return {"message": "Failed", "exception": "Illegal ID"}
    check_json = get_json_via_id(table_name,id,has_status,table_name_singular)
    if check_json == {}:
        cursor.execute("rollback")
        return {"message": "Failed","exception":"ID not found"}
    else:
        column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
        try:
            for i in range(1,len(column_list)-has_status):
                try:
                    query = f"update {table_name} set {column_list[i]} = '{json[column_list[i]]}' where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
                    cursor.execute(query)
                    print(query)
                except Exception as e:
                    print(type(e),e)
                    pass
            cursor.execute("commit")
            return {"message":"Success","put":get_json_via_id(table_name,id,has_status,table_name_singular)}
        except Exception as e:
            cursor.execute("rollback")
            return {"message":"Failed","exception":f"{type(e)}:{e}"}

def get_json_via_query(column_list,query,table_name=None):
    try:
        json = {}
        data = cursor.execute(query).fetchall()
        if len(data) <= 1:
            json = dict(zip(column_list,data[0]))
        else:
            json[table_name.lower()] = [dict(zip(column_list,row)) for row in data]
        return json
    except Exception as e:
        return {}

def get_table_list(table_name,has_status=False):
    json = {}
    column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
    query = "select "
    for i in range(0,len(column_list)-has_status):
        if i!=0:
            query += ", "
        query += column_list[i]
    query += f" from {table_name}"
    if has_status:
        query += " where Status = 'available'"
    data = cursor.execute(query).fetchall()
    data.insert(0,column_list)
    return data

#Routes

@app.route("/")
def home():
    return flask.render_template("Home.html")
@app.route("/introduction")
def introduction_page():
    return flask.render_template("Introduction.html")
@app.route("/sending-requests")
def sending_requests_page():
    return flask.render_template("Sending-Requests.html")
@app.route("/database")
def database_page():
    customers_table = cursor.execute("select * from Customers limit 5").fetchall()
    employees_table = cursor.execute("select * from Employees limit 5").fetchall()
    shippers_table = cursor.execute("select * from Shippers limit 5").fetchall()
    suppliers_table = cursor.execute("select * from Suppliers limit 5").fetchall()
    categories_table = cursor.execute("select * from Categories limit 5").fetchall()
    products_table = cursor.execute("select * from Products limit 5").fetchall()
    orders_table = cursor.execute("select * from Orders limit 5").fetchall()
    orderdates_table = cursor.execute("select * from OrderDates limit 5").fetchall()
    orderpayments_table = cursor.execute("select * from OrderPayments limit 5").fetchall()
    orderdetails_table = cursor.execute("select * from OrderDetails limit 5").fetchall()
    return flask.render_template("Database.html",
                                 customers_table = customers_table,
                                 employees_table = employees_table,
                                 shippers_table = shippers_table,
                                 suppliers_table = suppliers_table,
                                 categories_table = categories_table,
                                 products_table = products_table,
                                 orders_table = orders_table,
                                 orderdates_table = orderdates_table,
                                 orderpayments_table = orderpayments_table,
                                 orderdetails_table = orderdetails_table)
#API Routes
@app.route("/shippers",methods = ["GET"])
def get_shippers():
    return flask.jsonify(get_json("Shippers",True))

@app.route("/shippers",methods=["POST"])
def post_shippers():
    return flask.jsonify(post_json("Shippers",flask.request.json,True))
@app.route("/shippers/<id>")
def get_shippers_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_id("Shippers",id,True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/shippers/<id>",methods = ["DELETE"])
def delete_shipper(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return(flask.jsonify(delete_json("Shippers",id,True)))

@app.route("/shippers/<id>",methods = ["PUT"])
def put_shipper(id):
    if id_check(id) == False:
        return {"message": "Failed", "exception": "Illegal ID"}
    return flask.jsonify(put_json("Shippers", id, flask.request.json, True))


@app.route("/customers",methods = ["GET"])
def get_customers():
    return flask.jsonify(get_json("Customers", True))

@app.route("/customers", methods=["POST"])
def post_customers():
    return flask.jsonify(post_json("Customers", flask.request.json, True))

@app.route("/customers/<id>")
def get_customers_via_id(id):
    json = get_json_via_id("Customers", id, True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/customers/<id>", methods=["DELETE"])
def delete_customer(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return (flask.jsonify(delete_json("Customers", id, True)))

@app.route("/customers/<id>", methods=["PUT"])
def put_customer(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return flask.jsonify(put_json("Customers", id, flask.request.json, True))

@app.route("/suppliers",methods = ["GET"])
def get_suppliers():
    return flask.jsonify(get_json("Suppliers", True))

@app.route("/suppliers", methods=["POST"])
def post_suppliers():
    return flask.jsonify(post_json("Suppliers", flask.request.json, True))

@app.route("/suppliers/<id>",methods = ["GET"])
def get_suppliers_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_id("Suppliers", id, True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/suppliers/<id>", methods=["DELETE"])
def delete_supplier(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return (flask.jsonify(delete_json("Suppliers", id, True)))

@app.route("/suppliers/<id>", methods=["PUT"])
def put_supplier(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return flask.jsonify(put_json("Suppliers", id, flask.request.json, True))

@app.route("/employees",methods = ["GET"])
def get_employees():
    return flask.jsonify(get_json("Employees", True))

@app.route("/employees", methods=["POST"])
def post_employees():
    return flask.jsonify(post_json("Employees", flask.request.json, True))

@app.route("/employees/<id>",methods = ["GET"])
def get_employees_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_id("Employees", id, True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/employees/<id>", methods=["DELETE"])
def delete_employee(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return (flask.jsonify(delete_json("Employees", id, True)))

@app.route("/employees/<id>", methods=["PUT"])
def put_employee(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return flask.jsonify(put_json("Employees", id, flask.request.json, True))

@app.route("/categories",methods = ["GET"])
def get_categories():
    return flask.jsonify(get_json("Categories", False))

@app.route("/categories", methods=["POST"])
def post_categories():
    return flask.jsonify(post_json("Categories", flask.request.json, False))

@app.route("/categories/<id>",methods = ["GET"])
def get_categories_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_id("Categories", id, False,"Category")
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/categories/<id>", methods=["DELETE"])
def delete_categories(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return (flask.jsonify(delete_json("Categories", id, False,"Category")))

@app.route("/categories/<id>", methods=["PUT"])
def put_categories(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return flask.jsonify(put_json("Categories", id, flask.request.json, False,"Category"))

@app.route("/products",methods = ["GET"])
def get_products():
    json = get_json_via_query(['ProductID', 'ProductName', 'SupplierID','SupplierName', 'CategoryID','CategoryName', 'Unit', 'Price','Total'],"select ProductID, ProductName, Products.SupplierID, SupplierName, Products.CategoryID, CategoryName, Unit, Price,(Unit*Price) from Products inner join Suppliers on Products.SupplierID = Suppliers.SupplierID inner join Categories on Products.CategoryID = Categories.CategoryID","Products")
    json["total"] = cursor.execute("select sum(unit*price) from Products").fetchall()[0][0]
    return flask.jsonify(json)

@app.route("/products", methods=["POST"])
def post_products():
    cursor.execute("begin transaction")
    json = flask.request.json
    try:
        cursor.execute("insert into Products values('{}','{}','{}','{}',{},{})".format(json["ProductID"],json["ProductName"],json["SupplierID"],json["CategoryID"],json["Unit"],json["Price"]))
        cursor.execute("commit")
        return {"message": "Success", "posted": json}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}


@app.route("/products/<id>",methods = ["GET"])
def get_products_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_query(['ProductID', 'ProductName', 'SupplierID','SupplierName', 'CategoryID','CategoryName', 'Unit', 'Price','Total'],f"select ProductID, ProductName, Products.SupplierID, SupplierName, Products.CategoryID, CategoryName, Unit, Price,(Unit*Price) from Products inner join Suppliers on Products.SupplierID = Suppliers.SupplierID inner join Categories on Products.CategoryID = Categories.CategoryID where ProductID = '{id}'")
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/products/<id>", methods=["DELETE"])
def delete_products(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    return (flask.jsonify(delete_json("Products", id, False)))

@app.route("/products/<id>", methods=["PUT"])
def put_products(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    cursor.execute("begin transaction")
    json = flask.request.json
    check_json = get_json_via_id("Products",id,False)
    if check_json != {}:
        try:
            try:
                cursor.execute("update Products set ProductName = '{}' where ProductID = '{}' ".format(json["ProductName"],id))
            except:
                pass
            try:
                cursor.execute("update Products set SupplierID = '{}' where ProductID = '{}' ".format(json["SupplierID"],id))
            except:
                pass
            try:
                cursor.execute("update Products set CategoryID = '{}' where ProductID = '{}' ".format(json["CategoryID"],id))
            except:
                pass
            try:
                cursor.execute("update Products set Unit = {} where ProductID = '{}' ".format(json["Unit"], id))
            except:
                pass
            try:
                cursor.execute("update Products set Price = {} where ProductID = '{}' ".format(json["Price"], id))
            except:
                pass
            cursor.execute("commit")
            return {"message": "Success", "put": get_json_via_id("Products", id, False)}
        except Exception as e:
            cursor.execute("rollback")
            return {"message":"Failed","exception":f"{type(e)}:{e}"}
    else:
        cursor.execute("rollback")
        return {"message": "Failed","exception":"ID not found"}

@app.route("/orders",methods = ["GET"])
def get_orders():
    json = get_json_via_query(['OrderID', 'Orders.CustomerID', 'CustomerName', 'EmployeeID', 'EmployeeName', 'ShipperID', 'ShipperName', 'Date', 'PaymentMethod', 'Status', 'Total'],"select * from OrderViews","Orders")
    json["total"] = cursor.execute("select sum(total) from OrderPayments").fetchall()[0][0]
    for item in json['orders']:
        item["Estimated"] = cursor.execute("select sum(Quantity*Price) from OrderDetails inner join Products on OrderID = '{}' and OrderDetails.ProductID = Products.ProductID".format(item["OrderID"])).fetchall()[0][0]
        if item["Estimated"] == None:
            item["Estimated"] = 0.0
    return flask.jsonify(json)
@app.route("/orders",methods = ["POST"])
def post_orders():
    cursor.execute("begin transaction")
    try:
        json = flask.request.json
        cursor.execute("insert into Orders values ('{}','{}','{}','{}')".format(json["OrderID"],json["CustomerID"],json["EmployeeID"],json["ShipperID"]))
        try:
            cursor.execute("update OrderPayments set PaymentMethod = '{}' where OrderID = '{}'".format(json["PaymentMethod"],json["OrderID"]))
        except:
            pass
        cursor.execute("commit")
        return {"message": "Success", "posted": get_json_via_query(['OrderID', 'Orders.CustomerID', 'CustomerName', 'EmployeeID', 'EmployeeName', 'ShipperID', 'ShipperName', 'Date', 'PaymentMethod', 'Status', 'Total'],"select Orders.OrderID, Orders.CustomerID, CustomerName, Orders.EmployeeID, printf('%s %s',LastName,FirstName), Orders.ShipperID, ShipperName, Date, PaymentMethod, OrderPayments.Status, Total from Orders inner join Customers on Orders.CustomerID = Customers.CustomerID inner join Employees on Orders.EmployeeID = Employees.EmployeeID inner join Shippers on Orders.ShipperID = Shippers.ShipperID inner join OrderDates on Orders.OrderID = OrderDates.OrderID inner join OrderPayments on Orders.OrderID = OrderPayments.OrderID where Orders.OrderID = '{}'".format(json["OrderID"]))}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
@app.route("/orders/<id>",methods = ["GET"])
def get_orders_via_id(id):
    if id_check(id) == False:
        flask.abort(404)
    json = get_json_via_query(['OrderID', 'Orders.CustomerID', 'CustomerName', 'EmployeeID', 'EmployeeName', 'ShipperID', 'ShipperName', 'Date', 'PaymentMethod', 'Status', 'Total'],f"select * from OrderViews where OrderID = '{id}'")
    if json == {}:
        flask.abort(404)

    else:
        json["OrderDetails"] = [dict(zip(['ProductID', 'ProductName', 'Quantity', 'Price', 'Total'],row)) for row in cursor.execute("select OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID and OrderID = '{}'".format(id)).fetchall()]
        json["Estimated"] = cursor.execute("select sum(Quantity*Price) from OrderDetails inner join Products on OrderID = '{}' and OrderDetails.ProductID = Products.ProductID".format(id)).fetchall()[0][0]
        return flask.jsonify(json)
@app.route("/orders/<id>",methods=["POST"])
def post_order_details(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    cursor.execute("begin transaction")
    try:
        json = flask.request.json
        cursor.execute("insert into OrderDetails values('{}','{}',{})".format(id,json["ProductID"],json["Quantity"]))
        cursor.execute("commit")
        return {"message": "Success","posted":get_json_via_query(['ProductID', 'ProductName', 'Quantity', 'Price', 'Total'],"select OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID and Products.ProductID = '{}' where OrderID = '{}'".format(json["ProductID"],id))}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
@app.route("/orders/<id>",methods = ["PUT"])
def put_orders(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    cursor.execute("begin transaction")
    json = flask.request.json
    check_json = get_json_via_id("Orders", id, False)
    if check_json != {}:
        try:
            try:
                cursor.execute("update Orders set CustomerID = '{}' where OrderID = '{}' ".format(json["CustomerID"], id))
            except:
                pass
            try:
                cursor.execute("update Orders set EmployeeID = '{}' where OrderID = '{}' ".format(json["EmployeeID"], id))
            except:
                pass
            try:
                cursor.execute("update Orders set ShipperID = '{}' where OrderID = '{}' ".format(json["ShipperID"], id))
            except:
                pass
            try:
                cursor.execute("update OrderPayments set PaymentMethod = '{}' where OrderID = '{}' ".format(json["PaymentMethod"], id))
            except:
                pass
            try:
                cursor.execute("update OrderPayments set Status = '{}' where OrderID = '{}' ".format(json["Status"], id))
            except:
                pass
            cursor.execute("commit")
            return {"message": "Success", "put": get_json_via_query(['OrderID', 'Orders.CustomerID', 'CustomerName', 'EmployeeID', 'EmployeeName', 'ShipperID', 'ShipperName', 'Date', 'PaymentMethod', 'Status', 'Total'],f"select Orders.OrderID, Orders.CustomerID, CustomerName, Orders.EmployeeID, printf('%s %s',LastName,FirstName), Orders.ShipperID, ShipperName, Date, PaymentMethod, OrderPayments.Status, Total from Orders inner join Customers on Orders.CustomerID = Customers.CustomerID inner join Employees on Orders.EmployeeID = Employees.EmployeeID inner join Shippers on Orders.ShipperID = Shippers.ShipperID inner join OrderDates on Orders.OrderID = OrderDates.OrderID inner join OrderPayments on Orders.OrderID = OrderPayments.OrderID where Orders.OrderID = '{id}'")}
        except Exception as e:
            cursor.execute("rollback")
            return {"message":"Failed","exception":f"{type(e)}:{e}"}
    else:
        cursor.execute("rollback")
        return {"message": "Failed","exception":"ID not found"}
@app.route("/orders/<id>",methods = ["DELETE"])
def delete_orders(id):
    if id_check(id) == False:
        return {"message":"Failed","exception":"Illegal ID"}
    cursor.execute("begin transaction")
    try:
        check_json = get_json_via_id("Orders", id, False)
        if check_json == {}:
            cursor.execute("rollback")
            return {"message": "Failed","exception":"ID not found"}
        cursor.execute(f"update OrderPayments set Status = 'cancelled' where OrderID = '{id}'")
        cursor.execute("commit")
        return {"message":"Success","deleted": get_json_via_query(['OrderID', 'Orders.CustomerID', 'CustomerName', 'EmployeeID', 'EmployeeName', 'ShipperID', 'ShipperName', 'Date', 'PaymentMethod', 'Status', 'Total'],f"select Orders.OrderID, Orders.CustomerID, CustomerName, Orders.EmployeeID, printf('%s %s',LastName,FirstName), Orders.ShipperID, ShipperName, Date, PaymentMethod, OrderPayments.Status, Total from Orders inner join Customers on Orders.CustomerID = Customers.CustomerID inner join Employees on Orders.EmployeeID = Employees.EmployeeID inner join Shippers on Orders.ShipperID = Shippers.ShipperID inner join OrderDates on Orders.OrderID = OrderDates.OrderID inner join OrderPayments on Orders.OrderID = OrderPayments.OrderID where Orders.OrderID = '{id}'")}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}

@app.route("/orders/<orderid>/<productid>",methods = ["GET"])
def get_orderdetails_via_id(orderid,productid):
    if id_check(orderid) == False or id_check(productid) == False:
        flask.abort(404)
    try:
        json = cursor.execute(f"select OrderID, OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID where OrderID = '{orderid}' and OrderDetails.ProductID = '{productid}'").fetchall()
        if json == []:
            cursor.execute("rollback")
            return {"message": "Failed", "exception": "ID not found"}
        json = dict(zip(['OrderID','ProductID', 'ProductName', 'Quantity', 'Price', 'Total'],json[0]))
        return json
    except:
        flask.abort(404)
@app.route("/orders/<orderid>/<productid>",methods = ["DELETE"])
def delete_order_details(orderid,productid):
    if id_check(orderid) == False or id_check(productid) == False:
        return {"message":"Failed", "exception":"Illegal ID"}
    cursor.execute("begin transaction")
    try:
        json = cursor.execute(f"select OrderID, OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID where OrderID = '{orderid}' and OrderDetails.ProductID = '{productid}'").fetchall()
        if json == []:
            cursor.execute("rollback")
            return {"message": "Failed", "exception": "ID not found"}
        json = dict(zip(['OrderID', 'ProductID', 'ProductName', 'Quantity', 'Price', 'Total'], json[0]))
        cursor.execute(f"delete from OrderDetails where OrderID = '{orderid}' and ProductID = '{productid}'")
        cursor.execute("commit")
        return {"message": "Success", "deleted":json}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
@app.route("/orders/<orderid>/<productid>",methods = ["PUT"])
def put_order_details(orderid,productid):
    if id_check(orderid) == False or id_check(productid) == False:
        return {"message":"Failed", "exception":"Illegal ID"}
    cursor.execute("begin transaction")
    try:
        check_json = cursor.execute("select * from OrderDetails where OrderID = '{}' and ProductID = '{}'".format(orderid,productid)).fetchall()
        if check_json == []:
            cursor.execute("rollback")
            return {"message": "Failed", "exception": "ID not found"}
        json = flask.request.json
        try:
            cursor.execute("update OrderDetails set ProductID = '{}' where OrderID = '{}' and ProductID = '{}'".format(json["ProductID"],orderid,productid))
        except:
            pass
        try:
            cursor.execute("update OrderDetails set Quantity = {} where OrderID = '{}' and ProductID = '{}'".format(json["Quantity"], orderid, productid))
        except:
            pass
        return_json = None
        try:
            return_json = cursor.execute("select OrderID, OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID where OrderID = '{}' and OrderDetails.ProductID = '{}'".format(orderid,json["ProductID"])).fetchall()
        except:
            return_json = cursor.execute("select OrderID, OrderDetails.ProductID, ProductName, Quantity, Price, (Quantity*Price) from OrderDetails inner join Products on OrderDetails.ProductID = Products.ProductID where OrderID = '{}' and OrderDetails.ProductID = '{}'".format(orderid, productid)).fetchall()
        return_json = dict(zip(['OrderID', 'ProductID', 'ProductName', 'Quantity', 'Price', 'Total'], return_json[0]))
        cursor.execute("commit")
        return {"message": "Success","put":return_json}
    except Exception as e:
        cursor.execute("rollback")
        return {"message":"Failed","exception":f"{type(e)}:{e}"}


if __name__ == "__main__":
    app.run(debug=True)











