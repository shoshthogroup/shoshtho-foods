from flask import Blueprint, render_template, \
    request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import FoodItem, Order, User, db
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access দরকার!', 'danger')
            return redirect(url_for('shop.home'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/admin')
@login_required
@admin_required
def dashboard():
    foods = FoodItem.query.all()
    orders = Order.query.order_by(
        Order.created_at.desc()).all()
    users = User.query.all()
    return render_template('admin/dashboard.html',
                         foods=foods,
                         orders=orders,
                         users=users)

@admin.route('/admin/food/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_food():
    if request.method == 'POST':
        food = FoodItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=request.form.get('image_url')
        )
        db.session.add(food)
        db.session.commit()
        flash('খাবার যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_food.html')

@admin.route('/admin/order/<int:order_id>/update',
             methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form.get('status')
    db.session.commit()
    flash('Order status আপডেট হয়েছে!', 'success')
    return redirect(url_for('admin.dashboard'))