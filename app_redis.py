from flask import Flask, render_template, request, url_for, redirect, session
import pymysql
from datetime import datetime
import redis

app = Flask(__name__)

# 创建 Redis 连接
r = redis.Redis(host='localhost', port=6379, db=0)

# 设置键值对
r.set('name', 'John')

# 获取值
name = r.get('name')
print(name, name.decode('utf-8'))  # 将字节转换为字符串

# 列表操作
r.lpush('fruits', 'apple')
r.lpush('fruits', 'banana')
fruits = r.lrange('fruits', 0, -1)
print([fruit.decode('utf-8') for fruit in fruits])

if __name__ == '__main__':
    app.run(debug=True, port=5000)