
import flask
from flask import Flask

from api_and_table import *

app = Flask(__name__)

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
    customers_table = connection.execute("select * from Customers limit 5").fetchall()
    employees_table = connection.execute("select * from Employees limit 5").fetchall()
    shippers_table = connection.execute("select * from Shippers limit 5").fetchall()
    suppliers_table = connection.execute("select * from Suppliers limit 5").fetchall()
    categories_table = connection.execute("select * from Categories limit 5").fetchall()
    products_table = connection.execute("select * from Products limit 5").fetchall()
    orders_table = connection.execute("select * from Orders limit 5").fetchall()
    orderdates_table = connection.execute("select * from OrderDates limit 5").fetchall()
    orderpayments_table = connection.execute("select * from OrderPayments limit 5").fetchall()
    orderdetails_table = connection.execute("select * from OrderDetails limit 5").fetchall()
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
    return get_api("ShipperViews","Shippers")

@app.route("/shippers",methods=["POST"])
def post_shippers():
    return post_api("Shippers",flask.request.json)
@app.route("/shippers/<id>",methods = ["GET"])
def get_shippers_via_id(id):
    api = get_api("ShipperViews", "Shippers",id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/shippers/<id>",methods = ["DELETE"])
def delete_shipper(id):
    return delete_api("Shippers",id)
@app.route("/shippers/<id>",methods = ["PUT"])
def put_shipper(id):
    return put_api("Shippers", id, flask.request.json)

@app.route("/customers",methods = ["GET"])
def get_customers():
    return get_api("CustomerViews","Customers")

@app.route("/customers",methods=["POST"])
def post_customers():
    return post_api("Customers",flask.request.json)
@app.route("/customers/<id>",methods = ["GET"])
def get_customers_via_id(id):
    api = get_api("CustomerViews", "Customers", id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/customers/<id>",methods = ["DELETE"])
def delete_customer(id):
    return delete_api("Customers",id)
@app.route("/customers/<id>",methods = ["PUT"])
def put_customer(id):
    return put_api("Customers", id, flask.request.json)

@app.route("/suppliers",methods = ["GET"])
def get_suppliers():
    return get_api("SupplierViews","Suppliers")

@app.route("/suppliers",methods=["POST"])
def post_suppliers():
    return post_api("Suppliers",flask.request.json)
@app.route("/suppliers/<id>",methods = ["GET"])
def get_suppliers_via_id(id):
    api = get_api("SupplierViews", "Suppliers", id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/suppliers/<id>",methods = ["DELETE"])
def delete_supplier(id):
    return delete_api("Suppliers",id)
@app.route("/suppliers/<id>",methods = ["PUT"])
def put_supplier(id):
    return put_api("Suppliers", id, flask.request.json)

@app.route("/categories",methods = ["GET"])
def get_categories():
    return get_api("Categories","Categories")

@app.route("/categories",methods=["POST"])
def post_categories():
    return post_api("categories",flask.request.json)
@app.route("/categories/<id>",methods = ["GET"])
def get_category_via_id(id):
    api = get_api("Categories", "Categories", id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/categories/<id>",methods = ["DELETE"])
def delete_category(id):
    return delete_api("Categories",id)
@app.route("/categories/<id>",methods = ["PUT"])
def put_category(id):
    return put_api("categories", id, flask.request.json)

@app.route("/products",methods = ["GET"])
def get_products():
    return get_api("ProductViews","Products")

@app.route("/products",methods=["POST"])
def post_products():
    return post_api("Products",flask.request.json)
@app.route("/products/<id>",methods = ["GET"])
def get_products_via_id(id):
    api = get_api("ProductViews", "Products", id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/products/<id>",methods = ["DELETE"])
def delete_product(id):
    return delete_api("Products",id)
@app.route("/products/<id>",methods = ["PUT"])
def put_product(id):
    return put_api("Products", id, flask.request.json)

@app.route("/employees",methods = ["GET"])
def get_employees():
    return get_api("EmployeeViews","Employees")

@app.route("/employees",methods=["POST"])
def post_employees():
    return post_api("Employees",flask.request.json)
@app.route("/employees/<id>",methods = ["GET"])
def get_employees_via_id(id):
    api = get_api("EmployeeViews", "Employees", id)
    if api == {}:
        flask.abort(404)
    return api

@app.route("/employees/<id>",methods = ["DELETE"])
def delete_employee(id):
    return delete_api("Employees",id)
@app.route("/employees/<id>",methods = ["PUT"])
def put_employee(id):
    return put_api("Employees", id, flask.request.json)

@app.route("/orders",methods = ["GET"])
def get_orders():
    api = get_api("OrderViews","Orders")
    if api == {}:
        return {}
    for item in api['orders']:
        item["Estimated"] = connection.execute("select sum(Quantity*Price) from OrderDetails inner join Products on OrderID = '{}' and OrderDetails.ProductID = Products.ProductID".format(item["OrderID"])).fetchall()[0][0]
        if item["Estimated"] == None:
            item["Estimated"] = 0.0
    api["total"] = connection.execute("select sum(Total) from OrderPayments").fetchall()[0][0]
    return api
@app.route("/orders",methods = ["POST"])
def post_order():
    json = flask.request.json
    api = post_api("Orders",json)
    if api["message"] == "Failed":
        return api
    try:
        connection.execute(update(table["OrderPayments"]).where(table["OrderPayments"].OrderID == json["OrderID"]).values({table["OrderPayements"].PaymentMethod:json[table["PaymentMethod"].columns[i].__dict__["name"]]}))
    except:
        pass
    return {"message":"Success","posted":get_api("OrderViews","Orders",json["OrderID"])}

@app.route("/orders/<id>",methods = ["GET"])
def get_orders_via_id(id):
    api = get_api("OrderViews", "Orders", id)
    if api == {}:
        flask.abort(404)
    else:
        api["OrderDetails"] = [dict(zip(["OrderID","ProductID","ProductName","Quantity","Price","Estimated"],row)) for row in connection.execute(table["OrderDetailViews"].select(table["OrderDetailViews"].columns.OrderID == id).where()).fetchall()]
        api["Estimated"] = connection.execute("select sum(Quantity*Price) from OrderDetails inner join Products on OrderID = '{}' and OrderDetails.ProductID = Products.ProductID".format(id)).fetchall()[0][0]
        return flask.jsonify(api)
@app.route("/orders/<id>",methods=["POST"])
def post_order_details(id):
    try:
        if id_check(id) == False:
            raise NameError("Illegal ID")
        json = flask.request.json
        connection.execute(table["OrderDetails"].insert([id,json["ProductID"],json["Quantity"]]))
        return {"message": "Success","posted":get_api("OrderDetailViews","Orders",id,json["ProductID"])}
    except Exception as e:
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
@app.route("/orders/<id>",methods = ["PUT"])
def put_order(id):
    try:
        if id_check(id) == False:
            raise NameError("Illegal ID")
        if get_api("Orders","Orders", id) == {}:
            raise ValueError("ID not found")
        json = flask.request.json
        put_api("Orders", id, json)
        put_api("OrderPayments",id,json)
        try:
            connection.execute(update(table["OrderPayments"]).where(table["OrderPayments"].columns.OrderID == id).values({table["OrderPayments"].columns.Status: json["Status"]}))
        except Exception as e:
            print(f"{type(e)}:{e}")
    except:
        pass
    return {"message": "Success",
            "put":get_api("OrderViews","Orders",id)}
@app.route("/orders/<id>",methods = ["DELETE"])
def delete_orders(id):
    try:
        if id_check(id) == False:
            raise NameError("Illegal ID")
        if get_api("Orders","Orders", id) == {}:
            raise ValueError("ID not found")
        connection.execute(update(table["OrderPayments"]).where(table["OrderPayments"].columns.OrderID == id).values({table["OrderPayments"].columns.Status: "cancelled"}))
        return {"message": "Success","deleted":get_api("OrderDetailViews","Orders",id)}
    except Exception as e:
        return {"message":"Failed","exception":f"{type(e)}:{e}"}

@app.route("/orders/<orderid>/<productid>",methods = ["GET"])
def get_orderdetails_via_id(orderid,productid):
    api = get_api("OrderDetailViews","OrderDetails",orderid,productid)
    if api == {}:
        flask.abort(404)
    return api
@app.route("/orders/<orderid>/<productid>",methods = ["DELETE"])
def delete_order_details(orderid,productid):
    try:
        if id_check(orderid) == False or id_check(productid) == False:
            raise NameError("Illegal ID")
        if get_api("Orders","Orders", orderid,productid) == {}:
            raise ValueError("ID not found")
        deleted = get_api("OrderDetailViews","OrderDetails",orderid,productid)
        connection.execute(delete(table["OrderDetails"]).where(table["OrderDetails"].columns.OrderID == orderid and table["OrderDetails"].columns.ProductID == productid))
        return {"message": "Success", "deleted":deleted}
    except Exception as e:
        return {"message":"Failed","exception":f"{type(e)}:{e}"}
@app.route("/orders/<orderid>/<productid>",methods = ["PUT"])
def put_order_details(orderid,productid):
    try:
        if id_check(orderid) == False or id_check(productid) == False:
            raise NameError("Illegal ID")
        if get_api("Orders","Orders", orderid,productid) == {}:
            raise ValueError("ID not found")
        json = flask.request.json
        try:
            connection.execute(update(table["OrderDetails"]).where(table["OrderDetails"].columns.OrderID == orderid and table["OrderDetails"].columns.ProductID == productid).values({table["OrderDetails"].columns.ProductID : json["ProductID"]}))
        except:
            pass
        try:
            connection.execute(update(table["OrderDetails"]).where(table["OrderDetails"].columns.OrderID == orderid and table["OrderDetails"].columns.ProductID == productid).values({table["OrderDetails"].columns.Quantity : json["Quantity"]}))
        except:
            pass
        return {"message": "Success", "put":get_api("OrderDetailViews","OrderDetails", orderid,productid)}
    except Exception as e:
        return {"message":"Failed","exception":f"{type(e)}:{e}"}


if __name__ == "__main__":
    app.run(debug=True)











