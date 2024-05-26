from flask import Flask
from markupsafe import escape
from flask import url_for

# Flask程序初始化
app = Flask(__name__)


# 注册一个处理函数，处理某个请求的处理函数，又叫视图函数
# 修饰器app.route()为这个函数绑定对应的url，当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口
# / 是指根地址，只需要写相对地址，主机名后面的路径部分
# 一个视图函数可以绑定多个URL
# @app.route('/home')
@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'


@app.route('/home')
def home():
    return '<h1>Home Page</h1>'


# 路由可以有一部分为动态名字
@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello, {escape(name)}!</h1>'


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('home'))
    print(url_for('user', name='Alice'))
    print(url_for('user', name='Bob'))
    return 'Test page'


# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
