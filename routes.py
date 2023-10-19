from flask import *
from flask import Flask, request, render_template
from app import app
from sqlalchemy import desc,text
from models import *

@app.route('/')
def index():
    login_status = request.cookies.get('login_status')
    if login_status != 'logged in':
        return redirect('login')
    else:    
        sort_by = request.args.get('sort_by', 'nama_buku')
        order = request.args.get('order', 'asc')
        availability = request.args.get('availability', 'all')
        searchbar = request.args.get('searchbar', '')

        # Log the updated URL
        updated_url = request.url
        print("Updated URL:", updated_url)

        # Your sorting and filtering logic here
        catalogue_data = Catalogue.query

        if availability == 'available':
            catalogue_data = catalogue_data.filter(Catalogue.status == 'available')

        if searchbar:
            catalogue_data = catalogue_data.filter(Catalogue.nama_buku.ilike(f'%{searchbar}%'))

        if sort_by == 'tanggal_masuk':
            if order == 'asc':
                catalogue_data = catalogue_data.order_by(Catalogue.tanggal_masuk)
            else:
                catalogue_data = catalogue_data.order_by(desc(Catalogue.tanggal_masuk))
        else:
            if order == 'asc':
                catalogue_data = catalogue_data.order_by(sort_by)
            elif order == 'dsc':
                catalogue_data = catalogue_data.order_by(desc(sort_by))

        catalogue_data = catalogue_data.all()

        return render_template('index.html', catalogue_data=catalogue_data, title='Home')


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
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('login_status','not logged in')
        return resp
    else:
        return render_template('login.html',title="Login")

@app.route('/admin/editbook')
def editbook():
    login_status = request.cookies.get('login_status')
    if login_status != 'admin logged in':
        return redirect('/admin')
    
    catalogue_data = Catalogue.query.all()
    return render_template('/admin/editbook.html', catalogue_data=catalogue_data)

@app.route('/reservation')
def reservation():
    return render_template('reservation.html',title='Reservation')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html',title='Schedule ')

def check_admin_login():
    login_status = request.cookies.get('login_status')
    if login_status != 'admin logged in':
        return False
    else:
        return True

@app.route('/admin/')
@app.route('/admin')
def admin_login_page():
    login_status = check_admin_login()
    if login_status == True:
        resp = make_response(render_template('/admin/login.html'))
        resp.set_cookie('login_status','not logged in')
        return resp

    return render_template('/admin/login.html')

@app.route('/admin/register')
def admin_register_page():
    login_status = check_admin_login()
    if login_status == False:
        return redirect('/admin')
    
    return render_template('/admin/register.html')

@app.route('/admin/catalogue')
def admin_catalogue():
    login_status = check_admin_login()
    if login_status == False:
        return redirect('/admin')
    
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
    login_status = check_admin_login()
    if login_status == False:
        return redirect('/admin')
    
    return render_template('/admin/borrow.html')

