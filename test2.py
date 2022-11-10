import sqlite3

connection = sqlite3.connect("database.db") #if check_same_thread = True, sqlite3 won't work
cursor = connection.cursor()

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
print(cursor.execute("select sum(Unit*Price) from Products;").fetchall()[0][0])
print(get_json_via_query(['ProductID', 'ProductName', 'SupplierName', 'CategoryName', 'Unit', 'Price','Total'],"select ProductID, ProductName, SupplierName, CategoryName, Unit, Price,(Unit*Price) from Products inner join Suppliers on Products.SupplierID = Suppliers.SupplierID inner join Categories on Products.CategoryID = Categories.CategoryID","Products"))