import pymysql
import datetime
def count_borrowed_books(conn, nim_peminjam):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM peminjaman_ongoing WHERE nim_peminjam = %s", (nim_peminjam,))
    count = cursor.fetchone()[0]
    
    return count

def pinjam_buku(conn, id_buku, nim_peminjam):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM catalogue WHERE id_buku = %s AND status = 'available'", (id_buku,))
    buku = cursor.fetchone()

    num_borrowed_books = count_borrowed_books(conn, nim_peminjam)
    if num_borrowed_books >= 2:
        print("Anda sudah meminjam dua buku. Tidak dapat meminjam buku lagi.")
        return

    if buku:
        cursor.execute("SELECT fine FROM students WHERE nim = %s", (nim_peminjam,))
        user = cursor.fetchone()

        if user:
            if user[0] == 0:
                current_time = datetime.datetime.now()
                cursor.execute("INSERT INTO peminjaman_ongoing (id_buku, nim_peminjam, tanggal_peminjaman, waktu_peminjaman) VALUES (%s, %s, %s, %s)",
                               (id_buku, nim_peminjam, current_time.date(), current_time.time()))

                cursor.execute("UPDATE catalogue SET status = 'unavailable' WHERE id_buku = %s", (id_buku,))
                conn.commit()
                print("Buku berhasil dipinjam!")
            else:
                print("Anda memiliki denda. Anda tidak dapat meminjam buku baru.")
        else:
            print("NIM peminjam tidak ditemukan.")
    else:
        print("Buku tidak tersedia atau tidak ditemukan.")

    cursor.close()

def kembalikan_buku(conn, id_buku, nim_peminjam):
    cursor = conn.cursor()

    # Check if the book is borrowed by the user
    cursor.execute("SELECT * FROM peminjaman_ongoing WHERE id_buku = %s AND nim_peminjam = %s", (id_buku, nim_peminjam))
    borrowed_book = cursor.fetchone()

    if borrowed_book:
        current_time = datetime.datetime.now()
        return_date = current_time.date()

        # Calculate the fine if the book is returned late (after 14 days)
        tanggal_peminjaman = borrowed_book[3]  # assuming the third column is the borrow date
        days_late = (return_date - tanggal_peminjaman).days - 14
        fine = max(0, days_late // 2) * 2000

        # Update the fine for the student
        cursor.execute("UPDATE students SET fine = fine + %s WHERE nim = %s", (fine, nim_peminjam))

        # Insert data into the peminjaman_done table
        cursor.execute("INSERT INTO peminjaman_done (id_buku, nim_peminjam, tanggal_peminjaman, tanggal_pengembalian) VALUES (%s, %s, %s, %s)",
                       (id_buku, nim_peminjam, tanggal_peminjaman, return_date))

        # Delete the entry from peminjaman_ongoing
        cursor.execute("DELETE FROM peminjaman_ongoing WHERE id_buku = %s AND nim_peminjam = %s", (id_buku, nim_peminjam))

        # Update the status of the book to "available" in the catalogue table
        cursor.execute("UPDATE catalogue SET status = 'available' WHERE id_buku = %s", (id_buku,))
        conn.commit()
        print("Buku berhasil dikembalikan")
    else:
        print("Buku tidak ditemukan atau tidak dipinjam oleh NIM tersebut.")

    cursor.close()

connection = pymysql.connect(host='localhost', user='root', password='', database='perpus calvin')
cursor = connection.cursor()

id_buku = 1
nim_peminjam = 3
#try:

#pinjam atau kembalikan(connection, id_buku, nim_peminjam)
#pinjam_buku(connection, 2, 103)
#kembalikan_buku(connection, 2, 103)

#except Exception as e:
 #       print(f"Error: {e}")
#connection.close()
