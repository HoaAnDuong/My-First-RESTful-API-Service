import requests

# print(requests.get("http://127.0.0.1:5000/shippers").json())
# print(requests.post("http://127.0.0.1:5000/shippers",json={'ShipperID': 'SHI0010', 'ShipperName': 'Doan Van Z', 'Phone': '0121999999'}).json())
# print(requests.put("http://127.0.0.1:5000/shippers/SHI0010",json={'Phone': '0121888888'}).json())
# print(requests.delete("http://127.0.0.1:5000/shippers/SHI0010").json())


# print(requests.post("http://127.0.0.1:5000/orders",json={"OrderID":"ORD0008","CustomerID":"CUS0001","EmployeeID":"EMP0001","ShipperID":"SHI0004","PaymentMethod":"Cash"}).json())
# print(requests.put("http://127.0.0.1:5000/orders/ORD0008/PRO0008",json={"ProductID":"PRO0006"}).json())
# print(requests.post("http://127.0.0.1:5000/orders/ORD0008",json={"ProductID":"PRO0001","Quantity":2}))
# print(requests.post("http://127.0.0.1:5000/orders/ORD0008",json={"ProductID":"PRO0003","Quantity":1}))
# print(requests.put("http://127.0.0.1:5000/orders/ORD0008",json={"PaymentMethod":"Mobile Banking","Status": "paid"}))
print(requests.put("http://127.0.0.1:5000/products/PRO0003",json={"CategoryID":"CAT0003"}).json())
#print(requests.put("http://127.0.0.1:5000/orders/ORD0005",json={"Status":"paid"}).json())


