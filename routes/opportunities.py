from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Opportunity
from datetime import datetime

opp_bp = Blueprint('opportunities', __name__, url_prefix='/api/opportunities')

VALID_CATEGORIES = {'technology', 'business', 'design', 'marketing', 'data', 'other'}


def _require_login():
    """Returns (admin_id, None) if logged in, else (None, error_response)."""
    admin_id = session.get('admin_id')
    if not admin_id:
        return None, (jsonify({'success': False, 'message': 'Unauthorised. Please log in.'}), 401)
    return admin_id, None


def _validate_fields(data):
    """Validate all required fields. Returns dict of errors (empty = valid)."""
    errors = {}
    required = ['name', 'duration', 'start_date', 'description', 'skills', 'category', 'future_opportunities']
    labels   = {
        'name': 'Opportunity Name',
        'duration': 'Duration',
        'start_date': 'Start Date',
        'description': 'Description',
        'skills': 'Skills to Gain',
        'category': 'Category',
        'future_opportunities': 'Future Opportunities',
    }
    for field in required:
        val = (data.get(field) or '').strip()
        if not val:
            errors[field] = f'{labels[field]} is required.'

    if 'category' not in errors:
        if data.get('category', '').strip() not in VALID_CATEGORIES:
            errors['category'] = 'Please select a valid category.'

    max_app = data.get('max_applicants')
    if max_app not in (None, ''):
        try:
            v = int(max_app)
            if v < 1:
                errors['max_applicants'] = 'Maximum applicants must be at least 1.'
        except (ValueError, TypeError):
            errors['max_applicants'] = 'Maximum applicants must be a whole number.'

    return errors


# ─────────────────────────────────────────────
# US-2.1  LIST — all opportunities for this admin
# ─────────────────────────────────────────────
@opp_bp.route('', methods=['GET'])
def list_opportunities():
    admin_id, err = _require_login()
    if err:
        return err

    opps = (Opportunity.query
            .filter_by(admin_id=admin_id)
            .order_by(Opportunity.created_at.desc())
            .all())

    return jsonify({'success': True, 'opportunities': [o.to_dict() for o in opps]}), 200


# ─────────────────────────────────────────────
# US-2.2  CREATE a new opportunity
# ─────────────────────────────────────────────
@opp_bp.route('', methods=['POST'])
def create_opportunity():
    admin_id, err = _require_login()
    if err:
        return err

    data = request.get_json(force=True)
    errors = _validate_fields(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    max_app = data.get('max_applicants')
    max_app = int(max_app) if max_app not in (None, '') else None

    opp = Opportunity(
        admin_id=admin_id,
        name=data['name'].strip(),
        duration=data['duration'].strip(),
        start_date=data['start_date'].strip(),
        description=data['description'].strip(),
        skills=data['skills'].strip(),
        category=data['category'].strip(),
        future_opportunities=data['future_opportunities'].strip(),
        max_applicants=max_app,
    )
    db.session.add(opp)
    db.session.commit()

    return jsonify({'success': True, 'opportunity': opp.to_dict()}), 201


# ─────────────────────────────────────────────
# US-2.4  GET single opportunity details
# ─────────────────────────────────────────────
@opp_bp.route('/<int:opp_id>', methods=['GET'])
def get_opportunity(opp_id):
    admin_id, err = _require_login()
    if err:
        return err

    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'success': False, 'message': 'Opportunity not found.'}), 404

    return jsonify({'success': True, 'opportunity': opp.to_dict()}), 200


# ─────────────────────────────────────────────
# US-2.5  UPDATE / EDIT
# ─────────────────────────────────────────────
@opp_bp.route('/<int:opp_id>', methods=['PUT'])
def update_opportunity(opp_id):
    admin_id, err = _require_login()
    if err:
        return err

    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'success': False, 'message': 'Opportunity not found or access denied.'}), 404

    data = request.get_json(force=True)
    errors = _validate_fields(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    max_app = data.get('max_applicants')
    max_app = int(max_app) if max_app not in (None, '') else None

    opp.name = data['name'].strip()
    opp.duration = data['duration'].strip()
    opp.start_date = data['start_date'].strip()
    opp.description = data['description'].strip()
    opp.skills = data['skills'].strip()
    opp.category = data['category'].strip()
    opp.future_opportunities = data['future_opportunities'].strip()
    opp.max_applicants = max_app
    opp.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({'success': True, 'opportunity': opp.to_dict()}), 200


# ─────────────────────────────────────────────
# US-2.6  DELETE
# ─────────────────────────────────────────────
@opp_bp.route('/<int:opp_id>', methods=['DELETE'])
def delete_opportunity(opp_id):
    admin_id, err = _require_login()
    if err:
        return err

    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'success': False, 'message': 'Opportunity not found or access denied.'}), 404

    db.session.delete(opp)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Opportunity deleted successfully.'}), 200
