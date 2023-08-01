from flask import Flask, render_template, request, url_for, redirect, session
import pymysql

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

def getBookMetaData(book_name):
    cursor = db.cursor()
    sql = 'SELECT * FROM Book WHERE book_name=%s'
    cursor.execute(sql, book_name)
    metaData = cursor.fetchone()
    return metaData

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
    sql = 'DELETE FROM Book WHERE book_name=%s'
    cursor.execute(sql, bookname)
    return redirect(url_for('book_status'))

@app.route('/addBook', methods=['POST'])
def addBook():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    book_name = request.form['book_name']
    cursor = db.cursor()
    sql = 'INSERT INTO Book(book_name, username, loaned_to) VALUES(%s, %s, NULL)'
    cursor.execute(sql, (book_name, username))
    return redirect(url_for('book_status'))

@app.route('/trading_square')
def trading_square():
    cursor = db.cursor()
    sql = 'SELECT * FROM Book'
    cursor.execute(sql)
    books = cursor.fetchall()
    return render_template('trading_square.html', books=books)

@app.route('/borrowBook/<bookname>', methods=['POST'])
def borrowBook(bookname):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    cursor = db.cursor()
    sql = 'UPDATE Book SET request=%s WHERE book_name=%s'
    cursor.execute(sql, (username, bookname))
    return redirect(url_for('trading_square'))

@app.route('/returnBook/<bookname>', methods=['POST'])
def returnBook(bookname):
    cursor = db.cursor()
    sql = 'UPDATE Book SET loaned_to=NULL WHERE book_name=%s'
    cursor.execute(sql, bookname)
    return redirect(url_for('book_status'))

@app.route('/allowRequest/<bookname>', methods=['POST'])
def allowRequest(bookname):
    _, _, request, _ =  getBookMetaData(bookname)
    cursor = db.cursor()
    sql = 'UPDATE Book SET request=NULL, loaned_to=%s WHERE book_name=%s'
    cursor.execute(sql, (request, bookname))
    return redirect(url_for('book_status'))

@app.route('/denyRequest', methods=['POST'])
def denyRequest():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
