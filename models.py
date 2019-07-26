from sqlalchemy.sql import func
from config import db

#users - id, fn, ln, email, pw, created_at, updated_at
#orders - id, cost, user_id, created_at,updated_at 
#products - id, name, description, unit cost, quantity_available, created_at, updated_at
#orders_products - id, order_id, product_id

association_table = Table('association', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class Users(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  f_name = db.Column(db.String(45))
  l_name = db.Column(db.String(45))
  email = db.Column(db.String(45))
  pw = db.Column(db.String(45))
  created_at = db.Column(db.DateTime, server_default=func.now())
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Orders(db.Model):
  __tablename__ = "orders"
  products_ordered = relationship (
   "Products",
   secondary=Orders_Products,
   back_populates="orders")
  
  id = db.Column(db.Integer, primary_key=True)
  cost = db.Column(db.Integer)
  paypal_orders_id = db.Column(db.Integer)
  user_id =  db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
  created_at = db.Column(db.DateTime, server_default=func.now())
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
 
class Products(db.Model):
  __tablename__ = "products"
  orders_containing_product = relationship (
   "Orders",
   secondary=Orders_Products,
   back_populates="products")
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(45))
  desc = db.Column(db.String(45))
  unit_cost = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, server_default=func.now())
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Orders_Products(db.Model):
  __tablename__ = "order_products"
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, server_default=func.now())
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


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

