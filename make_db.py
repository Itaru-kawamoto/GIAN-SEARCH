import sqlite3
import pandas as pd


df = pd.read_csv('/Users/kawamoto/Desktop/Gian-Search/Gian_title.csv')

df.colums = ['date', 'title']


dbname = 'GIAN_TITEL.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

df.to_sql('titles', conn, if_exists='replace')

select_sql = 'SELECT * FROM titles'
for row in cur.execute(select_sql):
    print(row)

cur.close()
conn.close()