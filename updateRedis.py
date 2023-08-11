
import pymysql
import redis
import json
db_info = dict(
    host='localhost',
    user='zpc',
    password='zpjzpc',
    database='secondary_hand_trading_sys',
    autocommit=True,
    )
db = pymysql.connect(**db_info)

r = redis.Redis(host='localhost', port=6379, db=1)

# =================cache the contents of trading square=================


# =====================cache the top10clicks to Redis===================

def createView_top10clicks():
    with db.cursor() as cursor:
        sql = """CREATE view top10_click_books as 
                SELECT Book.bookname, Book.username, Click.count 
                FROM Book join Click ON Click.book = Book.bookname 
                ORDER BY Click.count desc limit 100"""
        cursor.execute(sql)

def cache_top10_clicks():
    with db.cursor() as cursor:
        sql = "SELECT * FROM top10_click_books"
        cursor.execute(sql)
        top10clicks = cursor.fetchall()
        for book, owner, clicks in top10clicks:
            info = {'owner':owner, 'clicks':clicks}
            r.hset("Topbooks::top100clicks", book, json.dumps(info))

def get_top10_clicks():
    data = r.hgetall("Topbooks::top100clicks")
    decoded_data = {}
    for key, value in data.items():
        decoded_key = key.decode('utf-8')
        decoded_value = value.decode('utf-8')
        decoded_data[decoded_key] = json.loads(decoded_value)
    sorted_data = sorted(decoded_data.items(), key=lambda item: item[1]['clicks'], reverse=True)
    return dict(sorted_data)

if __name__ == '__main__':
    print(get_top10_clicks())