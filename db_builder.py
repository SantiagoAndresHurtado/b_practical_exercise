"""
This file create a new default database.
"""

# 3rd party modules
import os

# Local modules
from lib import routes, models
from config import db

# Data to initialize database with
CUSTOMER = [
    {'name': 'Manny Bharma', 'email': 'manny.bharma@beitech.co'},
    {'name': 'Alan Briggs', 'email': 'alan.briggs@beitech.co'},
    {'name': 'Mike Simm', 'email': 'mike.simm@beitech.co'}
]

CUSTOMER_PRODUCT = [
    {"customer_id": 1, "product_id": 1},
    {"customer_id": 1, "product_id": 2},
    {"customer_id": 1, "product_id": 3},
    {"customer_id": 2, "product_id": 2},
    {"customer_id": 3, "product_id": 1},
    {"customer_id": 3, "product_id": 4}
]

PRODUCT = [
    {'name': 'Product A', 'product_description': 'big', 'price': 4.51},
    {'name': 'Product B', 'product_description': 'medium', 'price': 3.252},
    {'name': 'Product C', 'product_description': 'small', 'price': 2.123},
    {'name': 'Product D', 'product_description': 'micro', 'price': 1.64}
]


# Delete database file if it exists currently
if os.path.exists(routes.databaseFile.split('///')[1]):
    os.remove(routes.databaseFile.split('///')[1])

# Create the database
db.create_all()

# Iterate over the CUSTOMER structure and populate the database
for client in CUSTOMER:
    x = models.Customer(name=client['name'],
                        email=client['email'])
    db.session.add(x)

for relation in CUSTOMER_PRODUCT:
    y = models.Customer_product(customer_id=relation['customer_id'],
                                product_id=relation['product_id'])
    db.session.add(y)

for item in PRODUCT:
    z = models.Product( name=item['name'],
                        product_description=item['product_description'],
                        price=item['price'])
    db.session.add(z)

db.session.commit()
