import requests
from params import CUSTOMER_URL


# endpoint = "http://127.0.0.1:5012/customers"

def get_login_info(email):
    customer_url = f"{CUSTOMER_URL}/validate_login/{email}"
    rsp = requests.get(url=customer_url).json()
    res = rsp["has_login"]
    print(res)
    return res


if __name__ == "__main__":
    pass
