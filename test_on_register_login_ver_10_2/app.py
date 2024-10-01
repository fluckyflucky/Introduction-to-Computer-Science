from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息的密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 数据库配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 创建数据库
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    username = session.get('username')  # 从会话中获取用户名
    return render_template('index.html', username=username)

@app.route('/user_center')
def user_center():
    username = session.get('username')  # 从会话中获取用户名
    return render_template('user_center.html', username=username)  # 直接渲染用户中心模板，不管用户是否登录

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username  # 将用户名存入会话
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户已存在！', 'error')
        elif password != confirm_password:
            flash('两次输入的密码不一致！', 'error')
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除会话中的用户名
    flash('已成功登出！', 'success')  # 登出后设置闪现消息
    return redirect(url_for('user_center'))  # 重定向到用户中心

if __name__ == '__main__':
    app.run(debug=True)
