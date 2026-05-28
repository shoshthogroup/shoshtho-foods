from flask import Flask, render_template
from .models import db
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ── Extensions ──
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = \
        'Login করুন!'
    login_manager.login_message_category = 'warning'

    # ── Blueprints ──
    from .routes.auth import auth
    from .routes.shop import shop
    from .routes.cart import cart
    from .routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(shop)
    app.register_blueprint(cart)
    app.register_blueprint(admin)

    # ── Security Headers ──
    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = \
            'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = \
            '1; mode=block'
        response.headers['Referrer-Policy'] = \
            'strict-origin-when-cross-origin'
        return response

    # ── Custom Error Pages ──
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # ── Create Tables ──
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))