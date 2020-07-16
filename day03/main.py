# -*- coding:utf-8 -*-

from flask import Flask
from goods import get_goods
from users import register
from orders import app_orders
from cart import app_cart


app=Flask(__name__)

app.route("/register")(register)
app.route("/get_goods")(get_goods)

# 注册蓝图
#app.register_blueprint(app_orders)

# 在注册蓝图的时候给 url 添加前缀
app.register_blueprint(app_orders,url_prefix="/order")
# /order/get_orders
app.register_blueprint(app_cart,url_prefix="/cart")

@app.route("/")
def index():
    # from goods import get_goods
    # from users import register
    # 循环引用 解决方法 推迟一方的导入 让另一方先完成
    return "index page"


if __name__ == '__main__':
    print(app.url_map)
    # app.run(debug=True,port=8000)
    app.run(debug=True)
    
    
    