@app.route('/admin/register_user',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        nim = request.form.get('nim')
        full_name = request.form.get('nama')
        password = request.form.get('pass')
        conf_pass = request.form.get('confirm_pass')

        print("test")
        # Check if password = confirmation
        if password != conf_pass:
            flash("Password and confirm password does not match",'error')
            return redirect(url_for('admin_register_page'))

        # Check if the username is already taken
        existing_user = Students.query.filter_by(nim=nim).first()
        if existing_user:
            flash("Student already exists. Check the NIM.",'error')
            return redirect(url_for('admin_register_page'))

        new_user = Students(nim=nim,full_name=full_name,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful.", "success")
        return redirect(url_for('admin_register_page'))
    return redirect(url_for('admin_register_page'))        


@app.route('/admin/return')
def admin_return():
    login_status = check_admin_login()
    if login_status == False:
        return redirect('/admin')
    
    return render_template('/admin/return.html')

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
            resp.set_cookie('login_status','admin logged in')
            return resp
        
    flash('Invalid credentials. Please try again.', 'danger')
    return redirect(url_for('admin'))



@app.route('/borrow_book',methods=["post"])
def borrow_book():
    id_buku = request.form.get("id_buku")
    nim = request.form.get("nim")
    if id_buku != None and nim != None:
        student = Students.query.filter_by(nim=nim).first()
        book = Catalogue.query.filter_by(id_buku=id_buku).first()

        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('admin_return'))
        if not book: 
            flash('Book not found.', 'error')
            return redirect(url_for('admin_return'))
        
        if book.status == "available":
            book.status = "unavailable"
            lending = Peminjaman_ongoing(id_buku=id_buku,nim_peminjam=nim)
            db.session.add(lending)
            db.session.commit()
            flash(f'Book borrowed successfully!', 'success')
            return redirect(url_for('admin_borrow'))
        else:
            flash('Book is not available for borrowing.', 'error')
            return redirect(url_for('admin_borrow'))
        
    flash('Invalid input. Try again.', 'danger')
    return redirect(url_for('admin_borrow'))

@app.route('/return_book',methods=["post"])
def return_book():
    id_buku = request.form.get("id_buku")
    nim = request.form.get("nim")
    if id_buku != None and nim != None:
        student = Students.query.filter_by(nim=nim).first()
        book = Catalogue.query.filter_by(id_buku=id_buku).first()
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('admin_return'))
        if not book: 
            flash('Book not found.', 'error')
            return redirect(url_for('admin_return'))
        
        ongoing = Peminjaman_ongoing.query.filter_by(id_buku=id_buku).first()
        if ongoing:
            if ongoing.nim_peminjam != nim:
                flash('This student is not borrowing this book.', 'error')
                return redirect(url_for('admin_return'))
            
            if book.status == "unavailable":
                book.status = "available"
                returning = Peminjaman_done(id_buku=id_buku,nim_peminjam=nim,tanggal_peminjaman=ongoing.tanggal_peminjaman)
                db.session.add(returning)
                Peminjaman_ongoing.query.filter_by(id_buku=id_buku,nim_peminjam=nim).delete()
                db.session.commit()
                flash(f'Book returned successfully!', 'success')
                return redirect(url_for('admin_return'))
        else:
            flash('Book is not currently borrowed.', 'error')
            return redirect(url_for('admin_return'))
        
    flash('Invalid input. Try again.', 'danger')
    return redirect(url_for('admin_return'))

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
        print(e)
        return jsonify({"error": str(e)})

    
@app.route('/update_book/<int:book_id>', methods=['PUT'])
def change_book_details(book_id):
    try:
        book = Catalogue.query.get(book_id)
        if book:
            new_data = request.json
            book.nama_buku = new_data['updated_nama_buku']
            book.deskripsi_buku = new_data['updated_deskripsi_buku']
            book.tanggal_masuk = new_data['updated_tanggal_masuk']
            book.tanggal_terbit = new_data['updated_tanggal_terbit']
            book.author = new_data['updated_author']
            book.genre = new_data['updated_genre']
            book.status = new_data['updated_status']
            book.cover_link = new_data['cover_link']
            

            db.session.commit()
            return jsonify({"message": "Book details updated successfully."})
        else:
            return jsonify({"error": "Book not found."})
    except Exception as e:
        print(e)
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
    
@app.route('/admin/fines')
def view_fine():
    query = text("""
        SELECT Peminjaman_ongoing.nim_peminjam, Peminjaman_ongoing.id_buku, Catalogue.nama_buku, DATEDIFF(NOW(), Peminjaman_ongoing.tanggal_peminjaman) - 14 AS days_overdue
        FROM Peminjaman_ongoing
        INNER JOIN Catalogue ON Peminjaman_ongoing.id_buku = Catalogue.id_buku
        WHERE DATEDIFF(NOW(), Peminjaman_ongoing.tanggal_peminjaman) > 14
    """)
    result = db.session.execute(query)
    overdue_books = [(row.nim_peminjam, row.id_buku, row.nama_buku ,row.days_overdue, max(0, row.days_overdue) * 2000) for row in result]
    return render_template('/admin/denda.html',title='Fine', overdue_books=overdue_books)

@app.route('/admin/fines/delete/<nim>/<id_buku>', methods=['POST'])
def move_to_done(nim, id_buku):
    data_to_move = Peminjaman_ongoing.query.filter_by(nim_peminjam=nim, id_buku=id_buku).first()
    to_done = returning = Peminjaman_done(id_buku=id_buku,nim_peminjam=nim,tanggal_peminjaman=data_to_move.tanggal_peminjaman)
    db.session.add(to_done)
    Peminjaman_ongoing.query.filter_by(id_buku=id_buku,nim_peminjam=nim).delete()
    # Commit the changes to the database
    db.session.commit()

    flash('Book has been returned', 'success')
    return redirect(url_for('view_fine'))


if __name__ == '__main__':
    app.run(debug=True)