from flask import Flask, Response, request, jsonify, json, url_for
from flask_cors import CORS
from catalog_api import catalog_api
from customer_api import customer_api
from params import CATALOG_ENDPOINT, ORDER_ENDPOINT
from smartstreet_api.smart_street_adaptor import SmartyStreetsAdaptor
# from requests_futures.sessions import FuturesSession
import requests

app = Flask(__name__)
CORS(app)


# For order service
# @app.route("/order", methods=["GET"])
# def post_order():
#     data = json.loads(request.data)
#     pass


@app.before_request
def before_request():
    email = json.loads(request.data)["email"]
    log_in = customer_api.get_login_info(email)
    if not log_in:
        return Response(json.dumps({"message": "User not log in"}), status=404, content_type="application/json")


@app.route("/", methods=["GET"])
def index():
    old_stock = catalog_api.get_stock(item_id=1)
    return {"old_stock": old_stock}


@app.route("/order", methods=["POST"])
def post_order():
    data = json.loads(request.data)
    url = ORDER_ENDPOINT + url_for("post_order")
    r = requests.post(url=url, json=data)
    return Response(json.dumps(r.json()), status=r.status_code, content_type="application/json")

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


# @app.route("/order/<int:orderid>/orderline/<int:lineid>", methods=["PUT"])
# # can only modify the item amount
# def put_orderline(orderid, lineid):
#     data = json.loads(request.data)
#     if "amount" in data:
#         new_amount = data["amount"]
#     pass


@app.route("/verifyaddress", methods=["GET"])
def verify_address():
    addr_dict = {
        "city": request.args.get("city"),
        "state": request.args.get("state"),
        "street1": request.args.get("street1"),
        "street2": request.args.get("street2"),
        "zipcode": request.args.get("zipcode")
    }
    sm = SmartyStreetsAdaptor()
    sm.do_search(addr_dict)
    di = sm.to_json()
    li = list()
    if di:
        for _, v in di.items():
            li.append({"delivery_line_1": v["delivery_line_1"],
                       "delivery_line_2": v["delivery_line_2"],
                       "last_line": v["last_line"],
                       "verified": getattr(v["analysis"], 'dpv_match_code')
                       })
        result = li[0]

        verified = result["verified"]
        if verified == "Y":
            print("result:", result)
            return jsonify(result)
        elif verified == "D":
            return Response(json.dumps({"message": "street2 missing"}), status=400, content_type="application/json")
        elif verified == "N":
            return Response(json.dumps({"message": "address not valid"}), status=400, content_type="application/json")
        elif verified == "S":
            return Response(json.dumps({"message": "street2 not valid"}), status=400, content_type="application/json")
    return Response(json.dumps({"message": "no address found"}), status=400, content_type="application/json")


@app.route("/autocomplete", methods=["GET"])
def autocomplete_address():
    input_address = request.args.get('address')
    sm = SmartyStreetsAdaptor()
    res = sm.do_autocomplete(input_address)
    li = []
    if res:
        for suggestion in res:
            li.append({
                'city': suggestion.city,
                'entries': suggestion.entries,
                'secondary': suggestion.secondary,
                'state': suggestion.state,
                'street_line': suggestion.street_line,
                'zipcode': suggestion.zipcode
            })
        print("Suggestion: ", res)
        return jsonify(li)
    else:
        return Response(json.dumps({"message": "no address found"}), status=400, content_type="application/json")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5014)
