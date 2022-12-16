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
    # check if the ordered item exist
    exist = catalog_api.check_item_exist(item_id=item_id)
    if not exist:
        return Response(json.dumps({"message": "item not found"}), status=404, content_type="application/json")
    # check if the price is correct
    price_correct = catalog_api.check_price(item_id, data["price"])
    if not price_correct:
        item_price = catalog_api.get_price(item_id)
        return Response(json.dumps({"message": f"item price should be {item_price}"}), status=404,
                        content_type="application/json")
    # check if the item is available for the amount
    available = catalog_api.check_stock_availability(item_id, amount)
    if not available:
        stock = catalog_api.get_stock(item_id)
        return Response(json.dumps({"message": f"item not available, only {stock} left"}), status=404,
                        content_type="application/json")
    # POST the item into orderline
    url = ORDER_ENDPOINT + url_for("post_orderline", orderid=orderid)
    r = requests.post(url=url, json=data)
    # modify the stock if the order microservice return 200
    if r.status_code == 200:
        catalog_api.minus_stock(item_id=item_id, amount=amount)

    return Response(json.dumps(r.json()), status=r.status_code, content_type="application/json")


@app.route("/order/<int:orderid>/orderline/<int:lineid>", methods=["PUT"])
def put_orderline(orderid):
    pass


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5014)
