from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息的密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 数据库配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 上传文件保存路径
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传文件大小为16MB
db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200))  # 头像链接
    location = db.Column(db.String(100), nullable=True)  # 用户位置
    age = db.Column(db.Integer, nullable=True)  # 年龄
    interests = db.Column(db.String(200), nullable=True)  # 兴趣（以逗号分隔）

# 创建数据库
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    username = session.get('username')  # 从会话中获取用户名
    return render_template('index.html', username=username)

@app.route('/user_center', methods=['GET', 'POST'])
def user_center():
    username = session.get('username')  # 获取会话中的用户名
    user = User.query.filter_by(username=username).first()
    
    if request.method == 'POST':
        if user:  # 只有在用户存在时才处理上传
            file = request.files.get('avatar')  # 获取上传的文件
            if file:
                filename = secure_filename(file.filename)  # 安全获取文件名
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 文件保存路径
                file.save(file_path)  # 保存文件
                user.avatar = f"uploads/{filename}"  # 更新用户头像链接
                db.session.commit()  # 提交更改
                flash('头像更新成功！', 'success')
            else:
                flash('请上传有效的文件！', 'error')
        else:
            flash('请先登录，才能更新头像！', 'error')  # 用户未登录时的提示

    if user:
        return render_template('user_center.html', 
                               user_avatar=user.avatar or "http://via.placeholder.com/40",
                               user_name=user.username,
                               user_location=user.location or "未知",
                               user_age=user.age or 0,
                               user_interests=user.interests.split(',') if user.interests else [])
    else:
        flash('您尚未登录，请先登录！', 'error')
        return render_template('user_center.html', user_avatar=None, user_name=None)

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
            new_user = User(username=username, 
                            password=generate_password_hash(password), 
                            avatar="http://example.com/default-avatar.png",  # 默认头像链接
                            location="未知", 
                            age=0, 
                            interests="")
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除会话中的用户名
    flash('已成功登出！', 'success')  # 登出后设置闪现消息
    return redirect(url_for('index'))  # 重定向到首页

if __name__ == '__main__':
    app.run(debug=True)
