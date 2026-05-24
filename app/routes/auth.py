from flask import Blueprint, render_template, \
    request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, \
    check_password_hash
from app.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('এই Email আগে থেকে আছে!', 'danger')
            return redirect(url_for('auth.register'))
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, 
                   phone=phone, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registration সফল! এখন Login করো।', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('স্বাগতম! Login সফল ✅', 'success')
            return redirect(url_for('shop.home'))
        flash('Email বা Password ভুল!', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout হয়ে গেছে।', 'info')
    return redirect(url_for('shop.home'))