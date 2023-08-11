from flask import Flask, render_template, request, url_for, redirect, session
import pymysql
from datetime import datetime
import redis
from updateRedis import get_top10_clicks

app = Flask(__name__)

# 创建 Redis 连接
r = redis.Redis(host='localhost', port=6379, db=1)

@app.route('/rankings')
def rankings():
    rankings = get_top10_clicks()
    return render_template('rankings.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)