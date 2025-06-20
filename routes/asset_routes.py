
from flask import Blueprint, request, jsonify
from extensions import db
from models import Asset
from schemas import AssetSchema

asset_bp = Blueprint('asset_bp', __name__)
asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)

@asset_bp.route('/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    try:
        valid_data = asset_schema.load(data)
    except Exception as err:
        return jsonify({"error": str(err)}), 400

    asset = Asset(**valid_data)
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 201

@asset_bp.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    return jsonify(assets_schema.dump(assets)), 200

@asset_bp.route('/assets/<int:id>', methods=['PATCH'])
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    data = request.get_json()
    errors = asset_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify(asset_schema.dump(asset)), 200
