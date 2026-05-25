from flask import Blueprint, render_template, request, \
    redirect, url_for, session, flash
from app.models import FoodItem, Order, OrderItem, db

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def view_cart():
    cart_items = session.get('cart', {})
    foods = []
    total = 0
    for food_id, qty in cart_items.items():
        food = FoodItem.query.get(int(food_id))
        if food:
            subtotal = food.price * qty
            total += subtotal
            foods.append({
                'food': food,
                'qty': qty,
                'subtotal': subtotal
            })
    return render_template('cart.html',
                           foods=foods,
                           total=total)

@cart.route('/cart/add/<int:food_id>', methods=['POST'])
def add_to_cart(food_id):
    cart_items = session.get('cart', {})
    food_id_str = str(food_id)
    if food_id_str in cart_items:
        cart_items[food_id_str] += 1
    else:
        cart_items[food_id_str] = 1
    session['cart'] = cart_items
    flash('Cart এ যোগ হয়েছে! ✅', 'success')
    return redirect(url_for('shop.menu'))

@cart.route('/cart/remove/<int:food_id>')
def remove_from_cart(food_id):
    cart_items = session.get('cart', {})
    cart_items.pop(str(food_id), None)
    session['cart'] = cart_items
    return redirect(url_for('cart.view_cart'))

@cart.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart_items = session.get('cart', {})
        if not cart_items:
            flash('Cart ফাঁকা আছে!', 'danger')
            return redirect(url_for('cart.view_cart'))
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        payment = request.form.get('payment_method')
        total = 0

        # Guest user হিসেবে order নেবো
        from app.models import User
        from werkzeug.security import generate_password_hash
        guest = User.query.filter_by(
            email=f"{phone}@guest.com"
        ).first()
        if not guest:
            guest = User(
                name=name,
                email=f"{phone}@guest.com",
                phone=phone,
                password=generate_password_hash("guest"),
                is_admin=False
            )
            db.session.add(guest)
            db.session.flush()

        order = Order(
            user_id=guest.id,
            total=0,
            payment_method=payment,
            delivery_address=address,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()

        for food_id, qty in cart_items.items():
            food = FoodItem.query.get(int(food_id))
            if food:
                total += food.price * qty
                item = OrderItem(
                    order_id=order.id,
                    food_id=food.id,
                    quantity=qty,
                    price=food.price
                )
                db.session.add(item)

        order.total = total
        db.session.commit()
        session['cart'] = {}
        flash('অর্ডার সফল হয়েছে! 🎉', 'success')
        return redirect(url_for(
            'cart.order_success',
            order_id=order.id
        ))
    return render_template('checkout.html')

@cart.route('/order/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)