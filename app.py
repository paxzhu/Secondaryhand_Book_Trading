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
        username = request.args.get('username')
        password = request.args.get('password')
        cursor = db.cursor()
        sql = 'SELECT username FROM User WHERE username=%s AND password=%s'
        cursor.execute(sql,(username, password))
        res = cursor.fetchall()
        if res:
            return 'login successed'
        return 'login failed'
    return render_template('login.html')

@app.route('/deleteBook/<bookname>', methods=['POST'])
def deleteBook(bookname):
    cursor = db.cursor()
    sql = 'DELETE FROM Book WHERE book_name=%s'
    cursor.execute(sql, bookname)
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
