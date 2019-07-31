from flask import render_template, redirect, request, session	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db
from models import User, Order, Product, orders_products_table
import json

def landing():
  #select all the products and display them on the page
  #select all the services and display them on the page
  list_of_all_products = Product.query.all()
  return render_template('landing.html',all_products = list_of_all_products)

def login():
  return render_template('registration.html')

def my_account():
  return render_template('myaccount.html')

def view_order():
  return render_template('view_order.html')

def view_cart():
  return render_template('view_cart.html')

def confirm_order():
  return render_template('confirm_order.html')

def place_order():
  return render_template('place_order.html')

def add_to_cart(id):
  if not 'cart' in session:
    session['cart'] = list()
  
  print(session['cart'])
  list_of_products = session['cart']
  
  instance_of_product = Product.query.get(id)
  product = {
    'name':instance_of_product.name,
    'cost':instance_of_product.unit_cost
  }
  list_of_products.append(product)
  session['cart'] = list_of_products
  print(session['cart'])
  return redirect('/')
  #return json.dumps({'status':'OK','cart':session['cart']})


# def add_dojo():
#   #print(request.form)
#   instance_of_dojo = Dojos(
#     name=request.form['dojo_name'], 
#     city=request.form['dojo_city'], 
#     state = request.form['dojo_state']
#     )
#   print(type(instance_of_dojo))
#   #print(instance_of_dojo)
#   db.session.add(instance_of_dojo)
#   db.session.commit()
#   #all_dojos = Dojos.query.all()
#   #print(all_dojos)
#   return redirect('/')

# def add_ninja():
#   #print(request.form)
#   instance_of_ninja = Ninjas(
#     first_name=request.form['first_name'], 
#     last_name=request.form['last_name'], 
#     dojo_id = request.form['dojo']
#     )
#   #print(type(instance_of_ninja))
#   #print(instance_of_ninja)
#   db.session.add(instance_of_ninja)
#   db.session.commit()
#   return redirect('/')