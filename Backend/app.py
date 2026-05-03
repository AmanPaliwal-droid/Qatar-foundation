from flask import Flask, render_template, redirect, url_for, request
from extensions import db, bcrypt
from datetime import timedelta
import os
import sys

# ── Path setup ───────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))   # .../backend/
ROOT_DIR      = os.path.dirname(BASE_DIR)                    # repo root
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
STATIC_DIR    = os.path.join(ROOT_DIR, 'static')

# Make sure backend/ modules (extensions, models) are importable from routes/
sys.path.insert(0, BASE_DIR)

def create_app():
    app = Flask(
        __name__,
        template_folder=TEMPLATES_DIR,   # repo_root/templates/
        static_folder=STATIC_DIR,        # repo_root/static/
    )

    # ── Config ──────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'qf-admin-dev-secret-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "qf_admin.db")}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Remember-Me session lasts 30 days; non-persistent sessions end with the browser
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    app.config['SESSION_COOKIE_HTTPONLY']    = True
    app.config['SESSION_COOKIE_SAMESITE']    = 'Lax'

    # ── Extensions ──────────────────────────────────────────────────────
    db.init_app(app)
    bcrypt.init_app(app)

    # ── Blueprints ──────────────────────────────────────────────────────
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
        return render_template('admin.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
