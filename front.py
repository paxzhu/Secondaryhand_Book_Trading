from flask import Flask, render_template, request, url_for, redirect, session
import pymysql, requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
back_end = 'http://127.0.0.1:5000'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = back_end + '/login'
        response = requests.post(url, data = request.form)
        data = response.json()
        if data['status'] == 'success':
            session['username'] = data['username']
            return redirect(url_for('book_status'))
        return 'login failed'
    return render_template('login.html')

@app.route('/book_status')
def book_status():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    url = back_end + '/book_status'
    response = requests.post(url, data={'username':username})
    books = response.json()
    print(books)
    return render_template('book_status.html', books=books, owner=username)

@app.route('/deleteBook/<bookname>', methods=['POST'])
def deleteBook(bookname):
    url = back_end + '/deleteBook'
    response = requests.post(url, data={'bookname':bookname})
    data = response.json()
    if data['status'] == 'ok':
        return redirect(url_for('book_status'))
    return 

@app.route('/addBook', methods=['POST'])
def addBook():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    url = back_end + '/addBook'
    response = requests.post(url, data={'username':username, 'bookname':request.form['bookname']})
    data = response.json()
    
    return redirect(url_for('book_status'))

@app.route('/trading_square')
def trading_square():
    url = back_end + '/trading_square'
    response = requests.get(url)
    books = response.json()

    return render_template('trading_square.html', books=books)

@app.route('/search', methods=['POST'])
def search():
    url = back_end + '/search'
    response = requests.post(url, data=request.form)
    books = response.json()
    return render_template('trading_square.html', books=books)

@app.route('/borrowBook/<bookname>', methods=['POST'])
def borrowBook(bookname):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    url = back_end + '/borrowBook'
    response = requests.post(url, data={'username': username, 'bookname':bookname})
    books = response.json()
    return redirect(url_for('trading_square'))

@app.route('/returnBook/<bookname>', methods=['POST'])
def returnBook(bookname):
    url = back_end + '/returnBook'
    response = requests.post(url, data={'bookname':bookname})
    books = response.json()
    return redirect(url_for('book_status'))

@app.route('/allowRequest/<bookname>', methods=['POST'])
def allowRequest(bookname):
    url = back_end + '/allowRequest'
    response = requests.post(url, data={'bookname':bookname})
    data = response.json()
    return redirect(url_for('book_status'))

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
    app.run(debug=True, port=5555)