from flask_sqlalchemy import SQLAlchemy   # SQLite数据库 拓展类
from flask import Flask, render_template
from flask import request, url_for, redirect, flash
import os
import click

app = Flask(__name__)


# 创建数据库表
# 方法一：$ flask shell
# >>> from app import db
# >>> db.create_all()   # 创建表
# >>> db.drop_all()     # 删除创建的表
# 方法二：自定义命令initdb
# 可以使用如下两种指令：flask initdb 和 flask initdb --drop
# @app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
# @click.option('--drop', is_flag=True, help='Create after drop.')    # 设置选项
# def initdb(drop):
#     """Initialize the database."""
#     if drop:    # 判断是否输入了选项
#         db.drop_all()
#     db.create_all()
#     click.echo('Initialized database.')     # 输出提示信息


# SQLite的这个变量格式为sqlite:///数据库文件的绝对地址（Windows下三个/，Linux下四个/）
# 数据库文件放在了当前项目的根目录，app.root_path 返回程序实例所在模块的路径（目前来说，即项目根目录）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')

# 兼容性处理
# import sys
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监视
app.config['SECRET_KEY'] = 'dev'    # 为什么要设置这个与flash有关。等同于 app.secret_key = 'dev'，出于安全考虑，这个值应当设置为随机字符，且不应该明文写在代码里
db = SQLAlchemy(app)    # 初始化拓展，传入程序示例app


# 创建数据库模型
class User(db.Model):   # 表名将会是user（自动生成、小写处理）
    id = db.Column(db.Integer, primary_key=True)   # 主键
    name = db.Column(db.String(20))     # 名字


class Movie(db.Model):  # 表名：movie
    id = db.Column(db.Integer, primary_key=True)    # Column的属性除了primary_key以外还有nullable, index, unique, default等
    title = db.Column(db.String(60))    # 电影标题
    year = db.Column(db.String(4))      # 电影年份


# 创建自定义命令forge来生成虚拟数据
@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)    # 把新创建的记录添加到数据库会话
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)    # 把新创建的记录添加到数据库会话
    db.session.commit()
    click.echo('Done.')         # 输出提示信息


# 模块上下文处理函数
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 返回字典，等同于 return {'user' : user}


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


# 默认只接受 GET 请求；需要用methods属性指定同时接受 GET 和 POST 请求。两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存
@app.route('/', methods=['GET', 'POST'])
def index():
    # Flask 会在请求触发后把请求信息放到 request 对象里
    # 因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求的路径（request.path）、请求的方法（request.method）、表单数据（request.form）、查询字符串（request.args）等等
    # request.form 是一个特殊的字典，用表单字段的 name 属性值可以获取用户填入的对应数据
    if request.method == 'POST':
        # 获取数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据，通过在 <input> 元素内添加 required 属性实现的验证（客户端验证）并不完全可靠
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        # 保存表单数据至数据库
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        # flash消息 页面上的提示信息；其中 flash() 函数用来在视图函数里向模板传递提示消息，get_flashed_messages() 函数则用来在模板中获取提示消息
        # flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥

        flash('Item created.')  # 成功创建的提示
        return redirect(url_for('index'))   # 重定向回主页

    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', movies=movies)


# 编辑条目
# <int:movie_id> 部分表示 URL 变量，而 int 则是将变量转换成整型的 URL 变量转换器。在生成这个视图的 URL 时，我们也需要传入对应的变量。
# movie_id 变量是电影条目记录在数据库中的主键值
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)    # 找到记录返回记录，若没找到则返回404错误响应

    if request.method == 'POST':    # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        # 数据更新
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)    # 传入被编辑的电影记录，why? 便于更新数据显示，在模板里，通过表单 <input> 元素的 value 属性即可将它们提前写到输入框里


# 删除条目
# 为了安全的考虑，我们一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))
