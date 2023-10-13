from flask import *
from app import app
from models import *

@app.route('/')
def index():
    catalogue_data = Catalogue.query.all()
    return render_template('index.html', catalogue_data=catalogue_data, title='Index')

def show_catalogue():
    catalogue_data = Catalogue.query.all()
    return render_template('dummy.html', catalogue_data=catalogue_data)

@app.route('/dummy')
def show_catalogue():
    catalogue_data = Catalogue.query.all()
    return render_template('dummy.html', catalogue_data=catalogue_data)


@app.route('/login')
def login():
    login_status = request.cookies.get('login_status')
    if login_status == 'logged in':
        return redirect('/')
    else:
        return render_template('login.html',title="Login")

@app.route('/reservation')
def reservation():
    return render_template('reservation.html',title='Reservation')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html',title='Schedule ')

@app.route('/admin/login')
def admin_login_page():
    return render_template('/admin/login.html')

@app.route('/admin/catalogue')
def admin_catalogue():
    catalogue_data = Catalogue.query.all()
    return render_template('admin/catalogue.html', catalogue_data=catalogue_data, title='Index')

@app.route('/admin/catalogue/edit')
def admin_catalogue_edit():
    return render_template('/admin/catalogue-edit.html')

@app.route('/admin/schedule')
def admin_schedule():
    return render_template('/admin/admin_schedule.html')


@app.route('/admin/borrow')
def admin_borrow():
    return render_template('/admin/borrow.html')


@app.route('/login_user',methods=["post"])
def user_login():
    nim = request.form.get("nim")
    password = request.form.get("password")
    if nim != None and password != None:
        student = Students.query.filter_by(nim=nim).first()
        if student and (password == student.password):
            flash('Login successful!', 'success')
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('login_status','logged in')
            resp.set_cookie('account_type','user')
            resp.set_cookie('nim',nim)
            return resp
        
    flash('Invalid credentials. Please try again.', 'danger')
    return redirect(url_for('login'))

@app.route('/login_admin',methods=["post"])
def admin_login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username != None and password != None:
        acc = Admin.query.filter_by(username=username).first()
        if acc and (password == acc.password):
            flash('Login successful!', 'success')
            resp = make_response(redirect(url_for('admin_catalogue')))
            resp.set_cookie('login_status','logged in')
            resp.set_cookie('account_type','admin')
            resp.set_cookie('username',username)
            return resp
        
    flash('Invalid credentials. Please try again.', 'danger')
    return redirect(url_for('admin_login_page'))


@app.route('/borrow_book',methods=["post"])
def borrow_book():
    id_buku = request.form.get("id_buku")
    nim = request.form.get("nim")
    if id_buku != None and nim != None:
        student = Students.query.filter_by(nim=nim).first()
        book = Catalogue.query.filter_by(id_buku=id_buku).first()
        if student and book:
            if book.status == "available":
                book.status = "unavailable"
                lending = Peminjaman_ongoing(id_buku=id_buku,nim_peminjam=nim)
                db.session.add(lending)
                db.session.commit()
                flash(f'Book borrowed successfully!', 'success')
            else:
                flash('Book is not available for borrowing.', 'error')
        else:
            flash('Book not found.', 'error')
            return redirect(url_for('admin_borrow'))
        
    flash('Invalid input. Try again.', 'danger')
    return redirect(url_for('admin_borrow'))

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