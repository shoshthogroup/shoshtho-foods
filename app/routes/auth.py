from flask import Blueprint, render_template, \
    request, redirect, url_for, flash
from flask_login import login_user, logout_user, \
    login_required, current_user
from werkzeug.security import generate_password_hash, \
    check_password_hash
from app.models import User, db
from app import limiter

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        # ── Validation ──
        if len(password) < 6:
            flash('Password কমপক্ষে ৬ অক্ষরের হতে হবে!',
                  'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('এই Email আগে থেকে আছে!', 'danger')
            return redirect(url_for('auth.register'))

        hashed = generate_password_hash(
            password, method='pbkdf2:sha256')
        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration সফল! Login করুন।', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(
                user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('স্বাগতম! ✅', 'success')
            return redirect(next_page or
                            url_for('shop.home'))
        flash('Email বা Password ভুল!', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout হয়ে গেছে।', 'info')
    return redirect(url_for('shop.home'))