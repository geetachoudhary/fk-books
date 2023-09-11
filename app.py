
from flask import Flask, request, jsonify
import json
import pymysql

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(host='sql12.freesqldatabase.com',
                                database='sql12645575',
                                user='sql12645575',
                                password='rl9iMMRcJE',
                                cursorclass=pymysql.cursors.DictCursor
                               )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book")
        db_book_list = cursor.fetchall()
        print(db_book_list)
        all_books = [
            dict(id=row['id'], author=row['author'], language=row['language'], title=row['title'])
            for row in db_book_list
        ]
        if all_books is not None:
            return jsonify(all_books)
        return jsonify([])

    if request.method == 'POST':
        new_author = request.form['author']
        new_language = request.form['language']
        new_title = request.form['title']

        sql = """INSERT INTO book(author, language, title)
                    VALUES (%s, %s, %s)"""
        cursor.execute(sql, (new_author, new_language, new_title))
        conn.commit()
        return "Book with the id: 0 created successfully"


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id= %s", id)
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE book
                    SET title=%s,
                    author=%s,
                    language=%s
                    WHERE id = %s"""

        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
            'id': id,
            'author': author,
            'language': language,
            'title': 'title'
        }
        conn.execute(sql, (title, author, language, id))
        conn.commit()
        return jsonify(updated_book)
    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id = ? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200


if __name__ == '__main__':
    app.run()
