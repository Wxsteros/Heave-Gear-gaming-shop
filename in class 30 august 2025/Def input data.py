import sqlite3

def insertToUsers(fname, lname, email):
    try:
        conn = sqlite3.connect(r"D:\python porgramming\example.db")
        c = conn.cursor()
        sql = '''INSERT INTO users (fname, lname, email) VALUES (?, ?, ?)'''
        data = (fname, lname, email)
        c.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print("Failed to insert", e)
    finally:
        if conn:
            conn.close()

insertToUsers('Kittikon', 'Kingwichit', 'Kittikon.k@kkumail.com')
insertToUsers('Rapirat', 'Wangdongbang', 'Rapirat.w@kkumail.com')
