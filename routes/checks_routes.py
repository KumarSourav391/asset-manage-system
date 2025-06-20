
from flask import Blueprint, jsonify
from extensions import db
from models import Asset, Notification, Violation
from datetime import datetime, timedelta

check_bp = Blueprint('check_bp', __name__)

@check_bp.route('/run-checks', methods=['POST'])
def run_checks():
    now = datetime.utcnow()
    fifteen_minutes = timedelta(minutes=15)

    assets = Asset.query.all()
    for asset in assets:
        if 0 <= (asset.service_time - now).total_seconds() <= fifteen_minutes.total_seconds():
            n = Notification(asset_id=asset.id, message="Service time is near")
            db.session.add(n)

        if 0 <= (asset.expiration_time - now).total_seconds() <= fifteen_minutes.total_seconds():
            n = Notification(asset_id=asset.id, message="Expiration time is near")
            db.session.add(n)

        if now > asset.service_time and not asset.serviced:
            v = Violation(asset_id=asset.id, issue="Service overdue")
            db.session.add(v)

        if now > asset.expiration_time:
            v = Violation(asset_id=asset.id, issue="Asset expired")
            db.session.add(v)

    db.session.commit()
    return jsonify({"message": "Checks completed"}), 200
