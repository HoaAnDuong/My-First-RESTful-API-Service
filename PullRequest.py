import requests
print(requests.get("http://127.0.0.1:5000/categories").json())
print(requests.post("http://127.0.0.1:5000/categories",json={'CategoryID': 'CAT0008', 'CategoryName': 'Van phong pham', 'Description': 'But, thuoc, mau,...'}).json())
print(requests.put("http://127.0.0.1:5000/categories/CAT0008",json={"Description":"Do dung hoc tap"}).json())
#print(requests.delete("http://127.0.0.1:5000/categories/CAT0008"))