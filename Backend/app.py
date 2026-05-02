from flask import Flask, render_template, redirect, url_for, request
from extensions import db, bcrypt
from datetime import timedelta
import os

def create_app():
    app = Flask(__name__)

    # ── Config ──────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'qf-admin-dev-secret-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///qf_admin.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Remember-Me session lasts 30 days; non-persistent sessions end with the browser
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

    # ── Extensions ──────────────────────────────────────────────────────
    db.init_app(app)
    bcrypt.init_app(app)

    # ── Blueprints ──────────────────────────────────────────────────────
    #from routes.auth import auth_bp
    #app.register_blueprint(auth_bp)
    from routes.auth import auth_bp
    from routes.opportunities import opp_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(opp_bp)

    # ── Create tables ───────────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    # ── Main route — serves the single-page UI ──────────────────────────
    @app.route('/')
    def index():
        return render_template('admin.html')

    # ── Reset-password page route (token arrives as query-param) ─────────
    @app.route('/reset-password')
    def reset_password_page():
        # The token is validated client-side via the API;
        # we just serve the same SPA and let JS handle it.
        return render_template('admin.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
