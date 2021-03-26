"""
File which includes endpoints:  /api/create
                                /api/list
"""
# 3rd party modules
import logging
from datetime import datetime
from flask import abort, Response, request

# Local modules
from lib import routes
from lib import db_controller

logger = logging.getLogger(__name__)
folder = routes.rootFolder


def create():
    """
    POST method. It create a new order and order_detail if the requirements are right.
    """
    result = []
    dict_data = request.get_json()
    name = dict_data['name']
    result.append(check_info('name', name, name))
    email = dict_data['email']
    result.append(check_info('email', name, email))
    address = dict_data['delivery_address']
    result.append(check_info('address', name, address))

    if False in result:
        logger.info('Check your request')
        return abort(description='Check your request', status=404)

    # products may come from a .csv file
    products = ('Product A', 'Product B', 'Product C', 'Product D')
    quantity = [int(dict_data[product]) for product in products]

    possible_quantity = 5
    requested_quantity = sum(quantity)
    dict_products = {}
    if requested_quantity <= possible_quantity:
        dict_all_products = dict(zip(products, quantity))
        for key, value in dict_all_products.items():
            if value != 0:
                dict_products[key] = value

        dict_general = {}
        for product in dict_products:

            # Extract info from local database
            product_detail = db_controller.search_product(name=product)

            dict_general[product] = {
                'product_id': product_detail['product_id'],
                'product_description': product_detail['product_description'],
                'price': product_detail['price']
            }

        products_index = {key:value['product_id'] for key, value in dict_general.items()}
        customer_id = db_controller.search_user(name, 'customer_id')
        can_buy = db_controller.search_relation(customer_id, 'id_product')

        for key, value in products_index.items():
            if value not in can_buy:
                logger.info("You can not buy %s", key)
                return abort(description=f'You can not buy {key}', status=404)

        products_description = {key:value['product_description']
                                    for key, value in dict_general.items()}
        products_price = {key:value['price'] for key, value in dict_general.items()}

        zip_total = zip(dict_products.values(), products_price.values())
        total = sum([elem1*elem2 for elem1, elem2 in zip_total])
        order = {   'customer_id': customer_id, 'delivery_address': address,
                    'total': "{:.2f}".format(total)}

        try:
            id_order = db_controller.create_order(order)
        except Exception as exc:
            logger.error(exc)
            return abort(description='Something went wrong', status=500)

        for i in dict_products:
            order_detail = {'order_id': id_order, 'product_id': products_index[i],
                            'product_description': products_description[i],
                            'price': products_price[i],
                            'quantity': dict_products[i]}

            try:
                db_controller.create_order_detail(order_detail)
            except Exception as exc:
                logger.error(exc)
                return abort(description='Something went wrong', status=500)

        logger.info("%s, your order is on the way", name)
        return Response(f"{name}, your order is on the way", status=200)
    logger.info('%s, you exceed limit of 5 products', name)
    return abort(description=f'{name}, you exceed limit of 5 products', status=404)


def list_orders():
    """
    POST method. It create a list order between a range of dates.
    """
    result = []
    orders = []
    
    dict_data = request.get_json()  # Extract info to devicesSignature from web service
    name = dict_data['name']
    result.append(check_info('name', name, name))
    initial_str_date = dict_data['initial_date']
    result.append(check_info('initial_date', name, initial_str_date))
    final_str_date = dict_data['final_date']
    result.append(check_info('final_date', name, final_str_date))

    if False in result:
        logger.info('Check your request')
        return abort(description='Check your request', status=404)

    customer_id = db_controller.search_user(name, 'customer_id')
    ordered = db_controller.search_order(customer_id, 'customer_id')

    if isinstance(ordered, str):
        orders.append({
                'Creation_Date': 0,
                'Order_ID': 0,
                'Total': 0,
                'Delivery_Address': 0,
                'Products': 0
            })
        logger.info('%s does not have orders', name)
        return orders

    orders_detail = [db_controller.search_order_detail(item['order_id'], 'order_id')
                        for item in ordered]
    quantities = []
    for order_detail in orders_detail:
        aux = {}
        for specific_product in order_detail:
            product = db_controller.search_product(number_id=specific_product['product_id'])
            aux[product['name']] = specific_product['quantity']
        quantities.append(aux)

    start_date = datetime.strptime(initial_str_date, '%Y-%m-%d')
    end_date = datetime.strptime(final_str_date, '%Y-%m-%d')
    for i, order in enumerate(ordered):
        date_order = datetime.strptime(order['creation_date'], '%Y-%m-%dT%H:%M:%S.%f')
        if start_date < date_order < end_date:
            orders.append({
                'Creation_Date': date_order.date(),
                'Order_ID': order['order_id'],
                'Total': f"$ {order['total']}",
                'Delivery_Address': order['delivery_address'],
                'Products': quantities[i]

            })
    return orders


def check_info(parameter, user, parameter_value):
    """
    validate if the value has a correct format.
    """
    if not parameter_value:
        logger.info('%s is empty for the user %s', parameter, user)
        return False
    if isinstance(parameter_value, str):
        if parameter_value.isspace():
            logger.info('%s only has blank spaces for the user %s', parameter, user)
            return False
    return True
