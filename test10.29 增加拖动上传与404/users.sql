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
    image VARCHAR(200), -- 新增字段存储图片路径
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- 创建标签表
CREATE TABLE Tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL, -- 标签名称
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) -- 用户ID，外键关联到用户表
);

-- 创建用户关注表
CREATE TABLE User_Following (
    follower_id INTEGER NOT NULL, -- 关注者ID
    followed_id INTEGER NOT NULL, -- 被关注者ID
    PRIMARY KEY (follower_id, followed_id), -- 复合主键
    FOREIGN KEY (follower_id) REFERENCES User(id), -- 关注者外键关联到用户表
    FOREIGN KEY (followed_id) REFERENCES User(id)  -- 被关注者外键关联到用户表
);
