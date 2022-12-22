import os
import json
from smart_street_adaptor import SmartyStreetsAdaptor

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup


def t1():
    lookup = StreetLookup()
    # lookup.input_id = "24601"  # Optional ID from your system

    lookup.street = "212 W 91st ST"
    # lookup.street2 = "closet under the stairs"
    # lookup.secondary = "APT 2"
    # lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = "New York"
    lookup.state = "NY"
    lookup.zipcode = "10024"
    lookup.candidates = 2
    # lookup.match = "invalid"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.

    sm_adaptor = SmartyStreetsAdaptor()
    sm_adaptor.do_lookup(lookup)
    j_result = sm_adaptor.to_json()

    print("T1 result = \n", json.dumps(j_result, indent=2, default=str))


def t2():
    lookup = StreetLookup()
    # lookup.input_id = "24601"  # Optional ID from your system

    lookup.street = "21 Hoyt"
    # lookup.street2 = "closet under the stairs"
    # lookup.secondary = "APT 2"
    # lookup.urbanization = ""  # Only applies to Puerto Rico addresses
    lookup.city = "S Salem"
    lookup.state = "NY"
    # lookup.zipcode = "02341"
    lookup.candidates = 3
    # lookup.match = "invalid"  # "invalid" is the most permissive match,
    # this will always return at least one result even if the address is invalid.
    # Refer to the documentation for additional Match Strategy options.

    sm_adaptor = SmartyStreetsAdaptor()
    sm_adaptor.do_lookup(lookup)
    j_result = sm_adaptor.to_json()

    print("T1 result = \n", json.dumps(j_result, indent=2, default=str))


def t3():
    sm = SmartyStreetsAdaptor()

    q = {
        # "city": "Mars",
        # "state": "Sun",
        # "street1": "212 w 91st ST"
        "city": "New York",
        "state": "NY",
        "street1": "212 w 91st ST"
    }
    res = sm.do_search(q)
    print("t3 result = ", res)

    if res >= 1:
        print(json.dumps(sm.to_json(), indent=2, default=str))

    di = sm.to_json()
    # print(di)
    li = list()
    if di:
        for _, v in di.items():
            # base_fields = dir(v["analysis"])
            # analysis = dict()
            # for f in base_fields:
            #     if f[0] != "_":
            #         analysis[f] = getattr(v["analysis"], f, None)
            verified = getattr(v["analysis"], 'dpv_match_code')

            li.append({"delivery_line_1": v["delivery_line_1"],
                       "delivery_line_2": v["delivery_line_2"],
                       "last_line": v["last_line"],
                       })
        result = li[0]

        verified = result["verified"]
        if verified == "Y":
            pass
            # TODO: save address
        elif verified == "D":
            return {"message": "delivery line 2 missing"}
        elif verified == "N":
            return {"message": "address not valid"}
    else:
        return {"message": "no address found"}


def t4():
    sm = SmartyStreetsAdaptor()
    address = '212 W'
    res = sm.do_autocomplete(address)

    # ['city', 'entries', 'secondary', 'state', 'street_line', 'zipcode']
    print(dir(res[0]))

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

    print("t4 result = ", li)


# t1()
# t2()
# t3()
t4()
