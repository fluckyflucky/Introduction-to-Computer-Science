from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL数据库配置
db_config = {
    'user': 'root',        
    'password': 'Fengke20050330',    
    'host': 'localhost',            # 如果MySQL在本地运行
    'database': 'bdh01'               # 数据库名称
}

# 连接数据库
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 注册新用户
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    # 检查用户名是否已经存在
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Username already exists"}), 400

    # 插入新用户
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
