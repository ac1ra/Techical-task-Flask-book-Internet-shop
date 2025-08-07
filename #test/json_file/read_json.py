import sqlite3
import json

conn = sqlite3.connect('books.db')
cursor = conn.cursor()
json_file = 'books_catalog.json'


cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author TEXT NOT NULL,
price INT,
genre TEXT NOT NULL,
cover TEXT NOT NULL,
description TEXT NOT NULL,
rating INT,
year INT
)
''')


def insert_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)

            for item in data:
                print(item['title'], type(item['title']))

                cursor.execute(
                    '''INSERT INTO users(title, author,price,genre,cover,description,rating,year) VALUES (?,?,?,?,?,?,?,?)''', (
                        item['title'], item['author'], item['price'], item['genre'], item['cover'], item['description'], item['rating'], item['year'])
                )
        except json.JSONDecodeError as e:
            print(f"Error JSON: {e}")


if __name__ == "__main__":
    insert_data(json_file)
    conn.commit()
    conn.close()
