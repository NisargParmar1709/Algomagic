from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .models import db
from .models import User, UserSession
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .module import generate_otp, check_otp, mail_sender, forgot_mail_sender
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session_record = UserSession(user_id=user.id)
            db.session.add(session_record)
            db.session.commit()
            user = current_user
            session['first_name'] = current_user.first_name
            session['last_name'] = current_user.last_name
            return redirect(url_for('main.index'))
        return redirect(url_for('auth.login'))
    return render_template('/login.html')

 

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    otp_file = "instance/otp_data.json"
    pending_otp_file = "instance/panding_otp.json"

    if request.method == 'POST':
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        c_password = request.form["confirm-password"]

        errors = {}

        if len(name) < 2:
            errors["name_error"] = "Name is too short"
        if len(surname) < 2:
            errors["surname_error"] = "Surname is too short"
        if len(email) < 2:
            errors["email_error"] = "Email is too short"
        if password != c_password:
            errors["password_error"] = "Passwords do not match"
            
        # Add logic to save user to the database
        user = User.query.filter_by(email=email).first()
        if user:
            errors["exists_email_error"] = "Email already exists!"

        if errors:
            return render_template('signup.html', errors=errors)

        session['first_name'] = name
        session['surname'] = surname
        session['password'] = password
        
        otp = generate_otp(email=email, otp_file=otp_file)
        otp_status = check_otp(email=email, otp=otp,  otp_file=otp_file)

        if otp_status:
            mail_status = mail_sender(receiver_email=email, name=name, otp=otp)

            with open(otp_file, "r", encoding='utf-8') as f:
                otp_data = json.load(f)        

            if mail_status:
                otp_data[email] = {"otp": otp, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                with open(pending_otp_file, "w", encoding='utf-8') as f:
                    json.dump(otp_data, f)

                session['email'] = email
                return render_template('otp_verification.html')
    
    return render_template('signup.html')

@auth.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        # handle otp logic here
        
        pending_otp_file = "instance/panding_otp.json"

        with open(pending_otp_file, "r") as f:
            otp_data = json.load(f)

        for email in otp_data:
            if email == session['email']:

                first_digit = request.form['first_digit']
                second_digit = request.form['second_digit']
                third_digit = request.form['third_digit']
                fourth_digit = request.form['fourth_digit']

                fatch_otp = first_digit + second_digit + third_digit + fourth_digit
                fatch_otp = int(fatch_otp)

                if fatch_otp != otp_data[email]["otp"]:
                    name = session['first_name']
                    surname = session['surname']
                    password = session['password']

                    hashed_password = generate_password_hash(password)
                    session.pop("password", None)
                    new_user = User(email=email, first_name=name, last_name=surname, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()

                    session.pop("first_name", None)
                    session.pop("surname", None)

                    return redirect(url_for('main.index'))
                else:
                    return redirect(url_for('auth.otp_verification'))
    return render_template('otp_verification.html')

@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    otp_file = "instance/otp_data.json"
    pending_otp_file = "instance/panding_otp.json"
    
    print(request.method)
    
    if request.method == 'POST':
        # handle password reset logic here
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
        
            otp = generate_otp(email=email, otp_file=otp_file)
            otp_status = check_otp(email=email, otp=otp,  otp_file=otp_file)
            
            if otp_status:
                name = user.first_name
                mail_status = forgot_mail_sender(receiver_email=email, name=name, otp=otp)

                with open(otp_file, "r", encoding='utf-8') as f:
                    otp_data = json.load(f)        
                if mail_status:
                    otp_data[email] = {"otp": otp, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    with open(pending_otp_file, "w", encoding='utf-8') as f:
                        json.dump(otp_data, f)

                    session['email'] = email
                    return render_template('forgot.html', otp_sent=True)
                else:
                    return render_template('404.html'), 404
        else:
            errors = {}
            errors['not_exists_error'] = 'This email Not exsist in first signup please...'
            return render_template('forgot.html', error = errors)
        
        return redirect(url_for('auth.forgot'))
    return render_template('forgot.html')   

@auth.route('/forgot_otp_verify', methods=['GET', 'POST'])
def otp_verfiy():
    pending_otp_file = "instance/panding_otp.json"
    print(request.method)
    if request.method == 'POST':
        with open(pending_otp_file, "r") as f:
            otp_data = json.load(f)

        for email in otp_data:
            if email == request.form['email']:

                first_digit = request.form['first_digit']
                second_digit = request.form['second_digit']
                third_digit = request.form['third_digit']
                fourth_digit = request.form['fourth_digit']

                fatch_otp = first_digit + second_digit + third_digit + fourth_digit
                fatch_otp = int(fatch_otp)
                print(fatch_otp, otp_data[email]["otp"])
                if fatch_otp == int(otp_data[email]["otp"]):
                    user = User.query.filter_by(email=email).first()
                    print(user.password)
                    return render_template('forgot.html', otp_verified=True)
                else:
                    return render_template('forgot.html', )
    else:
        return render_template('forgot.html')

@auth.route('/change_password',  methods=['GET', 'POST'])
def change_password():
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password == confirm_password:
        user = User.query.filter_by(email=session['email']).first()
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        db.session.commit()
        return render_template('login.html')
    else:
        return 'Passwords do not match', 401

@auth.route('/logout')
@login_required
def logout():
    # handle logout logic here
    session_record = UserSession.query.filter_by(user_id=current_user.id, active=True).first()
    if session_record:
        session_record.logout_time = datetime.now()
        session_record.active = False
        db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))