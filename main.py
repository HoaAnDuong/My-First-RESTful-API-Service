import sqlite3
import flask
from flask import Flask

connection = sqlite3.connect("database.db",check_same_thread=False) #if check_same_thread = True, sqlite3 won't work
cursor = connection.cursor()
app = Flask(__name__)

table_list = [item[0] for item in cursor.execute("select name from sqlite_schema where type = 'table';").fetchall()]
print(table_list)

#These queries are made by string concatenation
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
    except:
        return {}


def post_json(table_name,json,has_status = False):
    cursor.execute("begin transaction")
    column_list = [item[1] for item in cursor.execute(f"pragma table_info({table_name})").fetchall()]
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
        return {"message":f"{type(e)}:{e}"}
def delete_json(table_name,id,has_status=False,table_name_singular = None):
    cursor.execute("begin transaction")
    json = get_json_via_id(table_name, id, has_status,table_name_singular)
    if json == {}:
        cursor.execute("rollback")
        return {"message": "ID not found"}
    if has_status:
        try:
            query = f"update {table_name} set Status = 'unavailable' where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
            cursor.execute(query)
            cursor.execute("commit")
            return {"message":"Success","deleted":json}
        except Exception as e:
            cursor.execute("commit")
            return {"message": f"{type(e)}:{e}"}
    else:
        try:
            query = f"delete from {table_name} where {table_name[0:-1] if table_name_singular == None else table_name_singular}ID = '{id}'"
            cursor.execute(query)
            cursor.execute("commit")
            return {"message":"Success","deleted":json}
        except Exception as e:
            cursor.execute("rollback")
            return {"message": f"{type(e)}:{e}"}

def put_json(table_name,id,json,has_status=False,table_name_singular = None):
    cursor.execute("begin transaction")
    check_json = get_json_via_id(table_name,id,has_status,table_name_singular)
    if check_json == {}:
        cursor.execute("rollback")
        return {"message": "ID not found"}
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
            return {"message": f"{type(e)}:{e}"}

def get_json_via_query(column_list,query,table_name):
    try:
        json = {}
        data = cursor.execute(query).fetchall()
        if len(data) == 1:
            json = dict(zip(column_list,data))
        else:
            json[table_name.lower()] = [dict(zip(column_list,row)) for row in data]
        return json
    except Exception as e:
        print(e)
        return {}



#Routes

@app.route("/shippers")
def get_shippers():
    return flask.jsonify(get_json("Shippers",True))

@app.route("/shippers",methods=["POST"])
def post_shippers():
    return flask.jsonify(post_json("Shippers",flask.request.json,True))
@app.route("/shippers/<id>")
def get_shippers_via_id(id):
    json = get_json_via_id("Shippers",id,True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/shippers/<id>",methods = ["DELETE"])
def delete_shipper(id):
    return(flask.jsonify(delete_json("Shippers",id,True)))

@app.route("/shippers/<id>",methods = ["PUT"])
def put_shipper(id):
    return flask.jsonify(put_json("Shippers", id, flask.request.json, True))


@app.route("/customers")
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
    return (flask.jsonify(delete_json("Customers", id, True)))

@app.route("/customers/<id>", methods=["PUT"])
def put_customer(id):
    return flask.jsonify(put_json("Customers", id, flask.request.json, True))

@app.route("/suppliers")
def get_suppliers():
    return flask.jsonify(get_json("Suppliers", True))

@app.route("/suppliers", methods=["POST"])
def post_suppliers():
    return flask.jsonify(post_json("Suppliers", flask.request.json, True))

@app.route("/suppliers/<id>")
def get_suppliers_via_id(id):
    json = get_json_via_id("Suppliers", id, True)
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/suppliers/<id>", methods=["DELETE"])
def delete_supplier(id):
    return (flask.jsonify(delete_json("Suppliers", id, True)))

@app.route("/suppliers/<id>", methods=["PUT"])
def put_supplier(id):
    return flask.jsonify(put_json("Suppliers", id, flask.request.json, True))

@app.route("/categories")
def get_categories():
    return flask.jsonify(get_json("Categories", False))

@app.route("/categories", methods=["POST"])
def post_categories():
    return flask.jsonify(post_json("Categories", flask.request.json, False))

@app.route("/categories/<id>")
def get_categories_via_id(id):
    json = get_json_via_id("Categories", id, False,"Category")
    if json == {}:
        flask.abort(404)
    else:
        return json

@app.route("/categories/<id>", methods=["DELETE"])
def delete_categories(id):
    return (flask.jsonify(delete_json("Categories", id, False,"Category")))

@app.route("/categories/<id>", methods=["PUT"])
def put_categories(id):
    return flask.jsonify(put_json("Categories", id, flask.request.json, False,"Category"))

@app.route("/products")
def get_products():
    json = get_json_via_query(['ProductID', 'ProductName', 'SupplierID','SupplierName', 'CategoryID','CategoryName', 'Unit', 'Price','Total'],"select ProductID, ProductName, Products.SupplierID, SupplierName, Products.CategoryID, CategoryName, Unit, Price,(Unit*Price) from Products inner join Suppliers on Products.SupplierID = Suppliers.SupplierID inner join Categories on Products.CategoryID = Categories.CategoryID","Products")
    json["total"] = cursor.execute("select sum(unit*price) from Products").fetchall()[0][0]
    return flask.jsonify(json)

if __name__ == "__main__":
    app.run(debug=True)











