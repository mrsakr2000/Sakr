from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import Invoice
from .. import db

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/ipn', methods=['POST'])
def paypal_ipn():
    data = request.form
    txn_id = data.get('txn_id')
    if Invoice.query.filter_by(paypal_txn=txn_id).first():
        return 'OK'
    invoice = Invoice(paypal_txn=txn_id, amount=float(data.get('mc_gross', 0)), user_id=1)
    db.session.add(invoice)
    db.session.commit()
    return 'OK'

@payments_bp.route('/invoices')
@login_required
def user_invoices():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': i.id, 'txn': i.paypal_txn, 'amount': i.amount} for i in invoices])
