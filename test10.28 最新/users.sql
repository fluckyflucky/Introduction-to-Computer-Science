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

CREATE TABLE Resource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- 外键关联用户表
    post_id INTEGER NOT NULL,  -- 外键关联帖子表
    title VARCHAR(200) NOT NULL, -- 文章标题
    cover_image VARCHAR(200), -- 缩略图，封面图片路径
    content TEXT NOT NULL, -- 文章具体内容
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- 文章创建时间
    full_image VARCHAR(200), -- 放大形式的图片路径
    FOREIGN KEY (user_id) REFERENCES User(id), -- 外键关联到用户表
    FOREIGN KEY (post_id) REFERENCES Post(id) -- 外键关联到帖子表
);