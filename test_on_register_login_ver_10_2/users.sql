CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    avatar VARCHAR(200),                   -- 头像链接
    location VARCHAR(100),                 -- 用户位置
    age INTEGER,                           -- 年龄
    interests VARCHAR(200)                 -- 兴趣（以逗号分隔）
);