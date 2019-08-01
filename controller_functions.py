from flask import render_template, redirect, request, session	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db
from models import User, Order, Product, orders_products_table
import json

def landing():
  #select all the products and display them on the page
  #select all the services and display them on the page
  list_of_all_products = Product.query.all() 
  if 'cart' in session:    
    session['cart_total'] = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    for item in session['cart']:
      session['cart_total'] += item['quantity'] * item['unit_cost']

  return render_template('landing.html',all_products = list_of_all_products)

def clear_session():
  session.clear()
  return redirect('/')

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
    'id':id,
    'name':instance_of_product.name,
    'description':instance_of_product.descr,
    'unit_cost':instance_of_product.unit_cost,
    'quantity':1 #default quantity set to 1. 
  }
  #add products to the session
  if len(list_of_products) == 0:
    list_of_products.append(product)
  else:
    counter = 0
    for product_dict in list_of_products:
      #check if the product is already in the list_of_products.
      #if so, just increment the quantity
      #if not, add it to the list
      if product_dict['id'] == id:
        product_dict['quantity']+=1
        break
      counter+=1
      if counter == len(list_of_products):
        list_of_products.append(product)
        break
  
  session['cart'] = list_of_products
  print(session['cart'])
  return redirect('/#yoga-products')
  #return json.dumps({'status':'OK','cart':session['cart']})

def update_cart():
  print(request.form)
  print(session['cart'])
  list_of_cart_items = session['cart']
  for form_item in request.form:
    for cart_item in list_of_cart_items:
      if cart_item['id'] == form_item:
        cart_item['quantity'] = int(request.form[form_item])
        if cart_item['quantity'] == 0:
          list_of_cart_items.remove(cart_item)
  
  session['cart'] = list_of_cart_items
  return redirect('/')
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