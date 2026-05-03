from flask import Blueprint, request, jsonify, session
from extensions import db, bcrypt
from models import Admin, PasswordResetToken
from datetime import datetime, timedelta
import secrets
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def _valid_email(email):
    return bool(EMAIL_RE.match(email))


# ─────────────────────────────────────────────
# US-1.1  SIGN UP
# ─────────────────────────────────────────────
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(force=True)

    full_name       = (data.get('full_name') or '').strip()
    email           = (data.get('email') or '').strip().lower()
    password        = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''

    # ── field-level validation ──────────────────
    errors = {}

    if not full_name:
        errors['full_name'] = 'Full name is required.'

    if not email:
        errors['email'] = 'Email address is required.'
    elif not _valid_email(email):
        errors['email'] = 'Please enter a valid email address.'

    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters.'

    if not confirm_password:
        errors['confirm_password'] = 'Please confirm your password.'
    elif password and confirm_password and password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    # ── duplicate-email check ───────────────────
    if Admin.query.filter_by(email=email).first():
        return jsonify({
            'success': False,
            'errors': {'email': 'An account with this email already exists.'}
        }), 409

    # ── persist ────────────────────────────────
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    admin = Admin(full_name=full_name, email=email, password_hash=hashed)
    db.session.add(admin)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Account created successfully.'}), 201


# ─────────────────────────────────────────────
# US-1.2  LOGIN
# ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)

    email       = (data.get('email') or '').strip().lower()
    password    = data.get('password') or ''
    remember_me = bool(data.get('remember_me', False))

    # basic field presence
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Invalid email or password.'
        }), 401

    # lookup + bcrypt check (constant-time — never reveal which field is wrong)
    admin = Admin.query.filter_by(email=email).first()
    if not admin or not bcrypt.check_password_hash(admin.password_hash, password):
        return jsonify({
            'success': False,
            'message': 'Invalid email or password.'
        }), 401

    # ── session ────────────────────────────────
    session.permanent = remember_me          # True → 30-day cookie; False → browser-session cookie
    session['admin_id']    = admin.id
    session['admin_email'] = admin.email
    session['admin_name']  = admin.full_name

    return jsonify({
        'success': True,
        'message': 'Login successful.',
        'admin': {
            'email':     admin.email,
            'full_name': admin.full_name
        }
    }), 200


# ─────────────────────────────────────────────
# US-1.3  FORGOT PASSWORD
# ─────────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data  = request.get_json(force=True)
    email = (data.get('email') or '').strip().lower()

    # Always return the same message regardless of whether the email exists (privacy)
    GENERIC_MSG = 'If that email is registered, a reset link has been sent.'

    if not email or not _valid_email(email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    admin = Admin.query.filter_by(email=email).first()
    if admin:
        # Invalidate any existing unused tokens for this admin
        PasswordResetToken.query.filter_by(admin_id=admin.id, used=False).delete()
        db.session.flush()

        token      = secrets.token_urlsafe(48)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        reset_token = PasswordResetToken(
            admin_id   = admin.id,
            token      = token,
            expires_at = expires_at
        )
        db.session.add(reset_token)
        db.session.commit()

        # In production this would be emailed; for now we log it internally
        reset_url = f'http://localhost:5000/reset-password?token={token}'
        print(f'\n[RESET LINK] {admin.email} → {reset_url}\n', flush=True)

    return jsonify({'success': True, 'message': GENERIC_MSG}), 200


# ─────────────────────────────────────────────
# RESET PASSWORD  (consume the token)
# ─────────────────────────────────────────────
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data         = request.get_json(force=True)
    token_value  = (data.get('token') or '').strip()
    new_password = data.get('new_password') or ''

    if not token_value:
        return jsonify({'success': False, 'message': 'Reset token is missing.'}), 400

    record = PasswordResetToken.query.filter_by(token=token_value, used=False).first()

    if not record:
        return jsonify({'success': False, 'message': 'This reset link is invalid or has already been used.'}), 400

    if record.is_expired():
        return jsonify({'success': False, 'message': 'This reset link has expired. Please request a new one.'}), 400

    if len(new_password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters.'}), 400

    admin = Admin.query.get(record.admin_id)
    admin.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    record.used = True
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password reset successfully. You can now log in.'}), 200


# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Signed out successfully.'}), 200


# ─────────────────────────────────────────────
# SESSION CHECK  (called on page load)
# ─────────────────────────────────────────────
@auth_bp.route('/session', methods=['GET'])
def check_session():
    if 'admin_id' in session:
        return jsonify({
            'logged_in': True,
            'admin': {
                'email':     session.get('admin_email'),
                'full_name': session.get('admin_name')
            }
        }), 200
    return jsonify({'logged_in': False}), 200
