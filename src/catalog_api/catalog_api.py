import json
import requests
from params import CATALOG_URL


def check_item_exist(item_id):
    pass


def get_stock(item_id):
    """
    :param item_id:
    :return: return num of stock if item exist
    """
    # return stock of an item
    stock_url = f"{CATALOG_URL}/{item_id}/stock"
    r = requests.get(url=stock_url)
    if r.status_code != 200:
        return False
    stock = r.json()["stock"]
    return stock


def check_stock_availability(item_id, amount):
    old_stock = get_stock(item_id)
    if old_stock < amount:
        return False
    return True


def minus_stock(item_id, amount):
    if not check_stock_availability(item_id, amount):
        return False
    new_stock = get_stock(item_id) - amount
    url = f"{CATALOG_URL}/{item_id}"
    update_json = {"stock": new_stock}
    rsp = requests.put(url=url, json=update_json)
    return True


if __name__ == "__main__":
    # # json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)
    # data = json.dumps(r.json(), sort_keys=True, indent=4)
    num_of_item_available = get_stock(2)
    print(num_of_item_available)
    print(minus_stock(item_id=2, amount=1))

