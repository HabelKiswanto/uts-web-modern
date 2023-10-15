from flask import *
from flask import Flask, request, render_template
from app import app
from sqlalchemy import desc
from models import *

@app.route('/')
def index():
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

    return render_template('index.html', catalogue_data=catalogue_data, title='Index')

if __name__ == '__main__':
    app.run(debug=True)

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

@app.route('/editbook')
def editbook():
    catalogue_data = Catalogue.query.all()
    return render_template('editbook.html', catalogue_data=catalogue_data)

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
    print("username: ",username, password)
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