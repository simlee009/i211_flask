import pymysql.cursors
from app import app

def get_connection():
    return pymysql.connect(host=app.config['DB_HOST'],
                           user=app.config['DB_USER'],
                           password=app.config['DB_PASS'],
                           database=app.config['DB_DATABASE'])

def insert_event(name, date, host):
    sql = "insert into Events (name, date, host) values (%s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, date, host))
        conn.commit()

def get_events():
    sql = "select id, name, date, host from Events order by date"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
