import os
from flask import Blueprint, render_template, \
    request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import FoodItem, Order, User, db
from functools import wraps
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_url = '/static/images/' + filename
        food = FoodItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=image_url
        )
        db.session.add(food)
        db.session.commit()
        flash('খাবার যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_food.html')

@admin.route('/admin/food/edit/<int:food_id>',
             methods=['GET', 'POST'])
@login_required
@admin_required
def edit_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    if request.method == 'POST':
        food.name = request.form.get('name')
        food.description = request.form.get('description')
        food.price = float(request.form.get('price'))
        food.category = request.form.get('category')
        food.is_available = 'is_available' in request.form
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                food.image_url = '/static/images/' + filename
        db.session.commit()
        flash('খাবার আপডেট হয়েছে! ✅', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_food.html', food=food)

@admin.route('/admin/food/delete/<int:food_id>',
             methods=['POST'])
@login_required
@admin_required
def delete_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('খাবার মুছে গেছে! ✅', 'success')
    return redirect(url_for('admin.dashboard'))

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
@admin.route('/admin/craft')
@login_required
@admin_required
def craft_dashboard():
    from app.models import CraftItem
    items = CraftItem.query.all()
    return render_template('admin/craft_dashboard.html',
                           items=items)

@admin.route('/admin/craft/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_craft():
    if request.method == 'POST':
        from app.models import CraftItem
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_url = '/static/images/' + filename
        item = CraftItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=image_url
        )
        db.session.add(item)
        db.session.commit()
        flash('Craft Item যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.craft_dashboard'))
    return render_template('admin/add_craft.html')

@admin.route('/admin/craft/edit/<int:item_id>',
             methods=['GET', 'POST'])
@login_required
@admin_required
def edit_craft(item_id):
    from app.models import CraftItem
    item = CraftItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))
        item.category = request.form.get('category')
        item.is_available = 'is_available' in request.form
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                item.image_url = '/static/images/' + filename
        db.session.commit()
        flash('Craft Item আপডেট হয়েছে! ✅', 'success')
        return redirect(url_for('admin.craft_dashboard'))
    return render_template('admin/edit_craft.html', item=item)

@admin.route('/admin/craft/delete/<int:item_id>',
             methods=['POST'])
@login_required
@admin_required
def delete_craft(item_id):
    from app.models import CraftItem
    item = CraftItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Craft Item মুছে গেছে! ✅', 'success')
    return redirect(url_for('admin.craft_dashboard'))