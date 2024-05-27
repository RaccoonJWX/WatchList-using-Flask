# 视图函数
from watchlist import app, db
from flask import request, flash, url_for, render_template, redirect
from flask_login import current_user, login_required, login_user, logout_user
from watchlist.models import Movie, User


@app.route('/', methods=['GET', 'POST'])
def index():
    # Flask 会在请求触发后把请求信息放到 request 对象里
    # 因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求的路径（request.path）、请求的方法（request.method）、表单数据（request.form）、查询字符串（request.args）等等
    # request.form 是一个特殊的字典，用表单字段的 name 属性值可以获取用户填入的对应数据
    if request.method == 'POST':
        # 对创建条目进行认证保护不能直接用login_request，而需要用POST请求中的current_user的is_authenticated属性
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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
@login_required
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
    return render_template('edit.html', movie=movie)


# 删除条目
# 为了安全的考虑，我们一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


# 登出
@app.route('/logout')
@login_required       # 用于视图保护，登录保护，没有登录无法进行很多操作.如果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示一个错误提示
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


# 设置 可修改用户名
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')