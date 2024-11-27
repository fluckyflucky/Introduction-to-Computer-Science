
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  
db = SQLAlchemy(app)

# 用户模型
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 关注者ID
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 被关注者ID

    follower = db.relationship('User', foreign_keys=[follower_id])
    followed = db.relationship('User', foreign_keys=[followed_id])

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
    title = db.Column(db.String(200), nullable=False)  # 新增字段：帖子标题
    content = db.Column(db.Text, nullable=False)  # 使用 TEXT 类型以支持长内容
    timestamp = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(200))  # 存储图片路径
    likes_count = db.Column(db.Integer, default=0)  # 存储点赞数量


class Tag(db.Model):  # 新增标签模型
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 标签名称
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键关联到用户表

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # 帖子ID

    user = db.relationship('User', backref='likes')
    post = db.relationship('Post', backref='likes')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 评论的唯一标识符
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 评论用户ID
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # 评论关联的帖子ID
    content = db.Column(db.String(500), nullable=False)  # 评论内容
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 评论时间戳

    user = db.relationship('User', backref='comments')  # 评论所属用户
    post = db.relationship('Post', backref='comments')  # 评论所属帖子

    # 创建所有表
with app.app_context():
    db.create_all()  # 创建所有表


@app.route('/')
def index():
    username = session.get('username')  
    return render_template('index.html', username=username)

@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return '未登录', 401

    post = Post.query.get(post_id)
    if not post:
        return '帖子不存在', 404  

    existing_like = Like.query.filter_by(user_id=user.id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        post.likes_count -= 1  # 点赞取消，减少点赞数
    else:
        new_like = Like(user_id=user.id, post_id=post_id)
        db.session.add(new_like)
        post.likes_count += 1  # 点赞，增加点赞数
        
    
    db.session.commit()
    return redirect(url_for('user_profile', user_id=post.user_id))





@app.route('/user_center', methods=['GET', 'POST'])
def user_center():
    username = session.get('username')  
    if not username:
        flash('您尚未登录，请先登录！', 'info')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=username).first()
    
    if not user:  # 检查用户是否存在
        flash('用户不存在，请重新登录！', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files.get('avatar')  
        if file:  # 检查文件是否存在
            filename = secure_filename(file.filename)  
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
            file.save(file_path)  
            user.avatar = f"uploads/{filename}"  # 更新用户头像路径

        signature = request.form.get('signature')
        if signature:
            user.signature = signature

        db.session.commit()  
        flash('资料更新成功！', 'success')  

    # 获取用户的帖子
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    
    # 获取用户已点赞的帖子 ID
    liked_posts_ids = [like.post_id for like in Like.query.filter_by(user_id=user.id).all()]

    # 创建 current_user 变量
    current_user = user  
    return render_template('user_center.html',
                           user=user,
                           user_id=user.id,
                           current_user=current_user,
                           user_avatar=user.avatar or "http://via.placeholder.com/40",
                           user_name=user.username,
                           user_signature=user.signature or "这位用户还没有设置签名。",
                           user_location=user.location or "未知",
                           user_age=user.age or 0,
                           user_interests=user.interests.split(',') if user.interests else [],
                           following_count=user.following_count,
                           followers_count=user.followers_count,
                           user_posts=user_posts,
                           liked_posts_ids=liked_posts_ids)  # 传递已点赞的帖子 ID 列表




@app.route('/search_user/<username>')
def search_user(username):
    user = User.query.filter_by(username=username).first()  # 根据用户名查询用户
    if user:
        # 跳转到用户个人主页，使用包含用户 ID 的路径
        return redirect(url_for('user_profile', user_id=user.id))  
    else:
        flash('用户不存在！', 'error')
        return render_template('404.html')  # 返回到404或其他合适的页面



@app.route('/user/<int:user_id>', methods=['GET', 'POST'])  # 添加 POST 方法
def user_profile(user_id):
    user = User.query.get(user_id)
    current_username = session.get('username')
    current_user = User.query.filter_by(username=current_username).first() if current_username else None

    if user:
        if request.method == 'POST':  # 处理头像上传
            file = request.files.get('avatar')
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                user.avatar = f"uploads/{filename}"  # 更新头像路径
                db.session.commit()
                flash('头像上传成功！', 'success')
            else:
                flash('请选择文件！', 'error')

        # 获取用户标签
        user_tags = Tag.query.filter_by(user_id=user.id).all()
        user_tag_names = [tag.name for tag in user_tags]

        # 获取用户帖子的列表
        user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()

        # 检查是否正在关注该用户
        is_following = Follow.query.filter_by(follower_id=current_user.id, followed_id=user.id).first() is not None
        
        # 获取当前用户已点赞的帖子 ID
        liked_posts_ids = [like.post_id for like in Like.query.filter_by(user_id=current_user.id).all()] if current_user else []

        return render_template('user_center.html',
                               user=user,
                               user_id=user.id,
                               user_avatar=user.avatar or "http://via.placeholder.com/40",
                               user_name=user.username,
                               user_signature=user.signature or "这位用户还没有设置签名。",
                               user_location=user.location or "未知",
                               user_age=user.age or 0,
                               user_interests=user.interests.split(',') if user.interests else [],
                               following_count=user.following_count,
                               followers_count=user.followers_count,
                               user_posts=user_posts,
                               current_user=current_user,
                               user_tags=user_tag_names,
                               is_following=is_following,
                               liked_posts_ids=liked_posts_ids)  # 传递已点赞的帖子 ID 列表
    else:
        flash('用户不存在！', 'error')
        return render_template('404.html')







def get_beijing_time():
    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)  
    return beijing_time

