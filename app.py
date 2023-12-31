from flask import Flask, render_template, request, url_for, redirect, session
import pymysql
from datetime import datetime
import redis
import json
# Set the secret key to some random bytes. Keep this really secret!

app = Flask(__name__)

db_info = dict(
    host='localhost',
    user='zpc',
    password='zpjzpc',
    database='secondary_hand_trading_sys',
    autocommit=True,
    )

db = pymysql.connect(**db_info)

def getBookMetaData(bookname):
    cursor = db.cursor()
    sql = 'SELECT * FROM Book WHERE bookname=%s'
    cursor.execute(sql, bookname)
    metaData = cursor.fetchone()
    return metaData

@app.route('/getBookRequest', methods=['POST'])
def getBookRequest():
    bookname = request.form['bookname']
    cursor = db.cursor()
    sql = 'SELECT request FROM Book WHERE bookname=%s'
    cursor.execute(sql, bookname)
    requested = cursor.fetchone()
    return {'requested': requested}

def saveMessage():
    cursor = db.cursor()
    sql = 'INSERT INTO Message(sender, action, bookname, receiver) VALUES(%s, %s, %s, %s)'
    cursor.execute(sql, (sender, action, bookname, receiver))

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        print(request.form)
        return 'ok'
    return render_template('test.html')

# login. redirect to user's home page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         cursor = db.cursor()
#         sql = 'SELECT username FROM User WHERE username=%s AND password=%s'
#         cursor.execute(sql,(username, password))
#         res = cursor.fetchone()
#         if res:
#             session['username'] = res[0]
#             return redirect(url_for('book_status'))
#         return 'login failed'
#     return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    cursor = db.cursor()
    sql = 'SELECT username FROM User WHERE username=%s AND password=%s'
    cursor.execute(sql,(username, password))
    res = cursor.fetchone()
    print(res)
    if res:
        return {'status':'success', 'username':username}
    return {'status':'failed'}
    

# @app.route('/book_status')
# def book_status():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     username = session['username']
#     cursor = db.cursor()
#     sql = 'SELECT * FROM Book WHERE username=%s OR loaned_to=%s'
#     cursor.execute(sql, (username, username))
#     books = cursor.fetchall()
#     return render_template('book_status.html', books=books, owner=username)

@app.route('/book_status', methods=['POST'])
def book_status():
    username = request.form['username']
    cursor = db.cursor()
    sql = 'SELECT * FROM Book WHERE username=%s OR loaned_to=%s'
    cursor.execute(sql, (username, username))
    books = cursor.fetchall()
    books = [{'bookname':book[0], 'username':book[1], 'request':book[2], 'loaned_to':book[3]} for book in books]
    return json.dumps(books)

@app.route('/deleteBook', methods=['POST'])
def deleteBook():
    bookname = request.form['bookname']
    cursor = db.cursor()
    sql = 'DELETE FROM Book WHERE bookname=%s'
    cursor.execute(sql, bookname)
    return {'status':'ok'}

@app.route('/addBook', methods=['POST'])
def addBook():
    username, bookname = request.form['username'], request.form['bookname']
    cursor = db.cursor()
    sql = 'INSERT INTO Book(bookname, username, loaned_to) VALUES(%s, %s, NULL)'
    cursor.execute(sql, (bookname, username))
    return {'status':'ok'}

@app.route('/trading_square')
def trading_square():
    cursor = db.cursor()
    sql = 'SELECT * FROM Book'
    cursor.execute(sql)
    books = cursor.fetchall()
    # print(books)
    # print(json.dumps(books))
    return json.dumps(books)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor = db.cursor()
    sql = f"SELECT * FROM Book WHERE bookname like '%{keyword}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return json.dumps(results)

@app.route('/borrowBook', methods=['POST'])
def borrowBook():
    username, bookname = request.form['username'], request.form['bookname']
    cursor = db.cursor()
    sql = 'UPDATE Book SET request=%s WHERE bookname=%s'
    cursor.execute(sql, (username, bookname))
    return {'status':'ok'}

