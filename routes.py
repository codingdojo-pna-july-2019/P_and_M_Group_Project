from config import app
from controller_functions import landing,add_dojo,add_ninja,my_account,view_order,login,view_cart,confirm_order,place_order
app.add_url_rule("/", view_func=landing)
app.add_url_rule("/add_dojo", view_func=add_dojo, methods=["POST"])
app.add_url_rule("/add_ninja", view_func=add_ninja,methods=["POST"])
app.add_url_rule("/my_account", view_func=my_account)
app.add_url_rule("/view_order", view_func=view_order)
app.add_url_rule("/login",view_func=login)
app.add_url_rule("/view_cart",view_func=view_cart)
app.add_url_rule("/confirm_order",view_func=confirm_order)
app.add_url_rule("/place_order",view_func=place_order)