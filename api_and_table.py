

import sqlalchemy
from sqlalchemy import *

engine = create_engine("sqlite:///database.db",connect_args={"check_same_thread": False})
connection = engine.connect()
metadata = MetaData()
table = {}

table["Shippers"] = Table(
        "Shippers", metadata,
        Column("ShipperID", VARCHAR(), unique = True, primary_key = True),
        Column("ShipperName", VARCHAR()),
        Column("Phone", VARCHAR()),
        Column("Status", VARCHAR()))
table["Customers"] = Table(
        "Customers", metadata,
        Column("CustomerID", VARCHAR(), unique = True, primary_key = True),
        Column("CustomerName", VARCHAR()),
        Column("ContactName", VARCHAR()),
        Column("Address", VARCHAR()),
        Column("City", VARCHAR()),
        Column("PostalCode", VARCHAR()),
        Column("Country", VARCHAR()),
        Column("Status", VARCHAR()))
table["Suppliers"] = Table(
        "Suppliers", metadata,
        Column("SupplierID", VARCHAR() , unique = True, primary_key = True),
        Column("SupplierName", VARCHAR()),
        Column("ContactName", VARCHAR()),
        Column("Address", VARCHAR()),
        Column("City", VARCHAR()),
        Column("PostalCode", VARCHAR()),
        Column("Country", VARCHAR()),
        Column("Phone", VARCHAR()),
        Column("Status", VARCHAR()))
table["Categories"] = Table(
        "Categories", metadata,
        Column("CategoryID", VARCHAR() , unique = True, primary_key = True),
        Column("CategoryName", VARCHAR()),
        Column("Description", TEXT()))
table["Products"] = Table(
        "Products", metadata,
        Column("ProductID", VARCHAR() , unique = True, primary_key = True),
        Column("ProductName", VARCHAR()),
        Column("SupplierID", VARCHAR()),
        Column("CategoryID", VARCHAR()),
        Column("Unit", INT()),
        Column("Price", REAL()))
table["Employees"] = Table(
        "Employees", metadata,
        Column("EmployeeID", VARCHAR() , unique = True, primary_key = True),
        Column("LastName", VARCHAR()),
        Column("FirstName", VARCHAR()),
        Column("BirthDate", VARCHAR()),
        Column("Notes", TEXT()),
        Column("Status", VARCHAR(20)))
table["Orders"] = Table(
        "Orders", metadata,
        Column("OrderID", VARCHAR(), unique = True, primary_key = True),
        Column("CustomerID", VARCHAR()),
        Column("EmployeeID", VARCHAR()),
        Column("ShipperID", VARCHAR()))

table["OrderPayments"]  = Table(
        "OrderPayments", metadata,
        Column("OrderID", VARCHAR() , unique = True, primary_key = True),
        Column("Total", REAL()),
        Column("PaymentMethod", VARCHAR()),
        Column("Status", VARCHAR()))
table["OrderDetails"]  = Table(
        "OrderDetails", metadata,
        Column("OrderID", VARCHAR()),
        Column("ProductID", VARCHAR()),
        Column("Quantity", INT()))

table["ShipperViews"] = Table(
        "ShipperViews", metadata,
        Column("ShipperID", VARCHAR(), unique = True, primary_key = True),
        Column("ShipperName", VARCHAR()),
        Column("Phone", VARCHAR()))

table["CustomerViews"] = Table(
        "CustomerViews", metadata,
        Column("CustomerID", VARCHAR(), unique = True, primary_key = True),
        Column("CustomerName", VARCHAR()),
        Column("ContactName", VARCHAR()),
        Column("Address", VARCHAR()),
        Column("City", VARCHAR()),
        Column("PostalCode", VARCHAR()),
        Column("Country", VARCHAR()))

table["EmployeeViews"] = Table(
        "EmployeeViews", metadata,
        Column("EmployeeID", VARCHAR() , unique = True, primary_key = True),
        Column("LastName", VARCHAR()),
        Column("FirstName", VARCHAR()),
        Column("BirthDate", VARCHAR()),
        Column("Notes", TEXT()))

table["SupplierViews"] = Table(
        "SupplierViews", metadata,
        Column("SupplierID", VARCHAR() , unique = True, primary_key = True),
        Column("SupplierName", VARCHAR()),
        Column("ContactName", VARCHAR()),
        Column("Address", VARCHAR()),
        Column("City", VARCHAR()),
        Column("PostalCode", VARCHAR()),
        Column("Country", VARCHAR()),
        Column("Phone", VARCHAR()))

