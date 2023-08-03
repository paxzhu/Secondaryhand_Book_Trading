from flask import Flask, render_template, request, url_for, redirect, session
import pymysql
from datetime import datetime

# Set the secret key to some random bytes. Keep this really secret!

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

def saveMessage():
    cursor = db.cursor()
    sql = 'INSERT INTO Message(sender, action, bookname, receiver) VALUES(%s, %s, %s, %s)'
    cursor.execute(sql, (sender, action, bookname, receiver))

@app.route('/')
def hello():
    
    return 'hello'

# login. redirect to user's home page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        sql = 'SELECT username FROM User WHERE username=%s AND password=%s'
        cursor.execute(sql,(username, password))
        res = cursor.fetchone()
        if res:
            session['username'] = res[0]
            return redirect(url_for('book_status'))
        return 'login failed'
    return render_template('login.html')



@app.route('/book_status')
def book_status():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    cursor = db.cursor()
    sql = 'SELECT * FROM Book WHERE username=%s OR loaned_to=%s'
    cursor.execute(sql, (username, username))
    books = cursor.fetchall()
    return render_template('book_status.html', books=books, owner=username)

@app.route('/deleteBook/<bookname>', methods=['POST'])
def deleteBook(bookname):
    cursor = db.cursor()
    sql = 'DELETE FROM Book WHERE bookname=%s'
    cursor.execute(sql, bookname)
    return redirect(url_for('book_status'))

@app.route('/addBook', methods=['POST'])
def addBook():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    bookname = request.form['bookname']
    cursor = db.cursor()
    sql = 'INSERT INTO Book(bookname, username, loaned_to) VALUES(%s, %s, NULL)'
    cursor.execute(sql, (bookname, username))
    return redirect(url_for('book_status'))

@app.route('/trading_square')
def trading_square():
    cursor = db.cursor()
    sql = 'SELECT * FROM Book'
    cursor.execute(sql)
    books = cursor.fetchall()
    return render_template('trading_square.html', books=books)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor = db.cursor()
    sql = f"SELECT * FROM Book WHERE bookname like '%{keyword}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('trading_square.html', books=results)

@app.route('/borrowBook/<bookname>', methods=['POST'])
def borrowBook(bookname):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    cursor = db.cursor()
    sql = 'UPDATE Book SET request=%s WHERE bookname=%s'
    cursor.execute(sql, (username, bookname))
    return redirect(url_for('trading_square'))

@app.route('/returnBook/<bookname>', methods=['POST'])
def returnBook(bookname):
    cursor = db.cursor()
    sql = 'UPDATE Book SET loaned_to=NULL WHERE bookname=%s'
    cursor.execute(sql, bookname)
    return redirect(url_for('book_status'))

@app.route('/allowRequest/<bookname>', methods=['POST'])
def allowRequest(bookname):
    _, _, request, _ =  getBookMetaData(bookname)
    cursor = db.cursor()
    sql = 'UPDATE Book SET request=NULL, loaned_to=%s WHERE bookname=%s'
    cursor.execute(sql, (request, bookname))
    return redirect(url_for('book_status'))

@app.route('/denyRequest', methods=['POST'])
def denyRequest():
    pass

# ==================ChatRoom================
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
