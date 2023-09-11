import pymysql


conn = pymysql.connect(
    host='sql12.freesqldatabase.com',
    database='sql12645575',
    user='sql12645575',
    password='rl9iMMRcJE',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()
sql_query = """CREATE TABLE book(
        id integer PRIMARY KEY,
        author text NOT NULL,
        language text NOT NULL,
        title text NOT NULL    
)"""
cursor.execute(sql_query)
conn.close()

