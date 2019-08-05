from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import db

Base = declarative_base()

orders_products_table = db.Table('orders_products',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(String(45))
  l_name = db.Column(String(45))
  email = db.Column(String(45))
  pw = db.Column(String(45))
  order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
  order = db.relationship("Order",back_populates="user")
  created_at = db.Column(DateTime, server_default=func.now())
  updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())

class Order(db.Model):
  __tablename__ = "orders"
  id = db.Column(db.Integer, primary_key=True)
  cost = db.Column(db.Integer)
  paypal_orders_id = db.Column(db.Integer)
  user = db.relationship("User",back_populates="order")
  shipping = db.relationship("Shipping",back_populates="order")
  products_in_this_order = db.relationship("Product",secondary=orders_products_table,back_populates="orders_containing_this_product")
  created_at = db.Column(DateTime, server_default=func.now())
  updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())
 
class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(String(45))
  descr = db.Column(String(45))
  unit_cost = db.Column(db.Integer)
  img_file = db.Column(String(200))
  orders_containing_this_product = db.relationship("Order",secondary=orders_products_table,back_populates="products_in_this_order")
  created_at = db.Column(DateTime, server_default=func.now())
  updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())

class Shipping(db.Model):
  __tablename__ = "shippings"
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(String(45))
  last_name = db.Column(String(45))
  address = db.Column(String(255))
  order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
  order = db.relationship("Order",back_populates="shipping")
  created_at = db.Column(DateTime, server_default=func.now())
  updated_at = db.Column(DateTime, server_default=func.now(), onupdate=func.now())