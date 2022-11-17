import requests
#print(requests.get("http://127.0.0.1:5000/shippers").json())
print(requests.delete("http://127.0.0.1:5000/products/'or''='").json())














# print(requests.post("http://127.0.0.1:5000/orders",json={
#     'OrderID':"ORD0004",
#     'CustomerID': 'CUS0003',
#     'EmployeeID': 'EMP0003',
#     'ShipperID': 'SHI0006',
#     'PaymentMethod': 'Cash'
# }).json())
# print(requests.post("http://127.0.0.1:5000/orders/ORD0004",json={"ProductID":"PRO0002","Quantity":10}).json())
# print(requests.put("http://127.0.0.1:5000/orders/ORD0004/PRO0002",json={"ProductID":"PRO0003","Quantity":10}).json())
# print(requests.delete("http://127.0.0.1:5000/orders/ORD0004/PRO0003").json())
# print(requests.post("http://127.0.0.1:5000/orders/ORD0003",json={"ProductID":"PRO0003","Quantity":5}))
# print(requests.put("http://127.0.0.1:5000/orders/ORD0003",json={"Status":"paid"}).json())
#print(requests.post("http://127.0.0.1:5000/orders/ORD0003",json={"ProductID":"PRO0002","Quantity":5}).json())
# print(requests.delete("http://127.0.0.1:5000/orders/ORD0003").json())