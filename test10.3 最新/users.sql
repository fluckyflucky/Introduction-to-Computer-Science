-- 创建用户表
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    avatar VARCHAR(200),
    location VARCHAR(100),
    age INTEGER,
    interests VARCHAR(200),
    signature VARCHAR(200),
    following_count INTEGER DEFAULT 0,
    followers_count INTEGER DEFAULT 0
);

-- 创建帖子表
CREATE TABLE Post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content VARCHAR(500) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id)
);
