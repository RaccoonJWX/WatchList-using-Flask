# 错误处理函数
from watchlist import app
from flask import render_template


# 这个函数返回了状态码作为第二个参数，而普通的视图函数返回的是默认的200状态码
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('errors/404.html'), 404  # 返回模块和状态码


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
