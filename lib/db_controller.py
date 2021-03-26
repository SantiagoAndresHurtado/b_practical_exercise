"""
In this file operations in the database are managed
"""

# 3rd party modules
import logging

# Local modules
from config import db
from lib import models

logger = logging.getLogger(__name__)


def search_user(name=None, item=None):
    """
    Search customer in database

    param name: search by name in database
    param item: search item of the name
    :return:    item info of the customer
    """

    if name is None and item is None:
        match = models.Customer.query.all()
        return match

    match = models.Customer.query \
        .filter(models.Customer.name == name) \
        .all()  # Get the customer requested

    if len(match) == 1:
        value = []
        unique_match = match[0]
        person_schema = models.CustomerSchema()  # Serialize the data for the response
        database_info = person_schema.dump(unique_match)
        value = database_info[f'{item}']
        return value
    elif len(match) > 1:  # more than one person exists?
        logger.info("There is more than one name %s in the database", name)
        return "There is more than one name %s in the database", name
    else:  # Otherwise, didn't find that person
        logger.info("User %s doesn't exist in the database", name)
        return "User %s'{name}' doesn't exist in the database", name


def search_product(name=None, number_id=None):
    """
    Search product in database

    param name:       search by name in database
    param number_id:  search by id in database
    :return:          info of the user
    """
    if name:
        match = models.Product.query \
            .filter(models.Product.name == name) \
            .all()

    elif number_id:
        match = models.Product.query \
            .filter(models.Product.product_id == number_id) \
            .all()

    if len(match) == 1:
        unique_match = match[0]
        item_schema = models.ProductSchema()
        database_info = item_schema.dump(unique_match)
        return database_info
    elif len(match) > 1:
        logger.info("There is more than one item %s in the database", name)
        return "There is more than one item %s in the database", name
    else:
        logger.info("Item %s doesn't exist in the database", name)
        return "Item %s doesn't exist in the database", name


def search_relation(name, item):
    """
    Search relation between customer and products in database

    param name: search by name in database
    param item: search item of the name
    :return:    item info of the customer
    """
    match = models.Customer_product.query \
        .filter(models.Customer_product.customer_id == name) \
        .all()

    if len(match) >= 1:
        value = []
        for unique_match in match:
            item_schema = models.customer_productSchema()
            database_info = item_schema.dump(unique_match)
            value.append(database_info[f'{item}'])
        return value
    else:
        logger.info("Item %s doesn't exist in the database", name)
        return "Item %s doesn't exist in the database", name


def search_order(index, item):
    """
    Search order in database

    param index: search by order_id in database
    param item:  search item of the index
    :return:     item info of the index
    """
    match = models.Order.query \
        .filter(models.Order.customer_id == index) \
        .all()

    if len(match) >= 1:
        value = []
        for unique_match in match:
            item_schema = models.OrderSchema()
            database_info = item_schema.dump(unique_match)
            value.append(database_info)
        return value
    else:
        logger.info("%s doesn't exist in the database", item)
        return f"{item} doesn't exist in the database"


def search_order_detail(index, item):
    """
    Search order_detail in database

    param index: search by index in database
    param item:  search item of the order_id
    :return:     item info of the order_id
    """
    match = models.Order_detail.query \
        .filter(models.Order_detail.order_id == index) \
        .all()

    if len(match) >= 1:
        value = []
        for unique_match in match:
            item_schema = models.Order_detailSchema()  # Serialize the data for the response
            database_info = item_schema.dump(unique_match)
            value.append(database_info)
        return value
    else:
        logger.info("Item %s doesn't exist in the database", item)
        return "Item %s doesn't exist in the database", item


def create_order(detail):
    """
    Create a new order in database

    :param detail:  data to create in database
    :return:        new order id
    """

    schema = models.OrderSchema()
    new_order = schema.load(detail, session=db.session)
    db.session.add(new_order)          # Add the order to the database
    db.session.commit()
    logger.info("Order added to database")
    return new_order.order_id


def create_order_detail(detail):
    """
    Creates a new order_detail in database

    :param detail:  data to create in database
    :return:        empty
    """
    schema = models.Order_detailSchema()
    new_order = schema.load(detail, session=db.session)
    db.session.add(new_order)
    db.session.commit()
    logger.info("Order detail added to database")
