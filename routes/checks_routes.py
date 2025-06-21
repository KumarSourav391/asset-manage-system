from flask import Blueprint, jsonify
from extensions import db
from models import Asset, Notification, Violation
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

check_bp = Blueprint('check_bp', __name__)

@check_bp.route('/run-checks', methods=['POST'])
def run_checks():
    now = datetime.utcnow()
    fifteen_minutes = timedelta(minutes=15)

    created_notifications = 0
    created_violations = 0

    assets = Asset.query.all()
    for asset in assets:
        if 0 <= (asset.service_time - now).total_seconds() <= fifteen_minutes.total_seconds():
            n = Notification(asset_id=asset.id, message="Service time is near")
            db.session.add(n)
            logger.info(f"Reminder: Service time near for Asset ID {asset.id}")
            created_notifications += 1

        if 0 <= (asset.expiration_time - now).total_seconds() <= fifteen_minutes.total_seconds():
            n = Notification(asset_id=asset.id, message="Expiration time is near")
            db.session.add(n)
            logger.info(f"Reminder: Expiration time near for Asset ID {asset.id}")
            created_notifications += 1

        if now > asset.service_time and not asset.serviced:
            v = Violation(asset_id=asset.id, issue="Service overdue")
            db.session.add(v)
            logger.warning(f"Violation: Service overdue for Asset ID {asset.id}")
            created_violations += 1

        if now > asset.expiration_time:
            v = Violation(asset_id=asset.id, issue="Asset expired")
            db.session.add(v)
            logger.warning(f"Violation: Asset expired for Asset ID {asset.id}")
            created_violations += 1

    db.session.commit()
    logger.info(f"Checks completed: {created_notifications} notifications, {created_violations} violations.")
    return jsonify({
        "message": "Checks completed",
        "notifications_created": created_notifications,
        "violations_created": created_violations
    }), 200