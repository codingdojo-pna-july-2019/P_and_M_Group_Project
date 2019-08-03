from flask import render_template, redirect, request, session, flash, jsonify	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db, bcrypt
from models import User, Order, Product, orders_products_table
import json
import paypalrestsdk
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdQRFW9SyfvciiVeF5oeOWosrOuz1qAdMi0Lguu9rT8MxDya68zQZiQGljosQkIXT9e197qV120VSjre",
  "client_secret": "EL722lqZPZBGY-x85jrjsg1SZGESCHu27HP7pz8754sa5dDLlFNMFehC8BLcMtM1xC6Wf7kIOLhuKv5c" })

def create_payment():

  payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
      "payment_method": "paypal"},
    "redirect_urls": {
      "return_url": "http://localhost:3000/payment/execute", #change these routes
      "cancel_url": "http://localhost:3000/"}, #change these routes
    "transactions": [{
      "item_list": {
          "items": [{
            "name": "item", #change item to items from the cart
            "sku": "item",
            "price": session['cart_total'], #change price to the prices of our items
            "currency": "USD", #leave this
            "quantity": 1}]}, #change quantities to match what's in the cart
      "amount": {
        "total": session['cart_total'],
        "currency": "USD"},
      "description": "This is the payment transaction description."}]})
  if payment.create():
    print('payment success')
  else:
    print(payment.error)

  return jsonify({'paymentID':payment.id})

def execute_payment():
  success = False
  payment = paypalrestsdk.Payment.find(request.form['paymentID'])

  if payment.execute({'payer_id': request.form['payerID']}):
    print("execute success")
    success = True
  else:
    print(payment.error)

  return jsonify({'success':success})


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

def logout():
  session.clear()
  return redirect('/')

def login_register():
  return render_template('/registration.html')

def login():
  is_valid=True
  #get form info
  form_email = request.form['email'].lower()

  if len(request.form['password'])<1:
    flash('Password cannot be blank.')
    is_valid = False
  if len(form_email)<1:
    flash('Email cannot be blank.')
    is_valid = False
  if is_valid == True:
    #see if user is already registered
    instance_of_user = User.query.filter_by(email=form_email).first()
    print(instance_of_user)
    
    if instance_of_user is None:
      flash('Email does not match a registered user')
      return redirect('/login_register')
    else:#check if password matches
      if bcrypt.check_password_hash(instance_of_user.pw,request.form['password']) == True:
        print('password matched')
        session['user_email'] = form_email
        session['first_name'] = instance_of_user.f_name
        session['id'] = instance_of_user.id
        return redirect('/my_account')
      else:
        flash('Password or email is incorrect.')
        return redirect('/login_register')
  return redirect('/')

def register():
  is_valid=True
  #get form info
  fn = request.form['first_name']
  ln = request.form['last_name']
  pw = request.form['password']
  cpw = request.form['confirm_password']
  form_email = request.form['email'].lower()

  if len(fn)<1:
    flash('First Name must be filled in.')
    is_valid = False
  if len(ln)<1:
    flash('Last Name must be filled in.')
    is_valid = False
  if is_valid == True:
    #check if email is registered
    instance_of_user = User.query.filter_by(email=form_email).first()
    print(instance_of_user)
    
    if instance_of_user is not None:
      flash('Email already registered. Please login.')
      return redirect('/login')
    
    #if email not registered, add the user to the db
    pw_hash = bcrypt.generate_password_hash(pw)
    flash('Successfully added new user!')

    new_instance_of_a_user = User(f_name=fn, l_name=ln, email=form_email, pw=pw_hash)
    db.session.add(new_instance_of_a_user)
    db.session.commit()
    session['user_email'] = form_email
    session['first_name'] = fn
    instance_of_user = User.query.filter_by(email=form_email).first()
    session['id'] = instance_of_user.id
  return redirect('/my_account')

def my_account():
  return render_template('myaccount.html')

def view_order():
  return render_template('view_order.html')

def view_cart():
  return render_template('view_cart.html')

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
    'img_file':instance_of_product.img_file,
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

def update_cart_checkout():
  #do the same thing as update_cart() but redirect to the place order page
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

  #get the cart total
  if 'cart' in session:    
    session['cart_total'] = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    for item in session['cart']:
      session['cart_total'] += item['quantity'] * item['unit_cost']

  return redirect('/view_cart')

def update_cart_and_shipping_checkout():
  return redirect('/place_order')

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