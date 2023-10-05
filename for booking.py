import pymysql
import datetime

def is_room_available(cursor, booking_date, booking_time, room_name):
    query = f"""
        SELECT * 
        FROM room_bookings 
        WHERE room_name = '{room_name}'
        AND booking_date = '{booking_date}'
        AND (
            ('{booking_time}' BETWEEN booking_time AND end_time)
            OR ('{end_time}' BETWEEN booking_time AND end_time)
        )"""
    cursor.execute(query)
    return cursor.fetchone() is None

def has_fine(cursor, student_id):
    query = f"SELECT fine FROM students WHERE id = {student_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return result and result[0] > 0

def is_valid_booking_time(booking_time, end_time):
    opening_booking_time = datetime.time(7, 30)
    closing_booking_time = datetime.time(22, 00)
    return opening_booking_time <= booking_time <= closing_booking_time and booking_time <= end_time <= closing_booking_time

def book_room(cursor, student_id, booking_date, booking_time_str, end_time_str, room_name):
    booking_time = datetime.datetime.strptime(booking_time_str, '%H:%M:%S').time()
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M:%S').time()

    booking_duration = (end_time.hour * 3600 + end_time.minute * 60 + end_time.second) - (booking_time.hour * 3600 + booking_time.minute * 60 + booking_time.second)

    if not is_valid_booking_time(booking_time, end_time):
        return "Ruangan hanya dapat dipesan antara pukul 7:30 pagi hingga 22:00 malam."
    if has_fine(cursor, student_id):
        return "Anda memiliki denda yang belum lunas. Tidak dapat melakukan pemesanan."
    elif not is_room_available(cursor, booking_date, booking_time, room_name):
        return "Ruangan sudah dibooking pada tanggal dan jam tersebut. Silakan coba lagi nanti."
    elif booking_duration > 2 * 3600: 
        return "Ruangan hanya dapat dibooking selama 2 jam per hari."
    elif booking_duration < 1800:  # 1800 seconds = 30 minutes
        return "Ruangan minimal dibooking 30 menit"
    elif end_time > datetime.time(22, 0):  
        return "Waktu selesai pemesanan tidak dapat melebihi pukul 22:00."
    else:
        query = f"INSERT INTO room_bookings (student_id, booking_date, booking_time, end_time, room_name) VALUES ({student_id}, '{booking_date}', '{booking_time}', '{end_time}', '{room_name}')"
        cursor.execute(query)
        return "Pemesanan berhasil."

connection = pymysql.connect(host='localhost', user='root', password='', database='perpus calvin')
cursor = connection.cursor()

student_id = 1
booking_date = '2023-10-16'
booking_time = '8:00:00'
end_time = '10:00:00'  
room_name = 'Ruangan A'

result = book_room(cursor, student_id, booking_date, booking_time, end_time, room_name)
print(result)

cursor.close()
connection.close()

#duration between end_time and booking_time
