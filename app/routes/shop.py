from flask import Blueprint, render_template, request
from app.models import FoodItem, db

shop = Blueprint('shop', __name__)

@shop.route('/')
def home():
    return render_template('index.html')

@shop.route('/menu')
def menu():
    category = request.args.get('category')
    if category:
        foods = FoodItem.query.filter_by(
            is_available=True,
            category=category
        ).all()
    else:
        foods = FoodItem.query.filter_by(
            is_available=True
        ).all()
    categories = db.session.query(
        FoodItem.category
    ).distinct().all()
    return render_template('menu.html',
                           foods=foods,
                           categories=categories)

@shop.route('/menu/<int:food_id>')
def food_detail(food_id):
    food = FoodItem.query.get_or_404(food_id)
    return render_template('food_detail.html', food=food)