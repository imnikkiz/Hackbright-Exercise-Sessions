from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    cart = session.get('cart')
    if not cart:
        empty_cart = {
            "No melons": {"qty": 0, "price": 0}
            }
        total = 0
        return render_template("cart.html",
                                cart=empty_cart.iteritems(),
                                total=total)

    return render_template("cart.html", 
                           cart=session['cart'].iteritems(),
                           total=session['total'])

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
# id = melon id from melon_details.html
    melon = model.get_melon_by_id(id)
    cart = session.get('cart', {})


    if melon.common_name in cart:
        cart[melon.common_name]["qty"] +=1
    else:
        cart[melon.common_name]= {"qty":1, "price":melon.price}

    flash("%s was sucessfully added to the cart!" % melon.common_name)

    total = 0
    for melon, info in cart.iteritems():
        total += (info["qty"] * info["price"])

    session['cart'] = cart
    session['total'] = total

    print cart

    return shopping_cart()

@app.route("/login", methods=["GET"])
def show_login():
    if session.get('name'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = model.get_customer_by_email(email)



    if user and password == user.password:
            flash("Welcome "+user.givenname+"! You have successfully logged in.")
            session['name'] = user.givenname

    else:
        flash("Oops, please check you login information again")
        return render_template("login.html")
   


    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return list_melons()


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
