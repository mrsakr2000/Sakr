from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import VPS
from .. import db
from ..contabo import ContaboAPI
from ..email_utils import send_email

vps_bp = Blueprint('vps', __name__)
api = ContaboAPI()

@vps_bp.route('/plans')
@login_required
def list_plans():
    plans = api.list_plans()
    return jsonify(plans)

@vps_bp.route('/create', methods=['POST'])
@login_required
def create_vps():
    data = request.json
    result = api.create_vps(data['plan_id'], data['region'], data['os_id'])
    vps = VPS(
        contabo_id=result['id'],
        plan=data.get('plan_name', ''),
        status=result.get('status', ''),
        ip_address=result.get('publicIp', ''),
        owner=current_user
    )
    db.session.add(vps)
    db.session.commit()
    send_email('Your VPS is ready', [current_user.email], f"VPS ID: {vps.contabo_id}\nIP: {vps.ip_address}")
    return jsonify({'message': 'VPS created', 'vps_id': vps.contabo_id})

@vps_bp.route('/')
@login_required
def user_vps_list():
    vps_list = [
        {
            'id': v.id,
            'contabo_id': v.contabo_id,
            'plan': v.plan,
            'status': v.status,
            'ip_address': v.ip_address,
        } for v in current_user.vps
    ]
    return jsonify(vps_list)

@vps_bp.route('/<int:vps_id>')
@login_required
def vps_detail(vps_id):
    vps = VPS.query.get_or_404(vps_id)
    if vps.owner != current_user:
        return jsonify({'message': 'Forbidden'}), 403
    info = api.get_vps(vps.contabo_id)
    return jsonify(info)
