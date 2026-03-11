import sqlite3
conn = sqlite3.connect(r"D:\python porgramming\example.db")
c = conn.cursor()
try:
    data = [('Kittikon', 'Kingwichit', 'Kittikon.k@kkumail.com'), ('Rapirat', 'Wangdongbang', 'Rapirat.w@kkumail.com'), ('Thaptap', 'Teaksom', 'Theptap.t@kkumail.com')]
    c.executemany('''INSERT INTO users (fname, lname, email) VALUES (?, ?, ?)''', data)
    conn.commit()
except sqlite3.Error as e:
    print(e)
finally:
    if conn:
        conn.close()