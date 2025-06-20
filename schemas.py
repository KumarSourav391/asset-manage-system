
from marshmallow import Schema, fields, validate

class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    service_time = fields.DateTime(required=True)
    expiration_time = fields.DateTime(required=True)
    serviced = fields.Bool()

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    asset_id = fields.Int()
    message = fields.Str()
    created_at = fields.DateTime()

class ViolationSchema(Schema):
    id = fields.Int(dump_only=True)
    asset_id = fields.Int()
    issue = fields.Str()
    created_at = fields.DateTime()