table["ProductViews"] = Table(
        "ProductViews", metadata,
        Column("ProductID", VARCHAR() , unique = True, primary_key = True),
        Column("ProductName", VARCHAR()),
        Column("SupplierID", VARCHAR()),
        Column("SupplierName", VARCHAR()),
        Column("CategoryID", VARCHAR()),
        Column("CategoryName", VARCHAR()),
        Column("Unit", INT()),
        Column("Price", REAL()))

table["OrderViews"] = Table(
    "OrderViews",metadata,
    Column("OrderID",VARCHAR(),primary_key=True,unique=True),
    Column("CustomerID",VARCHAR()),
    Column("CustomerName",VARCHAR()),
    Column("EmployeeID",VARCHAR()),
    Column("EmployeeName",VARCHAR()),
    Column("ShipperID",VARCHAR()),
    Column("ShipperName",VARCHAR()),
    Column("Date",VARCHAR()),
    Column("PaymentMethod",VARCHAR()),
    Column("Status",VARCHAR()),
    Column("Total",REAL())
)

table["OrderDetailViews"]  = Table(
        "OrderDetailViews", metadata,
        Column("OrderID", VARCHAR()),
        Column("ProductID", VARCHAR()),
        Column("ProductName", VARCHAR()),
        Column("Quantity", INT()),
        Column("Price", REAL()),
        Column("Estimated", REAL()))

forbidden_letter = []
for i in range(0,128):
    if i < 48 or (i > 57 and i <65) or (i > 90 and i < 97) or i > 122:
        forbidden_letter.append(chr(i))
def id_check(id):
    try:
        for i in forbidden_letter:
            if i in id:
                return False
        return True
    except:
        return False

def has_Status(table_name):
        try:
                for column in table[table_name].columns:
                        if column.__dict__["name"] == "Status":
                                return True
                return  False
        except:
                return False

def get_api(table_view,table_name,id = None,id_2 = None):
        try:
                if id_check(id) == False and id != None:
                        raise ValueError("Illegal ID")
                column_list = [column.__dict__["name"] for column in table[table_view].columns]
                if id == None:
                        data = connection.execute(table[table_view].select()).fetchall()
                        return {table_name.lower(): [dict(zip(column_list, row)) for row in data]}
                elif id_2 == None:
                        data = connection.execute(table[table_view].select().where(table[table_view].columns[0] == id)).fetchall()[0]
                        return dict(zip(column_list,data))
                else:
                        data = connection.execute(
                                table[table_view].select().where(table[table_view].columns[0] == id and table[table_view].columns[1] == id_2)).fetchall()[0]
                        return dict(zip(column_list, data))
        except Exception as e:
                return {}

def post_api(table_name,json):
        try:
                id = table[table_name].columns[0].__dict__["name"]
                if id_check(id) == False:
                        raise ValueError("Illegal ID")
                column_list = [column.__dict__["name"] for column in table[table_name].columns]
                if has_Status(table_name):
                        column_list.pop()
                        insert_value = [json[column] for column in column_list]
                        insert_value.append("available")
                        connection.execute(table[table_name].insert(insert_value))
                else:
                        insert_value = [json[column] for column in column_list]
                        connection.execute(table[table_name].insert(insert_value))
                return {"message": "Success","posted":get_api(table_name,table_name,json[id])}
        except Exception as e:
                return {"message": "Failed","exception": f"{type(e)}:{e}"}

def put_api(table_name,id,json):
        try:
                if id_check(id) == False:
                        raise ValueError("Illegal ID")
                if get_api(table_name, table_name, id) == {}:
                        raise ValueError("ID not found")
                for i in range(1,len(table[table_name].columns)-has_Status(table_name)):
                        try:
                                connection.execute(update(table[table_name]).where(table[table_name].columns[0]==id).values({table[table_name].columns[i]:json[table[table_name].columns[i].__dict__["name"]]}))
                        except:
                                pass
                return {"message": "Success", "put": get_api(table_name, table_name,id)}
        except Exception as e:
                return {"message": "Failed","exception": f"{type(e)}:{e}"}
def delete_api(table_name,id):
        try:
                if id_check(id) == False:
                        raise ValueError("Illegal ID")
                if get_api(table_name,table_name, id) == {}:
                        raise ValueError("ID not found")
                deleted = get_api(table_name, table_name, id)
                if has_Status(table_name):
                        connection.execute(update(table[table_name]).where(table[table_name].columns[0]==id).values({table[table_name].columns.Status:'unavailable'}))
                else:
                        connection.execute(delete(table[table_name]).where(table[table_name].columns[0]==id))
                return {"message": "Success", "deleted": deleted}
        except Exception as e:
                return {"message": "Failed","exception": f"{type(e)}:{e}"}

