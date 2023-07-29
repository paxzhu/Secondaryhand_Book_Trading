from flask import Flask, render_template, request, url_for, redirect
import pymysql

app = Flask(__name__)

db_info = dict(
    host='localhost',
    user='zpc',
    password='zpjzpc',
    database='secondary_hand_trading_sys',
    autocommit=True,
    )

db = pymysql.connect(**db_info)

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
            return redirect(url_for('mybooks', username=res[0]))
        return 'login failed'
    return render_template('login.html')

@app.route('/mybooks/<username>')
def mybooks(username):
    cursor = db.cursor()
    sql = 'SELECT book_name FROM Book WHERE username=%s'
    cursor.execute(sql, username)
    books = cursor.fetchall()
    return render_template('mybooks.html', books=books)

@app.route('/deleteBook/<bookname>', methods=['POST'])
def deleteBook(bookname):
    cursor = db.cursor()
    sql = 'DELETE FROM Book WHERE book_name=%s'
    cursor.execute(sql, bookname)
    return redirect(url_for('booklist'))

@app.route('/addBook', methods=['POST'])
def addBook():
    book_name = request.form['book_name']
    cursor = db.cursor()
    sql = 'INSERT INTO Book (book_name) VALUES (%s)'
    cursor.execute(sql, book_name)
    return redirect(url_for('booklist'))

@app.route('/booklist')
def booklist():
    cursor = db.cursor()
    sql = 'SELECT * FROM Book'
    cursor.execute(sql)
    books = cursor.fetchall()
    return render_template('booklist.html', books=books)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
