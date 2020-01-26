import sqlite3
conn = sqlite3.connect('dz_17.sqlite')
cursor = conn.cursor()

# cursor.execute('SELECT * from schedule_query')
mt_last_id=cursor.execute("SELECT max(querry_id) FROM main_table").fetchall()[0][0]
print(mt_last_id.fetchall()[0][0])
# print(cursor.execute('SELECT shed_id from schedule_query where schedule=?',('full',)).fetchall()[0][0])
