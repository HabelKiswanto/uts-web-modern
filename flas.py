from flask import Flask, request, jsonify, send_from_directory
import pymysql
import re
# app = Flask(__name__)

# Define your database connection settings here
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'perpus_calvin'
connection = pymysql.connect(host='localhost', user='root', password='', database='perpus calvin')
cursor = connection.cursor()

@app.route('/add_book', methods=['POST'])
def add_new_book():
    try:
        # Get book data from the request
        book_data = request.json

        # Insert a new book into the catalog table
        sql = "INSERT INTO catalogue (nama_buku, deskripsi_buku, tanggal_masuk, tanggal_terbit, author, genre, status, cover_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            book_data['nama_buku'],
            book_data['deskripsi_buku'],
            book_data['tanggal_masuk'],
            book_data['tanggal_terbit'],
            book_data['author'],
            book_data['genre'],
            book_data['status'],
            book_data['cover_link']

        ))
        connection.commit()
        print("New book added successfully.")
        return jsonify({"message": "Book added successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/update_book/<int:book_id>', methods=['PUT'])
def change_book_details(book_id):
    try:

        # Get updated book data from the request
        new_data = request.json

        # Update book details in the catalog table
        sql = "UPDATE catalogue SET nama_buku=%s, deskripsi_buku=%s, tanggal_masuk=%s, tanggal_terbit=%s, author=%s, genre=%s, status=%s, cover_link=%s WHERE id_buku=%s"
        cursor.execute(sql, (
            new_data['nama_buku'],
            new_data['deskripsi_buku'],
            new_data['tanggal_masuk'],
            new_data['tanggal_terbit'],
            new_data['author'],
            new_data['genre'],
            new_data['status'],
            new_data['cover_link'],
            book_id
        ))
        connection.commit()
        return jsonify({"message": "Book details updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/remove_book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    try:

        # Delete a book from the catalog table
        sql = "DELETE FROM catalogue WHERE id_buku=%s"
        cursor.execute(sql, (book_id,))
        connection.commit()
        return jsonify({"message": "Book removed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def editbooks():
    return send_from_directory('templates', 'editbook.html')

if __name__ == '__main__':
    app.run(debug=True)