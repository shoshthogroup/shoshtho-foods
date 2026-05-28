from flask import Blueprint, render_template, request
from app.models import FoodItem, CraftItem, \
    Banner, BlogPost, db

shop = Blueprint('shop', __name__)

def get_blogs():
    try:
        return BlogPost.query.order_by(
            BlogPost.created_at.desc()).limit(5).all()
    except:
        return []

@shop.app_context_processor
def inject_globals():
    return dict(get_blogs=get_blogs)

@shop.route('/')
def home():
    return render_template('index.html')

@shop.route('/menu')
def menu():
    sub = request.args.get('sub')
    if sub:
        foods = FoodItem.query.filter_by(
            is_available=True,
            sub_category=sub
        ).order_by(FoodItem.sort_order).all()
    else:
        foods = FoodItem.query.filter_by(
            is_available=True
        ).order_by(FoodItem.sort_order).all()

    # Banners from Admin
    sliders = Banner.query.filter_by(
        page='food',
        banner_type='slider',
        is_active=True
    ).order_by(Banner.sort_order).all()

    minis = Banner.query.filter_by(
        page='food',
        banner_type='mini',
        is_active=True
    ).order_by(Banner.sort_order).limit(2).all()

    blogs = get_blogs()

    return render_template('menu.html',
                           foods=foods,
                           sliders=sliders,
                           minis=minis,
                           blogs=blogs,
                           current_sub=sub)

@shop.route('/craft')
def craft():
    category = request.args.get('category')
    if category:
        items = CraftItem.query.filter_by(
            is_available=True,
            category=category
        ).order_by(CraftItem.sort_order).all()
    else:
        items = CraftItem.query.filter_by(
            is_available=True
        ).order_by(CraftItem.sort_order).all()

    sliders = Banner.query.filter_by(
        page='craft',
        banner_type='slider',
        is_active=True
    ).order_by(Banner.sort_order).all()

    minis = Banner.query.filter_by(
        page='craft',
        banner_type='mini',
        is_active=True
    ).order_by(Banner.sort_order).limit(2).all()

    return render_template('craft.html',
                           items=items,
                           sliders=sliders,
                           minis=minis,
                           current_cat=category)

@shop.route('/blog')
def blog():
    posts = BlogPost.query.order_by(
        BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@shop.route('/education')
def education():
    return render_template('education.html')