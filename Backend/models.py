from extensions import db
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reset_tokens = db.relationship('PasswordResetToken', backref='admin', lazy=True,
                                   cascade='all, delete-orphan')
    opportunities = db.relationship('Opportunity', backref='admin', lazy=True,
                                cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Admin {self.email}>'


class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    future_opportunities = db.Column(db.Text, nullable=False)
    max_applicants = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'start_date': self.start_date,
            'description': self.description,
            'skills': [s.strip() for s in self.skills.split(',') if s.strip()],
            'category': self.category,
            'future_opportunities': self.future_opportunities,
            'max_applicants': self.max_applicants,
        }


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f'<ResetToken admin_id={self.admin_id} expires={self.expires_at}>'
