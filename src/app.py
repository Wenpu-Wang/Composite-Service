from flask import Flask, Response, request, jsonify, json, url_for
from flask_cors import CORS
from catalog_api import catalog_api
from params import CATALOG_ENDPOINT, ORDER_ENDPOINT
# from requests_futures.sessions import FuturesSession
import requests

app = Flask(__name__)
CORS(app)


# For order service
# @app.route("/order", methods=["GET"])
# def post_order():
#     data = json.loads(request.data)
#     pass


@app.route("/", methods=["GET"])
def index():
    old_stock = catalog_api.get_stock(item_id=1)
    return {"old_stock": old_stock}


@app.route("/order/<int:orderid>/orderline", methods=["POST"])
def post_orderline(orderid):
    data = json.loads(request.data)
    item_id, amount = data["itemid"], data["amount"]
    old_stock = catalog_api.get_stock(item_id=item_id)

    # if item not found
    if not old_stock:
        return Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")

    # post orderline
    if not catalog_api.check_stock_availability(item_id, amount):
        return Response(json.dumps({"message": "item not available"}), status=404, content_type="application/json")
    url = ORDER_ENDPOINT + url_for("post_orderline", orderid=orderid)
    r = requests.post(url=url, json=data)
    print("status code:", r.status_code)
    if r.status_code == 200:
        catalog_api.minus_stock(item_id=item_id, amount=amount)
    return r.status_code, r.json()


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5014)
