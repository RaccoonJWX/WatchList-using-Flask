# 模型类
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):   # 表名将会是user（自动生成、小写处理）
    id = db.Column(db.Integer, primary_key=True)   # 主键
    name = db.Column(db.String(20))     # 名字
    username = db.Column(db.String(20))     # 用户名
    password_hash = db.Column(db.String(128))     # 密码哈希值

    # 生成密码哈希值
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码哈希值
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Book(db.Model):  # 表名：movie
    id = db.Column(db.Integer, primary_key=True)    # Column的属性除了primary_key以外还有nullable, index, unique, default等
    title = db.Column(db.String(60))        # 书的标题
    writer = db.Column(db.String(60))       # 书的作者
    filename = db.Column(db.String(64))
