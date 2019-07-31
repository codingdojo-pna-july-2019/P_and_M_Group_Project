from config import app
from controller_functions import landing,my_account,view_order,login,view_cart,confirm_order,place_order,add_to_cart
app.add_url_rule("/", view_func=landing)
app.add_url_rule("/my_account", view_func=my_account)
app.add_url_rule("/view_order", view_func=view_order)
app.add_url_rule("/login",view_func=login)
app.add_url_rule("/view_cart",view_func=view_cart)
app.add_url_rule("/confirm_order",view_func=confirm_order)
app.add_url_rule("/place_order",view_func=place_order)
app.add_url_rule("/add_to_cart/<id>",view_func=add_to_cart)