import pymysql

def register_student(conn, nim, full_name, password):
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO students (nim, full_name, password) VALUES (%s, %s, %s)", (nim, full_name, password))
        conn.commit()
        print("Registrasi berhasil!")
    except pymysql.Error as e:
        conn.rollback()
        print(f"Error: {e}")

    cursor.close()

connection = pymysql.connect(host='localhost', user='root', password='', database='perpus calvin')
cursor = connection.cursor()
try:
    

    nim = 103
    full_name = "Justin Habel Kiswanto"
    password = "ehey"

    register_student(connection, nim, full_name, password)
except pymysql.Error as e:
    print(f"Error: {e}")
    
if connection:
    connection.close()
