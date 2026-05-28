import os
from flask import Blueprint, render_template, \
    request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import FoodItem, CraftItem, Order, \
    User, Banner, BlogPost, db
from functools import wraps
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)
UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','webp'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return '/static/images/' + filename
    return ''

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access দরকার!', 'danger')
            return redirect(url_for('shop.home'))
        return f(*args, **kwargs)
    return decorated

# ── Dashboard ──
@admin.route('/admin')
@login_required
@admin_required
def dashboard():
    foods = FoodItem.query.order_by(
        FoodItem.sort_order).all()
    crafts = CraftItem.query.order_by(
        CraftItem.sort_order).all()
    orders = Order.query.order_by(
        Order.created_at.desc()).all()
    users = User.query.all()
    banners = Banner.query.all()
    blogs = BlogPost.query.order_by(
        BlogPost.created_at.desc()).all()
    return render_template('admin/dashboard.html',
                           foods=foods,
                           crafts=crafts,
                           orders=orders,
                           users=users,
                           banners=banners,
                           blogs=blogs)

# ══════════════════════════════
# FOOD MANAGEMENT
# ══════════════════════════════
@admin.route('/admin/food/add', methods=['GET','POST'])
@login_required
@admin_required
def add_food():
    if request.method == 'POST':
        image_url = save_image(request.files.get('image'))
        food = FoodItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            old_price=float(request.form.get('old_price'))
                if request.form.get('old_price') else None,
            badge=request.form.get('badge'),
            category=request.form.get('category'),
            sub_category=request.form.get('sub_category'),
            image_url=image_url,
            is_featured='is_featured' in request.form,
            sort_order=int(request.form.get('sort_order',0))
        )
        db.session.add(food)
        db.session.commit()
        flash('খাবার যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_food.html')

@admin.route('/admin/food/edit/<int:food_id>',
             methods=['GET','POST'])
@login_required
@admin_required
def edit_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    if request.method == 'POST':
        food.name = request.form.get('name')
        food.description = request.form.get('description')
        food.price = float(request.form.get('price'))
        food.old_price = float(
            request.form.get('old_price')) \
            if request.form.get('old_price') else None
        food.badge = request.form.get('badge')
        food.category = request.form.get('category')
        food.sub_category = request.form.get('sub_category')
        food.is_available = 'is_available' in request.form
        food.is_featured = 'is_featured' in request.form
        food.sort_order = int(
            request.form.get('sort_order', 0))
        img = save_image(request.files.get('image'))
        if img:
            food.image_url = img
        db.session.commit()
        flash('আপডেট হয়েছে! ✅', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_food.html',
                           food=food)

@admin.route('/admin/food/delete/<int:food_id>',
             methods=['POST'])
@login_required
@admin_required
def delete_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('মুছে গেছে! ✅', 'success')
    return redirect(url_for('admin.dashboard'))

# ══════════════════════════════
# CRAFT MANAGEMENT
# ══════════════════════════════
@admin.route('/admin/craft')
@login_required
@admin_required
def craft_dashboard():
    items = CraftItem.query.order_by(
        CraftItem.sort_order).all()
    return render_template('admin/craft_dashboard.html',
                           items=items)

@admin.route('/admin/craft/add', methods=['GET','POST'])
@login_required
@admin_required
def add_craft():
    if request.method == 'POST':
        image_url = save_image(request.files.get('image'))
        item = CraftItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            old_price=float(request.form.get('old_price'))
                if request.form.get('old_price') else None,
            badge=request.form.get('badge'),
            category=request.form.get('category'),
            image_url=image_url,
            is_featured='is_featured' in request.form,
            sort_order=int(request.form.get('sort_order',0))
        )
        db.session.add(item)
        db.session.commit()
        flash('Craft Item যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.craft_dashboard'))
    return render_template('admin/add_craft.html')

@admin.route('/admin/craft/edit/<int:item_id>',
             methods=['GET','POST'])