@app.route('/post_message', methods=['POST'])
def post_message():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    
    if user:
        # 获取标题和内容
        title = request.form.get('title')  # 从表单获取标题
        content = request.form.get('message')  # 从表单获取内容
        file = request.files.get('image')  # 获取上传的图片
        image_path = None

        # 处理图片上传
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            image_path = f"uploads/{filename}"  # 保存相对路径
        
        if title and content:  # 确保标题和内容都不为空
            timestamp = get_beijing_time()  
            new_post = Post(user_id=user.id, title=title, content=content, timestamp=timestamp, image=image_path)  # 保存标题和内容
            db.session.add(new_post)
            db.session.commit()
            flash('帖子发布成功！', 'success')
        else:
            flash('标题和内容不能为空！', 'error')
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
            # 删除与该帖子相关的所有评论
            comments_to_delete = Comment.query.filter_by(post_id=post_id).all()
            for comment in comments_to_delete:
                db.session.delete(comment)  # 删除每一个评论
                
            # 删除与该帖子相关的所有点赞记录
            likes_to_delete = Like.query.filter_by(post_id=post_id).all()
            for like in likes_to_delete:
                db.session.delete(like)  # 删除每一个点赞记录
            
            db.session.delete(post)  # 删除帖子
            db.session.commit()  # 提交更改
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
            session['username'] = username  # 将用户名存储在会话中
            flash('登录成功！', 'success')

            # 登录成功后，重定向到包含用户 ID 的个人主页 URL
            return redirect(url_for('user_profile', user_id=user.id))  # 这里更新为 user_profile

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
            # 生成五位数ID
            max_id = db.session.query(db.func.max(User.id)).scalar()  # 获取当前最大用户ID
            new_user_id = 10000  # 初始ID

            if max_id is not None:
                new_user_id = max(max_id + 1, 10000)  # 确保新ID不小于10000

            new_user = User(id=new_user_id,  # 设置新用户的ID
                            username=username, 
                            password=generate_password_hash(password), 
                            avatar="http://example.com/default-avatar.png",  #这里不改我会报错
                            location="未知", 
                            age=0, 
                            interests="",
                            signature="",  
                            following_count=0,
                            followers_count=0)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))  # 修改为重定向到登录页面

    return render_template('user_center.html')


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
    username = session.get('username')  
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': '用户未登录'}), 403

    user_id = user.id  # 使用当前用户的 ID
    data = request.get_json()
    
    Tag.query.filter_by(user_id=user_id).delete()  # 清空当前用户的标签

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


# 获取用户的关注者
def get_followers_from_db(user_id):
    # 获取所有的关注者
    followers = Follow.query.filter_by(followed_id=user_id).all()
    follower_users = [User.query.get(f.follower_id) for f in followers if User.query.get(f.follower_id)]  # 获取对应的用户对象
    return follower_users  # 返回用户对象列表

# 获取用户关注的对象
def get_following_from_db(user_id):
    # 获取所有的关注用户
    following = Follow.query.filter_by(follower_id=user_id).all()
    following_users = [User.query.get(f.followed_id) for f in following if User.query.get(f.followed_id)]  # 获取对应的用户对象
    return following_users  # 返回用户对象列表

@app.route('/get_followers')
def get_followers():
    user_id = request.args.get('user_id')  # 通过请求参数获取用户ID
    followers = get_followers_from_db(user_id)  # 获取关注者

    # 返回包含头像和用户名的列表
    return jsonify({
        'followers': [
            {
                'username': follower.username,
                'avatar': url_for('static', filename=follower.avatar) if follower.avatar else 'http://via.placeholder.com/40'
            }
            for follower in followers
        ]
    })

@app.route('/get_following')
def get_following():
    user_id = request.args.get('user_id')  # 通过请求参数获取用户ID
    following = get_following_from_db(user_id)  # 获取关注用户

    # 返回包含头像和用户名的列表
    return jsonify({
        'following': [
            {
                'username': follow.username,
                'avatar': url_for('static', filename=follow.avatar) if follow.avatar else 'http://via.placeholder.com/40'
            }
            for follow in following
        ]
    })



