from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import db

Base = declarative_base()
#users - id, fn, ln, email, pw, created_at, updated_at
#orders - id, cost, user_id, created_at,updated_at 
#products - id, name, description, unit cost, quantity_available, created_at, updated_at
#orders_products - id, order_id, product_id

association_table = Table('order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class User(db.Model):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  f_name = Column(String(45))
  l_name = Column(String(45))
  email = Column(String(45))
  pw = Column(String(45))
  orders = relationship("Order")
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Order(db.Model):
  __tablename__ = "orders"
  products_ordered = relationship (
   "Products",
   secondary=association_table,
   back_populates="orders")
  id = Column(Integer, primary_key=True)
  cost = Column(Integer)
  paypal_orders_id = Column(db.Integer)
  user_id =  Column(Integer, ForeignKey('users.id'))
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
 
class Product(db.Model):
  __tablename__ = "products"
  orders_containing_product = relationship (
   "Orders",
   secondary=association_table,
   back_populates="products")
  id = Column(Integer, primary_key=True)
  name = Column(String(45))
  descr = Column(String(45))
  unit_cost = Column(Integer)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# class Orders_Products(db.Model):
#   __tablename__ = "order_products"
#   id = db.Column(db.Integer, primary_key=True)
#   created_at = db.Column(db.DateTime, server_default=func.now())
#   updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


# class Dojos(db.Model):
#   __tablename__ = "dojos"
#   create the table here
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(45))
#   city = db.Column(db.String(45))
#   state = db.Column(db.String(45))
#   ninjas = db.relationship("Ninjas",backref="dojos", lazy=True)
#   created_at = db.Column(db.DateTime, server_default=func.now())
#   updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
  
# class Ninjas(db.Model):
#   __tablename__ = "ninjas"
#   id = db.Column(db.Integer, primary_key=True)
#   first_name = db.Column(db.String(45))
#   last_name = db.Column(db.String(45))
#   dojo_id = db.Column(db.Integer, db.ForeignKey('dojos.id'), nullable = False)
#   # the below line could be used instead of the relationship in Dojos
#   # dojos = db.relationship('Dojo', foreign_keys=[dojo_id], backref="dojo_ninjas",cascade="all")
#   created_at = db.Column(db.DateTime, server_default=func.now())
#   updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

