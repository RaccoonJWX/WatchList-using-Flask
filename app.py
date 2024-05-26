from flask_sqlalchemy import SQLAlchemy   # SQLite数据库 拓展类
from flask import Flask, render_template
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


@app.route('/')
def index():
    user = User.query.first()   # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user,movies=movies)
