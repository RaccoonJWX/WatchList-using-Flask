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


# 命令行创建管理员账户
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
