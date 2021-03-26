"""
This file contains the dabatase structure.
"""

#  3rd party modules
from datetime import datetime

# Local modules
from config import db, ma


class Customer(db.Model):
    """fields in the customer table of the database"""
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), nullable=False)
    email = db.Column(db.String(191), nullable=False)


class Product(db.Model):
    """fields in the product table of the database"""
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), nullable=False)
    product_description = db.Column(db.String(191), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Customer_product(db.Model):
    """fields in the customer_product table of the database"""
    __tablename__ = 'customer_product'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    id_customer = db.relationship("Customer")
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    id_product = db.relationship("Product")
    # customer_id = db.Column(db.Integer)
    # product_id = db.Column(db.Integer)


class Order_detail(db.Model):
    """fields in the order_detail table of the database"""
    __tablename__ = 'order_detail'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_description = db.Column(db.String(191), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    """fields in the order table of the database"""
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow, nullable=False)
    delivery_address = db.Column(db.String(191), nullable=False)
    total = db.Column(db.Float, nullable=False)


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Serializing customer table of the database"""
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    """Serializing product table of the database"""
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True

class customer_productSchema(ma.SQLAlchemyAutoSchema):
    """Serializing customer_product table of the database"""
    class Meta:
        model = Customer_product
        include_relationships = True
        load_instance = True

class Order_detailSchema(ma.SQLAlchemyAutoSchema):
    """Serializing order_detail table of the database"""
    class Meta:
        model = Order_detail
        include_relationships = True
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    """Serializing order table of the database"""
    class Meta:
        model = Order
        include_relationships = True
        load_instance = True
