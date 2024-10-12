from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  
db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200))  
    location = db.Column(db.String(100), nullable=True)  
    age = db.Column(db.Integer, nullable=True)  
    interests = db.Column(db.String(200), nullable=True)  
    signature = db.Column(db.String(200), nullable=True)  
    following_count = db.Column(db.Integer, default=0)  
    followers_count = db.Column(db.Integer, default=0)  

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)  

class Tag(db.Model):  # 新增标签模型
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 标签名称
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键关联到用户表

with app.app_context():
    db.create_all()  # 创建所有表

@app.route('/')
def index():
    username = session.get('username')  
    return render_template('index.html', username=username)

@app.route('/user_center', methods=['GET', 'POST'])
def user_center():
    username = session.get('username')  
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        if user:  
            file = request.files.get('avatar')  
            if file:
                filename = secure_filename(file.filename)  
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
                file.save(file_path)  
                user.avatar = f"uploads/{filename}"  
            
            signature = request.form.get('signature')
            if signature:
                user.signature = signature
            
            db.session.commit()  
            flash('资料更新成功！', 'success')
        else:
            flash('请先登录，才能更新资料！', 'error') 

    # 修改后的帖子查询，以确保新发的帖子出现在前
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all() if user else []  

    if user:
        return render_template('user_center.html', 
                               user_avatar=user.avatar or "http://via.placeholder.com/40",
                               user_name=user.username,
                               user_signature=user.signature or "这位用户还没有设置签名。",
                               user_location=user.location or "未知",
                               user_age=user.age or 0,
                               user_interests=user.interests.split(',') if user.interests else [],
                               following_count=user.following_count,
                               followers_count=user.followers_count,
                               user_posts=user_posts)  
    else:
        flash('您尚未登录，请先登录！', 'error')
        return render_template('user_center.html', user_avatar=None, user_name=None)

def get_beijing_time():
    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)  
    return beijing_time

@app.route('/post_message', methods=['POST'])
def post_message():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        content = request.form.get('message')
        if content:
            timestamp = get_beijing_time()  
            new_post = Post(user_id=user.id, content=content, timestamp=timestamp)
            db.session.add(new_post)
            db.session.commit()
            flash('帖子发布成功！', 'success')
        else:
            flash('帖子内容不能为空！', 'error')
    else:
        flash('请先登录，才能发布帖子！', 'error')
    return redirect(url_for('user_center'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    
    if user:
        post = Post.query.get(post_id)
        if post and post.user_id == user.id:
            db.session.delete(post)
            db.session.commit()
            flash('帖子已成功删除！', 'success')
        else:
            flash('无法删除该帖子！', 'error')
    else:
        flash('请先登录，才能删除帖子！', 'error')
    
    return redirect(url_for('user_center'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username  
            flash('登录成功！', 'success')
            return redirect(url_for('user_center'))
        else:
            flash('用户名或密码错误！', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if User.query.filter_by(username=username).first():
            flash('用户已存在！', 'error')
        elif password != confirm_password:
            flash('两次输入的密码不一致！', 'error')
        else:
            new_user = User(username=username, 
                            password=generate_password_hash(password), 
                            avatar="http://example.com/default-avatar.png",  
                            location="未知", 
                            age=0, 
                            interests="",
                            signature="",  
                            following_count=0,
                            followers_count=0)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  
    flash('已成功登出！', 'success')  
    return redirect(url_for('user_center'))  

@app.route('/update_signature', methods=['POST'])
def update_signature():
    username = session.get('username')  
    user = User.query.filter_by(username=username).first()

    if user:
        signature = request.json.get('signature')  # 从请求中获取新的签名
        if signature:
            user.signature = signature  # 更新用户的签名
            db.session.commit()  # 提交更改
            return {'message': '签名更新成功'}, 200  # 返回成功响应
        else:
            return {'message': '缺少签名数据'}, 400  # 返回错误响应
    else:
        return {'message': '用户未登录'}, 401  # 返回未登录错误

@app.route('/update_tags', methods=['POST'])
def update_tags():
    # 确保用户已登录
    username = session.get('username')  
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': '用户未登录'}), 403

    user_id = user.id  # 使用当前用户的 ID
    data = request.get_json()
    
    # 清空当前用户的标签数据（可以选择更新而不是清空）
    Tag.query.filter_by(user_id=user_id).delete()

    # 添加新的标签
    tags = data.get('tags', [])
    for tag_name in tags:
        if tag_name:  # 确保标签不为空
            new_tag = Tag(name=tag_name, user_id=user_id)
            db.session.add(new_tag)

    db.session.commit()  # 提交更改

    return jsonify({'message': '标签更新成功'}), 200

@app.route('/get_user_tags', methods=['GET'])
def get_user_tags():
    username = session.get('username')  
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': '用户未登录'}), 403

    user_id = user.id
    tags = Tag.query.filter_by(user_id=user_id).all()
    tag_names = [tag.name for tag in tags]

    return jsonify({'tags': tag_names}), 200

if __name__ == '__main__':
    app.run(debug=True)
