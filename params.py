# URLs

# for local
# CATALOG_ENDPOINT = "http://127.0.0.1:5011"
# CUSTOMER_ENDPOINT = "http://127.0.0.1:5012"
# ORDER_ENDPOINT = "http://127.0.0.1:5013"
# COMPOSITE_ENDPOINT = "http://127.0.0.1:5014"

# for aws
CATALOG_ENDPOINT = "http://ec2-44-203-201-57.compute-1.amazonaws.com:5011"
CUSTOMER_ENDPOINT = "http://6156customer-env.eba-m4hgj3cy.us-east-1.elasticbeanstalk.com"
ORDER_ENDPOINT = "http://ordermicroservice-env.eba-p53mr9ym.us-east-1.elasticbeanstalk.com"
COMPOSITE_ENDPOINT = "http://127.0.0.1:5014"

# put together
CATALOG_URL = CATALOG_ENDPOINT + "/items"
CUSTOMER_URL = CUSTOMER_ENDPOINT + "/customer"
ORDER_URL = ORDER_ENDPOINT + "/order"
COMPOSITE_URL = COMPOSITE_ENDPOINT
