from flask import Flask, redirect, render_template, request, send_file, session, flash, jsonify, Response, url_for ,Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from faulthandler import disable
from io import BytesIO
import datetime
from fileinput import filename
from .models import *
from .func import convert_salary
from . import db,mail
from flask_mail import Message,Mail


employers = Blueprint('employers',__name__)

@employers.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        workfield = request.form.get('workfield')
        print(username,email,password,workfield)

        #check if username and email are unique

        #users = []
        u = Users_database.query.all()
        for g in u:
            #users.append((g.username,g.email))
            if g.username == username:
                flash("This username isn't available!",'error')
                return render_template('recruit.html')
            if g.email == email:
                flash("This email isn't available!",'error')
                return render_template('recruit.html')

        #add new user to the database
        
        password = generate_password_hash(password,"sha256")
        user = Users_database(username=username ,email=email,password_hash=password,workfield=workfield)
        db.session.add(user)
        db.session.commit()
        return render_template('recruit.html',new_message='Successfully created a new account!')

@employers.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        u = Users_database.query.all()
        for g in u:
            if g.email == email:
                #check the hash
                user = Users_database.query.filter_by(email=email).first()
                if check_password_hash(user.password_hash, password):
                    login_user(user)
                    flash("You have successfully logged in",'success')
                    print(user.username)
                    username = user.username
                    print('logged in')

                    #session
                    session['user'] = username
                    session['email'] = email

                    return redirect('/dashboard/'+str(username))
                else:
                    flash("The password is incorrect!",'error')
                    return render_template('recruit.html',error_message='The password is incorrect!')
                    #return redirect('/recruit')
        else:
            #flash("This user doesn't exist!",'error')
            return render_template('recruit.html',error_message='This user doesn t exist!')

@employers.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect('/recruit')

@employers.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if request.method == 'POST':
        user = Users_database.verify_token(token)
        print('user is:',user)
        if user is None:
            return '<h1>That is an invalid token or expired. Please try again!</h1>'
    
        new_password = request.form.get('new_pass')
        new_hashed_password = generate_password_hash(new_password,"sha256")
        user.password_hash = new_hashed_password
        db.session.commit()
        print('new pass!')
        flash('password changed!')
        return redirect('/recruit')
    else:
        user = Users_database.verify_token(token)
        print('user is:',user)
        if user is None:
            return '<h1>That is an invalid token or expired. Please try again!</h1>'
        else:
            return render_template('change_pass.html',token=token)


def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request',recipients=[user.email],sender='noreply@climaxresourcing.com')
    msg.body = f''' To reset your password please follow the link below.

    {url_for('employers.reset_token',token=token,_external=True)}

    If you didn't send a password reset request, please ignore this message.
    '''
    mail.send(msg)


@employers.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        print('email is',email)
        user = Users_database.query.filter_by(email=email).first()
        #Send email with unique token
        if user:
            send_mail(user)
            
            #email user 
            return redirect('/recruit')
        else:
            return render_template("forgot_pass.html",message='Oops something happened! Please try again!')

    else:
        return render_template("forgot_pass.html")


@employers.route('/download_cv/<string:filename>')
def download_cv(filename):
    upload = REQUESTS_database.query.filter_by(filename=filename).first()
    print(upload)
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

