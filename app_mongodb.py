from flask import Flask, render_template, request, url_for, redirect, session
from datetime import datetime
from pymongo import MongoClient
app = Flask(__name__)

# 创建 MongoDB 连接
client = MongoClient('localhost', 27017)
db = client.secondary_hand_trading_sys
Books = db.Books
User = db.User

@app.route('/login', methods=['GET', 'POST'])
def login():
    username, password = request.form['username'], request.form['password']
    

@app.route('/trading_square')
def trading_square():
    books = Books.find()
    # book_info = []
    # for book in books:
    #     single = [book['name'], book['belong_to'], book['request'], book['loaned_to']]
    #     book_info.append(single)
    books = [book.values() for book in books if book.pop('_id')]
    return render_template('trading_square.html', books=books)


@app.route('/borrowBook/<bookname>', methods=['POST'])
def borrowBook(bookname):
    
    return "hello"

if __name__ == '__main__':
    app.run(debug=True, port=5000)