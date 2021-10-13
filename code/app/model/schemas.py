from library.utils import camelcase
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import SomeModel


class BaseSchema(SQLAlchemyAutoSchema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class SomeModelSchema(BaseSchema):
    fields.Integer(load_only=True)

    class Meta:
        model = SomeModel
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        include_fk = True
