from flask import render_template, redirect, request, session, flash, jsonify	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db, bcrypt
from models import User, Order, Product, Shipping, orders_products_table
import json, os, paypalrestsdk

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdQRFW9SyfvciiVeF5oeOWosrOuz1qAdMi0Lguu9rT8MxDya68zQZiQGljosQkIXT9e197qV120VSjre",
  "client_secret": "EL722lqZPZBGY-x85jrjsg1SZGESCHu27HP7pz8754sa5dDLlFNMFehC8BLcMtM1xC6Wf7kIOLhuKv5c" })

def update_cart_function():
  list_of_cart_items = session['cart']
  for form_item in request.form:
    for cart_item in list_of_cart_items:
      if cart_item['id'] == form_item:
        cart_item['quantity'] = int(request.form[form_item])
        if cart_item['quantity'] == 0:
          list_of_cart_items.remove(cart_item)

  session['cart'] = list_of_cart_items
  #no return needed

def cart_total():
  #get the cart total
  if 'cart' in session:    
    session['cart_total'] = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    for item in session['cart']:
      session['cart_total'] += item['quantity'] * item['unit_cost']
  #no return needed

def success():
  if 'cart' in session:
    session.pop('cart')
    session.pop('cart_total')
  return render_template('success.html')

def create_payment():
  #create a new order
  paypal_items = []
  paypal_item = {}
  for item in session['cart']:
    paypal_item = {"name":item['name'],"sku":item['id'],"price":item['unit_cost'],"currency":"USD","quantity":item['quantity']}
    paypal_items.append(paypal_item)

  payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
      "payment_method": "paypal"},
    "redirect_urls": {
      "return_url": "http://localhost/success", #change these routes
      "cancel_url": "http://localhost/place_order"}, #change these routes
    "transactions": [{
      "item_list": {"items": paypal_items}, #change quantities to match what's in the cart
      "amount": {
        "total": session['cart_total'],
        "currency": "USD"},
      "description": "This is the payment transaction description."}]})
  if payment.create():
    print('payment success')
    for link in payment.links:
      if link.method=="REDIRECT":
        redirect_url = (link.href)
  else:
    print(payment.error)

  return jsonify({'paymentID':payment.id})

def execute_payment():
  success = False
  payment = paypalrestsdk.Payment.find(request.form['paymentID'])

  if payment.execute({'payer_id': request.form['payerID']}):
    print("execute success")
    success = True
    #commit order to the DB

  else:
    print(payment.error)
    flash('There was an error when placing payment')
    return redirect('/place_order')

  return jsonify({'success':success})

def landing():
  #select all the products and display them on the page
  list_of_all_products = Product.query.all() 
  cart_total() #call the cart_total function
  return render_template('landing.html',all_products = list_of_all_products)

def clear_session():
  session.clear()
  return redirect('/')

def logout():
  session.clear()
  return redirect('/')

def login_register(flag=0): #flag = 1 if the user is trying to place an order. otherwise flag is 0
  print(flag)
  if flag == '1':
    flash('Please login to continue')

  return render_template('/registration.html',flag=flag)

def login(flag=0):#flag = 1 if the user is trying to place an order. otherwise flag is 0
  print(flag) #flag = 1 if the user is trying to place an order. otherwise flag is 0
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
    
    if instance_of_user is None:
      flash('Email does not match a registered user')
      return redirect('/login_register/'+str(flag))
    else:#check if password matches
      if bcrypt.check_password_hash(instance_of_user.pw,request.form['password']) == True:
        print('password matched')
        session['user_email'] = form_email
        session['first_name'] = instance_of_user.f_name
        session['id'] = instance_of_user.id
        if flag=='1':
          return redirect('/place_order')
        return redirect('/my_account')
      else:
        flash('Password or email is incorrect.')
        return redirect('/login_register/'+str(flag))
  return redirect('/')

def register(flag=0): #flag = 1 if the user is trying to place an order. otherwise flag is 0
  print(flag)
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
      return redirect('/login_register/'+str(flag))
    
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
    if flag=='1':
      return redirect('/place_order')
  return redirect('/my_account')

def my_account():
  return render_template('myaccount.html')

