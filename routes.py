from flask import *
from app import app
from models import *

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html',title='Index')

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

@app.route('/admin')
def admin_login_page():
    return render_template('/admin/login.html')

@app.route('/admin/catalogue')
def admin_catalogue():
    return render_template('/admin/catalogue.html')

@app.route('/admin/catalogue/edit')
def admin_catalogue_edit():
    return render_template('/admin/catalogue-edit.html')

@app.route('/admin/schedule')
def admin_schedule():
    return render_template('/admin/admin_schedule.html')


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
