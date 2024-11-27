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
    title VARCHAR(200) NOT NULL,  -- 新增字段：帖子标题
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    image VARCHAR(200),  -- 新增字段存储图片路径
    likes_count INTEGER DEFAULT 0,  -- 新增字段存储点赞数
    FOREIGN KEY (user_id) REFERENCES User(id)
);

-- 创建标签表
CREATE TABLE Tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,  -- 标签名称
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)  -- 用户ID，外键关联到用户表
);

-- 创建用户关注表
CREATE TABLE User_Following (
    follower_id INTEGER NOT NULL,  -- 关注者ID
    followed_id INTEGER NOT NULL,  -- 被关注者ID
    PRIMARY KEY (follower_id, followed_id),  -- 复合主键
    FOREIGN KEY (follower_id) REFERENCES User(id),  -- 关注者外键关联到用户表
    FOREIGN KEY (followed_id) REFERENCES User(id)  -- 被关注者外键关联到用户表
);

-- 创建点赞表 (已添加)
CREATE TABLE Post_Likes (
    user_id INTEGER NOT NULL,  -- 点赞用户ID
    post_id INTEGER NOT NULL,  -- 被点赞的帖子ID
    PRIMARY KEY (user_id, post_id),  -- 复合主键
    FOREIGN KEY (user_id) REFERENCES User(id),  -- 点赞用户外键关联到用户表
    FOREIGN KEY (post_id) REFERENCES Post(id)  -- 被点赞的帖子外键关联到帖子表
);

-- 创建评论表
CREATE TABLE Comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 评论ID
    post_id INTEGER NOT NULL,  -- 所属帖子ID
    user_id INTEGER NOT NULL,  -- 评论者用户ID
    content VARCHAR(500) NOT NULL,  -- 评论内容
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 评论时间
    FOREIGN KEY (post_id) REFERENCES Post(id),  -- 外键关联到帖子表
    FOREIGN KEY (user_id) REFERENCES User(id)  -- 外键关联到用户表
);

--考虑可能的拓展，虽然实际内容都是post类还是新开
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