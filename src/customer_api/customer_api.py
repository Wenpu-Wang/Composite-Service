import json
import requests

endpoint = "http://127.0.0.1:5012/customers"

def get_login_info(email):
    customer_url = f"{endpoint}/validate_login/{email}"
    rsp = requests.get(url=customer_url).json()
    res = rsp["has_login"]
    print(res)
    return res
# def get_stock(item_id):
#     # return stock of an item
#     stock_url = f"{endpoint}/{item_id}"
#     rsp = requests.get(url=stock_url).json()
#     stock = rsp["stock"]
#     return stock
#
#
# def minus_stock(item_id, amount):
#     old_stock = get_stock(item_id)
#     if old_stock < amount:
#         return False
#     new_stock = old_stock - amount
#     stock_url = f"{endpoint}/{item_id}"
#     update_json = {"stock": new_stock}
#     rsp = requests.put(url=stock_url, json=update_json)
#     return True


if __name__ == "__main__":
    pass
