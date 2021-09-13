import pymysql.cursors
from app import app

def get_connection():
    return pymysql.connect(host=app.config['DB_HOST'],
                           user=app.config['DB_USER'],
                           password=app.config['DB_PASS'],
                           database=app.config['DB_DATABASE'],
                           cursorclass=pymysql.cursors.DictCursor)

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

def get_event(event_id):
    sql = "select id, name, date, host from Events where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id))
            return cursor.fetchone()

def update_event(event_id, name, date, host):
    sql = "update Events set name = %s, date = %s, host = %s where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, date, host, event_id))
        conn.commit()

def delete_event(event_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            # When deleting an event, delete all attendees first.
            sql = "delete from Attendees where event_id = %s"
            cursor.execute(sql, event_id)
            sql = "delete from Events where id = %s"
            cursor.execute(sql, event_id)
        conn.commit()

def get_attendees(event_id):
    sql = "select id, event_id, name, email, comment from Attendees where event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id))
            return cursor.fetchall()

def get_attendee(attendee_id):
    sql = "select id, event_id, name, email, comment from Attendees where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (attendee_id))
            return cursor.fetchone()

def insert_attendee(event_id, name, email, comment):
    sql = "insert into Attendees (event_id, name, email, comment) values (%s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, name, email, comment))
        conn.commit()

def update_attendee(attendee_id, name, email, comment):
    sql = "update Attendees set name = %s, email = %s, comment = %s where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, email, comment, attendee_id))
        conn.commit()

def delete_attendee(attendee_id):
    sql = "delete from Attendees where id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (attendee_id))
        conn.commit()
