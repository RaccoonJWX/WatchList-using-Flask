# 命令函数
import click
from watchlist import app, db
from watchlist.models import User, Book


@app.cli.command()  # 注册为命令，可以传入name参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')    # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:    # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')     # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    name = 'Raccoon'
    books = [
        {'title': '窗边的小豆豆', 'writer': '黑柳彻子'},
        {'title': '秋园', 'writer': '杨本芬'},
        {'title': '鼠疫', 'writer': '阿尔贝·加缪'},
        {'title': '我的天才女友', 'writer': '埃莱娜·费兰特'},
        {'title': '一个叫欧维的男人决定去死', 'writer': '弗雷德里克·巴克曼'},
        {'title': '失踪的孩子', 'writer': '埃莱娜·费兰特'},
    ]
    user = User(name=name)
    db.session.add(user)    # 把新创建的记录添加到数据库会话
    for m in books:
        book = Book(title=m['title'], writer=m['writer'])
        db.session.add(book)    # 把新创建的记录添加到数据库会话
    db.session.commit()
    click.echo('Done.')         # 输出提示信息


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