@app.route('/returnBook', methods=['POST'])
def returnBook():
    bookname = request.form['bookname']
    cursor = db.cursor()
    sql = 'UPDATE Book SET loaned_to=NULL WHERE bookname=%s'
    cursor.execute(sql, bookname)
    return {'status':'ok'}

@app.route('/allowRequest', methods=['POST'])
def allowRequest():
    bookname = request.form['bookname']
    cursor = db.cursor()
    sql = 'UPDATE Book SET loaned_to=request, request=NULL WHERE bookname=%s'
    cursor.execute(sql, bookname)
    return {'status':'ok'}

@app.route('/denyRequest', methods=['POST'])
def denyRequest():
    pass

# ==================Chat Room================
@app.route('/chatWith/<friend>/')
def chatWith(friend):
    if 'username' not in session:
        return redirect(url_for('login'))
    sender = session['username']
    receiver = friend
    cursor = db.cursor()
    sql = 'SELECT * FROM Messages WHERE (sender=%s and receiver=%s) or (sender=%s and receiver=%s) ORDER BY time'
    cursor.execute(sql, (sender, receiver, receiver, sender))
    results = cursor.fetchall()
    return render_template('chatWith.html', friend=friend, results=results)

@app.route('/sendMessage/<friend>', methods=['POST'])
def sendMessage(friend):
    if 'username' not in session:
        return redirect(url_for('login'))
    sender = session['username']
    receiver = friend
    content = request.form['input']
    time = datetime.now()
    cursor = db.cursor()
    print(sender, receiver, content, time)
    sql = 'INSERT INTO Messages(sender, receiver, content, time) VALUES(%s, %s, %s, %s)'
    cursor.execute(sql, (sender, receiver, content, time))
    return redirect(url_for('chatWith', friend=friend))

@app.route('/searchDialog', methods=['POST'])
def searchDialog():
    friend = request.form['keyword']
    return redirect(url_for('chatWith', friend=friend))

@app.route('/dialogList')
def dialogList():
    if 'username' not in session:
        return redirect(url_for('login'))
    sender = session['username']
    cursor = db.cursor()
    sql = """
            SELECT DISTINCT 
                CASE 
                    WHEN sender=%s THEN receiver
                    WHEN receiver=%s THEN sender
                END AS friend
            FROM Messages
            WHERE sender=%s OR receiver=%s"""
    cursor.execute(sql, (sender, sender, sender, sender))
    friends = cursor.fetchall()
    return render_template('chatRoom.html', friends=friends)

# ===================User List=========================
def followedSet(follower):
    cursor = db.cursor()
    sql = 'SELECT followed FROM Follows WHERE follower=%s'
    cursor.execute(sql, follower)
    followeds =  cursor.fetchall()
    print(followeds)
    followeds = {followed[0] for followed in followeds}
    return followeds

@app.route('/userList')
def userList():
    if 'username' not in session:
        return redirect(url_for('login'))
    follower = session['username']
    cursor = db.cursor()
    sql = 'SELECT username FROM User WHERE username!=%s'
    cursor.execute(sql, follower)
    users =  cursor.fetchall()
    followeds = followedSet(follower)
    print(followeds)
    return render_template('userList.html', users=users, followeds=followeds)

@app.route('/follows/<followed>/', methods=['POST'])
def follows(followed):
    if 'username' not in session:
        return redirect(url_for('login'))
    follower = session['username']
    cursor = db.cursor()
    sql = 'INSERT INTO Follows(follower, followed) VALUES(%s, %s)'
    cursor.execute(sql, (follower, followed))
    return redirect(url_for('userList'))

@app.route('/unfollowed/<followed>/', methods=['POST'])
def unfollowed(followed):
    if 'username' not in session:
        return redirect(url_for('login'))
    follower = session['username']
    cursor = db.cursor()
    sql = 'DELETE FROM Follows WHERE follower=%s and followed=%s'
    cursor.execute(sql, (follower, followed))
    return redirect(url_for('userList'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
