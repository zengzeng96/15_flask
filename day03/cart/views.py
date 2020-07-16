# -*- coding:utf-8 -*-

from flask import render_template

from . import app_cart

# .  就表示当前的这个包

@app_cart.route("/get_cart")
def get_cart():
    return render_template("cart.html")