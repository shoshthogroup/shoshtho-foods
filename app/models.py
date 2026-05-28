from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True,
                      nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user',
                             lazy=True)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    # Discount badge: New, Hot, -20%, etc.
    badge = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100))
    sub_category = db.Column(db.String(100))
    image_url = db.Column(db.String(300))
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)

class CraftItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    badge = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100))
    image_url = db.Column(db.String(300))
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(300))
    button_text = db.Column(db.String(100))
    button_link = db.Column(db.String(200))
    image_url = db.Column(db.String(300))
    bg_color = db.Column(db.String(100),
                         default='linear-gradient(135deg,#1a3c5e,#2e86c1)')
    emoji = db.Column(db.String(10), default='🍽️')
    page = db.Column(db.String(50), default='food')
    # food or craft
    banner_type = db.Column(db.String(50),
                            default='slider')
    # slider or mini
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(100),
                         default='Health Tips')
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    payment_method = db.Column(db.String(50))
    delivery_address = db.Column(db.Text)
    order_type = db.Column(db.String(50), default='food')
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order',
                            lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('order.id'))
    food_id = db.Column(db.Integer,
                        db.ForeignKey('food_item.id'),
                        nullable=True)
    craft_id = db.Column(db.Integer,
                         db.ForeignKey('craft_item.id'),
                         nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    food = db.relationship('FoodItem')
    craft = db.relationship('CraftItem')