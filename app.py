from flask import *
from flask import Flask, request, jsonify, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

app.secret_key = 'And blood black nothingness began to spin. A series of cells interlinked within cells interlinked within cells interlinked within one stem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/perpus_calvin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### models ###

class Room_bookings(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.nim'))
    booking_date = db.Column(db.Date)
    booking_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    room_name = db.Column(db.String(200))

class Students(db.Model):
    nim = db.Column('nim',db.Integer,primary_key=True)
    full_name = db.Column(db.String)
    password = db.Column(db.String)
    fine = db.Column(db.Float,default=0.0)
    room_bookings = db.relationship('Room_bookings',backref='room_bookings')
    peminjaman_ongoing = db.relationship('Peminjaman_ongoing',backref='peminjaman_ongoing')

class Peminjaman_ongoing(db.Model):
    id_peminjaman = db.Column('id_peminjaman',db.Integer,primary_key=True)
    id_buku = db.Column(db.Integer,db.ForeignKey('catalogue.id_buku')) 
    nim_peminjam = db.Column(db.Integer,db.ForeignKey('students.nim'))
    tanggal_peminjaman = db.Column(db.Date)
    waktu_peminjaman = db.Column(db.Time)

class Peminjaman_done(db.Model):
    id_peminjaman = db.Column('id_peminjaman',db.Integer,primary_key=True)
    id_buku = db.Column(db.Integer,db.ForeignKey('catalogue.id_buku')) 
    nim_peminjam = db.Column(db.Integer,db.ForeignKey('students.nim'))
    tanggal_peminjaman = db.Column(db.Date)
    tanggal_pengembalian = db.Column(db.Date)

class Catalogue(db.Model):
    id_buku = db.Column('id_buku',db.Integer,primary_key=True)
    nama_buku = db.Column(db.String(200))
    deskripsi_buku = db.Column(db.String(255))
    tanggal_masuk = db.Column(db.Date)
    tanggal_terbit = db.Column(db.Date)
    author = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    status = db.Column(db.String(255))
    cover_link = db.Column(db.String(255))



### models ###

@app.route('/')
def index():
    print(url_for('static', filename='style.css'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/admin/edit_book')
def admin_edit_book():
    return render_template('editbook.html')

@app.route('/login_user',methods=["post","get"])
def user_login():
    _method = request.method
    if _method == 'POST':
        nim = request.form.get("nim")
        password = request.form.get("password")
        
        student = Students.query.filter_by(nim=nim).first()

        if student and (password == student.password):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))


#Habel
@app.route('/add_book', methods=['POST'])
def add_new_book():
    try:
        book_data = request.json
        new_book = Catalogue(
            nama_buku=book_data['nama_buku'],
            deskripsi_buku=book_data['deskripsi_buku'],
            tanggal_masuk=book_data['tanggal_masuk'],
            tanggal_terbit=book_data['tanggal_terbit'],
            author=book_data['author'],
            genre=book_data['genre'],
            status=book_data['status'],
            cover_link=book_data['cover_link']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/update_book/<int:book_id>', methods=['PUT'])
def change_book_details(book_id):
    try:
        book = Catalogue.query.get(book_id)
        if book:
            new_data = request.json
            book.nama_buku = new_data['nama_buku']
            book.deskripsi_buku = new_data['deskripsi_buku']
            book.tanggal_masuk = new_data['tanggal_masuk']
            book.tanggal_terbit = new_data['tanggal_terbit']
            book.author = new_data['author']
            book.genre = new_data['genre']
            book.status = new_data['status']
            book.cover_link = new_data['cover_link']
            db.session.commit()
            return jsonify({"message": "Book details updated successfully."})
        else:
            return jsonify({"error": "Book not found."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/remove_book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    try:
        book = Catalogue.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Book removed successfully."})
        else:
            return jsonify({"error": "Book not found."})
    except Exception as e:
        return jsonify({"error": str(e)})