@app.route('/toggle_follow', methods=['POST'])
def toggle_follow():
    data = request.get_json()
    follower_id = data.get('follower_id')
    followed_id = data.get('followed_id')

    # 查询用户
    with db.session.no_autoflush:  # 使用上下文管理
        follower = db.session.get(User, follower_id)
        followed = db.session.get(User, followed_id)

    if follower is None or followed is None:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    is_following=False
    # 检查是否已经关注
    existing_follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()

    if existing_follow:
        # 如果已经关注，则删除关注
        db.session.delete(existing_follow)
        # 更新关注和粉丝数量
        follower.following_count -= 1
        followed.followers_count -= 1
        new_follow_status = "关注"  # 更新按钮文本
        is_following=False
    else:
        # 如果未关注，则添加关注
        new_follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.session.add(new_follow)
        # 更新关注和粉丝数量
        follower.following_count += 1
        followed.followers_count += 1
        new_follow_status = "已关注"  # 更新按钮文本
        is_following=True
    # 提交更改
    db.session.commit()

    return jsonify({'success': True, 'new_follow_status': new_follow_status,'is_following': is_following })





#这里是查询resource获得信息的函数
@app.route('/get_resources')
def get_resources():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    current_user_id = user.id if user else None

    posts = db.session.query(
        Post.id,
        Post.content,
        Post.image,
        Post.timestamp,
        User.username,
        User.id.label('user_id'),
        User.avatar
    ).join(User, Post.user_id == User.id)

    post_info = []
    for post in posts:
        # 检查当前用户是否关注了帖子作者
        is_following = False
        if current_user_id:
            is_following = db.session.query(Follow).filter_by(
                follower_id=current_user_id,
                followed_id=post.user_id
            ).first() is not None

        post_info.append({
            'id': post.id,
            'content': post.content,
            'image_path': url_for('static', filename=f'{post.image}') if post.image else None,
            'timestamp': post.timestamp,
            'author': post.username,
            'user_id': post.user_id,
            'avatar': url_for('static', filename=f'{post.avatar}') if post.avatar else url_for('static', filename='default-avatar.png'),
            'is_liked': db.session.query(Like).filter_by(user_id=current_user_id, post_id=post.id).first() is not None if current_user_id else False,
            'is_following': is_following  # 返回用户关注状态
        })

    return jsonify(post_info)

@app.route('/is_logged_in')
def is_logged_in():
    username = session.get('username')
    
    if username:
        # 查询数据库中的用户
        user = User.query.filter_by(username=username).first()
        
        if user:
            # 返回当前登录用户的 ID
            return jsonify({'logged_in': True, 'user_id': user.id})
        else:
            return jsonify({'logged_in': False})
    else:
        return jsonify({'logged_in': False})
    

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content')

    if not post_id or not content:
        return jsonify({'success': False, 'message': '缺少必要参数'})

    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': '用户未登录'})

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'})

    new_comment = Comment(user_id=user.id, post_id=post_id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'success': True, 'message': '评论提交成功'})


@app.route('/get_comments', methods=['GET'])
def get_comments():
    post_id = request.args.get('post_id')  # 获取请求参数
    if not post_id:
        return jsonify({'error': 'post_id is required'}), 400

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    comment_data = [
        {
            'id': comment.id,
            'username': comment.user.username,
            'content': comment.content,
            'user_id':comment.user_id,
            'timestamp': comment.timestamp,
            'avatar': url_for('static', filename=comment.user.avatar) if comment.user.avatar else 'http://via.placeholder.com/40'
        }
        for comment in comments
    ]
    return jsonify({'comments': comment_data})

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    username = session.get('username')
    if not username:
        # 用户未登录，返回错误信息
        return jsonify({'success': False, 'message': '请先登录，才能删除评论！'}), 401

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': '用户信息不存在！'}), 404

    comment = Comment.query.get(comment_id)
    if not comment:
        # 评论不存在
        return jsonify({'success': False, 'message': '评论不存在！'}), 404

    # 只有评论的作者才能删除评论
    if comment.user_id != user.id:
        return jsonify({'success': False, 'message': '只能删除自己的评论！'}), 403

    # 删除评论
    db.session.delete(comment)
    db.session.commit()

    return jsonify({'success': True, 'message': '评论已删除！'}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def user_profile_view(user_id):  # 改成 user_profile_view
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    comments_for_posts = {}

    # 获取每个帖子的评论
    for post in posts:
        comments_for_posts[post.id] = Comment.query.filter_by(post_id=post.id).all()

    return render_template('user_profile.html', user=user, posts=posts, comments_for_posts=comments_for_posts)

if __name__ == '__main__':
    app.run(debug=True)


