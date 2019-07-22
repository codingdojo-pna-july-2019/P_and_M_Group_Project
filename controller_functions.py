from flask import render_template, redirect, request	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db
from models import Dojos,Ninjas

def landing():
  return render_template('landing.html')

def add_dojo():
  #print(request.form)
  instance_of_dojo = Dojos(
    name=request.form['dojo_name'], 
    city=request.form['dojo_city'], 
    state = request.form['dojo_state']
    )
  print(type(instance_of_dojo))
  #print(instance_of_dojo)
  db.session.add(instance_of_dojo)
  db.session.commit()
  #all_dojos = Dojos.query.all()
  #print(all_dojos)
  return redirect('/')

def add_ninja():
  #print(request.form)
  instance_of_ninja = Ninjas(
    first_name=request.form['first_name'], 
    last_name=request.form['last_name'], 
    dojo_id = request.form['dojo']
    )
  #print(type(instance_of_ninja))
  #print(instance_of_ninja)
  db.session.add(instance_of_ninja)
  db.session.commit()
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