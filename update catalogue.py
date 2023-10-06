import pymysql
import datetime

connection = pymysql.connect(host='localhost', user='root', password='', database='perpus calvin')
cursor = connection.cursor()

def add_new_book(book_data):
    try:
        # Insert a new book into the catalog table
        sql = "INSERT INTO catalogue (nama_buku, deskripsi_buku, tanggal_masuk, tanggal_terbit, author, genre, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            book_data['nama_buku'],
            book_data['deskripsi_buku'],
            book_data['tanggal_masuk'],
            book_data['tanggal_terbit'],
            book_data['author'],
            book_data['genre'],
            book_data['status']
        ))
        connection.commit()
        print("New book added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    if connection:
        connection.close()

def change_book_details(book_id, new_data):
    try:
        # Insert a new book into the catalog table
        sql = "UPDATE catalogue SET nama_buku=%s, deskripsi_buku=%s, tanggal_masuk=%s, tanggal_terbit=%s, author=%s, genre=%s, status=%s WHERE id_buku=%s"
        cursor.execute(sql, (
                    new_data['nama_buku'],
                    new_data['deskripsi_buku'],
                    new_data['tanggal_masuk'],
                    new_data['tanggal_terbit'],
                    new_data['author'],
                    new_data['genre'],
                    new_data['status'],
                    book_id
                ))
        connection.commit()
        print("Book details updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    if connection:
        connection.close()


def remove_book(book_id):
    try:
        sql = "DELETE FROM catalogue WHERE id_buku=%s"
        cursor.execute(sql, (book_id,))
        connection.commit()
        print("Book removed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    if connection:
        connection.close()


new_book_data = {
    'nama_buku': 'Stanley',
    'deskripsi_buku': 'A struggle against Autism',
    'tanggal_masuk': '2023-10-01',
    'tanggal_terbit': '2022-01-15',
    'author': 'Habel',
    'genre': 'Biography',
    'status': 'Available'
}


updated_book_data = {
    'nama_buku': '100 cara menjadi Ryan Gosling',
    'deskripsi_buku': 'bagaimana cara menjadi pria pujangga idola semua pria',
    'tanggal_masuk': '2023-10-01',
    'tanggal_terbit': '2022-01-15',
    'author': 'Kenji Yamamoto',
    'genre': 'Pyschology',
    'status': 'Available'
}

#add_new_book(new_book_data)
change_book_details(2, updated_book_data) 
#remove_book(3)
#Kelemahan kode ini: cuma bisa ngerun 1 at the time, mungkin cocok sih untuk fungsinya