@employers.route('/dashboard/<string:user>', methods=['POST','GET'])
@login_required
def dashboard(user):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_num')
        org_name = request.form.get('org_name')
        org_postcode = request.form.get('org_postcode')
        position = request.form.get('position')
        reg_staff = request.form.get('reg_staff')
        staff_type = request.form.get('staff_type')
        location = request.form.get('location')
        staff_num = request.form.get('staff_num')
        specialty = request.form.get('specialty')
        contract_length = request.form.get('contract_length')
        salary = request.form.get('salary')
        salary_per = request.form.get('salary_per')
        job_desc = request.form.get('job_desc')
        image = request.files.get('pdf')

        #job_ad = JOB_ADS_database.query.filter_by(phone_number=phone_number).first()
        dt = datetime.datetime.today()
        date = str(dt.day) +"-"+ str(dt.month) +"-"+ str(dt.year)
        print("date is",date)
        #if not job_ad:
        ad = JOB_ADS_database(first_name=first_name, last_name=last_name, email=email, phone_number = phone_number, org_name= org_name , org_postcode=org_postcode, position=position, reg_staff= reg_staff, staff_type= staff_type, 
        location = location, staff_num = staff_num, specialty = specialty, contract_length=contract_length,salary = float(salary), salary_per=salary_per ,job_desc = job_desc ,date_posted = date, filename=image.filename,data=image.read(),visibility=1)
        db.session.add(ad)
        db.session.commit()
        flash("You have successfully posted you job ad",'success')
        return redirect('/dashboard/'+str(user))
        #else:
           # return redirect('/dashboard/'+str(user))

    else:
        userr = Users_database.query.filter_by(username=user).first()
        return render_template('dashboard.html',user = user, email = userr.email)

@employers.route('/requests', methods=['GET','POST'])
@login_required
def requests():
    user = session.get('user')
    email = session.get('email')
    print(user,email)
    if request.method == 'POST':
        pass
    else:
        #job_ads = JOB_ADS_database.query.filter_by(first_name=user, email=email).all()
        job_ads = JOB_ADS_database.query.filter_by(email=email).all()
        print(job_ads)
        req = []
        for i in job_ads:
            print(i.id)
            req.append(REQUESTS_database.query.filter_by(job_id = i.id).all())
        print('req',req)

        requests = []
        for j in req:
            if j:
                for k in j:
                    requests.append(k)
        try:
            r = requests
            print(requests[0])
            l=0
            for i in r:l+=1
        except:
            r = requests
            l=0
        print(l)
        print('r',r)
        return render_template('requests.html',job_ads=job_ads, req=r, l=l)

@employers.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_num')
        org_name = request.form.get('org_name')
        org_postcode = request.form.get('org_postcode')
        position = request.form.get('position')
        reg_staff = request.form.get('reg_staff')
        staff_type = request.form.get('staff_type')
        location = request.form.get('location')
        staff_num = request.form.get('staff_num')
        specialty = request.form.get('specialty')
        contract_length = request.form.get('contract_length')
        salary = request.form.get('salary')
        salary_per = request.form.get('salary_per')
        job_desc = request.form.get('job_desc')
        image = request.files.get('pdf')

        print(salary_per)
        #job_ad = JOB_ADS_database.query.filter_by(phone_number=phone_number).first()
        #if not job_ad:
        user_to_update = JOB_ADS_database.query.filter_by(id=id).first()

        if user_to_update:
            user_to_update.first_name = first_name
            user_to_update.last_name = last_name
            user_to_update.email = email
            user_to_update.phone_number = phone_number
            user_to_update.org_name = org_name
            user_to_update.org_postcode = org_postcode
            user_to_update.position = position
            user_to_update.reg_staff = reg_staff
            user_to_update.staff_type = staff_type
            user_to_update.location = location
            user_to_update.staff_num = staff_num
            user_to_update.specialty = specialty
            user_to_update.contract_length = contract_length
            user_to_update.salary = salary
            user_to_update.salary_per = salary_per
            user_to_update.job_desc = job_desc

            if image:
                user_to_update.filename=image.filename
                user_to_update.data=image.read()
            db.session.commit()
            flash("You have successfully posted you job ad",'success')
            return redirect('/requests')

@employers.route('/delete_history/<int:id>')
def delete_history(id):
    del_form = JOB_ADS_database.query.get_or_404(id)
    try:
        db.session.delete(del_form)
        db.session.commit()
        return redirect('/requests')

    except:
        return "<h1>ERROR 404</h1>"
    
@employers.route('/deactivate/<int:id>')
def deactivate(id):
    job_ab = JOB_ADS_database.query.get_or_404(id)
    job_ab.visibility = 0
    db.session.commit()
    return redirect('/requests')

@employers.route('/activate/<int:id>')
def activate(id):
    job_ab = JOB_ADS_database.query.get_or_404(id)
    job_ab.visibility = 1
    db.session.commit()
    return redirect('/requests')