@login_required
@admin_required
def edit_craft(item_id):
    item = CraftItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))
        item.old_price = float(
            request.form.get('old_price')) \
            if request.form.get('old_price') else None
        item.badge = request.form.get('badge')
        item.category = request.form.get('category')
        item.is_available = 'is_available' in request.form
        item.is_featured = 'is_featured' in request.form
        item.sort_order = int(
            request.form.get('sort_order', 0))
        img = save_image(request.files.get('image'))
        if img:
            item.image_url = img
        db.session.commit()
        flash('আপডেট হয়েছে! ✅', 'success')
        return redirect(url_for('admin.craft_dashboard'))
    return render_template('admin/edit_craft.html',
                           item=item)

@admin.route('/admin/craft/delete/<int:item_id>',
             methods=['POST'])
@login_required
@admin_required
def delete_craft(item_id):
    item = CraftItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('মুছে গেছে! ✅', 'success')
    return redirect(url_for('admin.craft_dashboard'))

# ══════════════════════════════
# BANNER MANAGEMENT
# ══════════════════════════════
@admin.route('/admin/banner')
@login_required
@admin_required
def banner_dashboard():
    banners = Banner.query.order_by(
        Banner.sort_order).all()
    return render_template('admin/banner_dashboard.html',
                           banners=banners)

@admin.route('/admin/banner/add', methods=['GET','POST'])
@login_required
@admin_required
def add_banner():
    if request.method == 'POST':
        image_url = save_image(request.files.get('image'))
        banner = Banner(
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            button_text=request.form.get('button_text'),
            button_link=request.form.get('button_link'),
            image_url=image_url,
            bg_color=request.form.get('bg_color'),
            emoji=request.form.get('emoji'),
            page=request.form.get('page'),
            banner_type=request.form.get('banner_type'),
            sort_order=int(request.form.get('sort_order',0))
        )
        db.session.add(banner)
        db.session.commit()
        flash('Banner যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.banner_dashboard'))
    return render_template('admin/add_banner.html')

@admin.route('/admin/banner/delete/<int:bid>',
             methods=['POST'])
@login_required
@admin_required
def delete_banner(bid):
    banner = Banner.query.get_or_404(bid)
    db.session.delete(banner)
    db.session.commit()
    flash('Banner মুছে গেছে!', 'success')
    return redirect(url_for('admin.banner_dashboard'))

@admin.route('/admin/banner/toggle/<int:bid>',
             methods=['POST'])
@login_required
@admin_required
def toggle_banner(bid):
    banner = Banner.query.get_or_404(bid)
    banner.is_active = not banner.is_active
    db.session.commit()
    return redirect(url_for('admin.banner_dashboard'))

# ══════════════════════════════
# BLOG MANAGEMENT
# ══════════════════════════════
@admin.route('/admin/blog')
@login_required
@admin_required
def blog_dashboard():
    posts = BlogPost.query.order_by(
        BlogPost.created_at.desc()).all()
    return render_template('admin/blog_dashboard.html',
                           posts=posts)

@admin.route('/admin/blog/add', methods=['GET','POST'])
@login_required
@admin_required
def add_blog():
    if request.method == 'POST':
        image_url = save_image(request.files.get('image'))
        post = BlogPost(
            title=request.form.get('title'),
            content=request.form.get('content'),
            category=request.form.get('category'),
            image_url=image_url
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog Post যোগ হয়েছে! ✅', 'success')
        return redirect(url_for('admin.blog_dashboard'))
    return render_template('admin/add_blog.html')

@admin.route('/admin/blog/delete/<int:post_id>',
             methods=['POST'])
@login_required
@admin_required
def delete_blog(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog Post মুছে গেছে!', 'success')
    return redirect(url_for('admin.blog_dashboard'))

# ══════════════════════════════
# ORDER MANAGEMENT
# ══════════════════════════════
@admin.route('/admin/order/<int:order_id>/update',
             methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form.get('status')
    db.session.commit()
    flash('Order আপডেট হয়েছে!', 'success')
    return redirect(url_for('admin.dashboard'))