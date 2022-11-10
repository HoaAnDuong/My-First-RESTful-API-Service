import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

print(cursor.execute(f"select ShipperID,ShipperName,Phone from Shippers where Status = 'available' and ShipperID = 'SHI000';").fetchall())

cursor.execute("select name from sqlite_schema where type = 'table';")
table_list = cursor.fetchall()
table_list = [item[0] for item in table_list]
print(table_list)

for table in table_list:
    api = {}
    column_list = [item[1] for item in cursor.execute(f"pragma table_info({table})")]
    data = cursor.execute(f"select * from {table}").fetchall()
    print(column_list)
    if table != "OrderDetails":
        for item in data:
            api[item[0]] = {}
            for i in range(1, len(column_list)):
                api[item[0]][column_list[i]] = item[i]
        print(api)
    else:
        for item in data:
            try:
                api[item[0]][item[1]] = item[2]
            except:
                api[item[0]] = {}
                api[item[0]][item[1]] = item[2]
        print(api)