def view_order():
  return render_template('view_order.html')

def view_cart():
  return render_template('view_cart.html')

def place_order():
  if 'id' not in session:
    return redirect('/login_register/1')
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
  cart_total() #call the cart_total function
  return redirect('/#yoga-products')

def update_cart():
  update_cart_function() #call the update_cart_function
  cart_total() #call the cart_total function
  return redirect('/')

def update_cart_checkout():
  #do the same thing as update_cart() but redirect to the view cart page
  update_cart_function() #call the update_cart_function
  cart_total() #call the cart_total function
  return redirect('/view_cart')


def update_cart_and_shipping_checkout():
  update_cart_function() #call the update_cart_function
  cart_total() #call the cart_total function

  #validate the shipping information and add it to the DB
  session['shipping_address'] = request.form['address']
  print(session['shipping_address'])

  #should probably check if the shipping already exists before commiting it
  instance_of_shippings = Shipping.query.filter_by(address=session['shipping_address'], first_name=session['shipping_fn'], last_name=session['shipping_ln']).first()
  print(instance_of_shippings)

  if instance_of_shippings is None:
    print('instance of shippings was none')
    #add the shipping address to the DB
    new_shipping_instance = Shipping(first_name=session['shipping_fn'], last_name=session['shipping_ln'], address=session['shipping_address'])
    db.session.add(new_shipping_instance)
    db.session.commit()

  return redirect('/place_order')

def address_validation():

  found = True
  # We recommend storing your secret keys in environment variables instead---it's safer!
  auth_id = os.environ['SMARTY_AUTH_ID']
  auth_token = os.environ['SMARTY_AUTH_TOKEN']
  session['shipping_fn'] = request.form['first_name']
  session['shipping_ln'] = request.form['last_name']
  input_address = {
    'street':request.form['street1']+' '+request.form['street2'],
    'city':request.form['city'],
    'state':request.form['state'],
    'zip':request.form['zip_code']
  }

  credentials = StaticCredentials(auth_id, auth_token)

  client = ClientBuilder(credentials).build_us_street_api_client()
  # client = ClientBuilder(credentials).with_custom_header({'User-Agent': 'smartystreets (python@0.0.0)', 'Content-Type': 'application/json'}).build_us_street_api_client()
  # client = ClientBuilder(credentials).with_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
  # Uncomment the line above to try it with a proxy instead

  # Documentation for input fields can be found at:
  # https://smartystreets.com/docs/us-street-api#input-fields

  lookup = Lookup()
  #lookup.input_id = "24601"  # Optional ID from your system
  lookup.addressee = request.form['first_name']+' '+request.form['last_name']
  lookup.street = request.form['street1']
  lookup.street2 = request.form['street2']
  #lookup.secondary = "APT 2"
  lookup.urbanization = ""  # Only applies to Puerto Rico addresses
  lookup.city = request.form['city']
  lookup.state = request.form['state']
  lookup.zipcode = request.form['zip_code']
  lookup.candidates = 3
  lookup.match = "Invalid"  # "invalid" is the most permissive match

  try:
    client.send_lookup(lookup)
  except exceptions.SmartyException as err:
    print(err)
    return

  result = lookup.result

  if not result:
    found = False
    print("No candidates. This means the address is not valid.")
    flash('Address is not valid. Please re-enter shipping information.')
    return render_template('partials/address.html', found=found)

  #for output example fields here https://smartystreets.com/docs/cloud/us-street-api#http-response-status
  first_candidate = result[0]

  print("Address is valid. (There is at least one candidate)\n")
  suggested_address_line1 = first_candidate.delivery_line_1
  suggested_address_line2 = first_candidate.components.city_name+", "+first_candidate.components.state_abbreviation+" "+first_candidate.components.zipcode
  print(first_candidate.delivery_line_1)
  print(suggested_address_line1)
  print(first_candidate.components.city_name+", "+first_candidate.components.state_abbreviation+" "+first_candidate.components.zipcode)
  return render_template('partials/address.html', found=found,suggested_address_line1=suggested_address_line1,suggested_address_line2=suggested_address_line2,input_address=input_address)
