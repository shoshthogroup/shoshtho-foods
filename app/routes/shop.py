from flask import Blueprint, render_template, request
from app.models import FoodItem, CraftItem, db

shop = Blueprint('shop', __name__)

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
        ).all()
    else:
        foods = FoodItem.query.filter_by(
            is_available=True
        ).all()
    sub_categories = db.session.query(
        FoodItem.sub_category
    ).distinct().all()
    return render_template('menu.html',
                           foods=foods,
                           sub_categories=sub_categories,
                           current_sub=sub)

@shop.route('/craft')
def craft():
    category = request.args.get('category')
    if category:
        items = CraftItem.query.filter_by(
            is_available=True,
            category=category
        ).all()
    else:
        items = CraftItem.query.filter_by(
            is_available=True
        ).all()
    return render_template('craft.html',
                           items=items,
                           current_cat=category)

@shop.route('/education')
def education():
    return render_template('education.html')