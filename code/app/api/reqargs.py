from webargs import fields, validate


some_get_args = {
    "type": fields.Int(required=True, validate=validate.OneOf([1, 2, 3, 4, 7])),
    "page": fields.Int(missing=1),
    "size": fields.Int(missing=10)
}

some_post_args = {
    "type": fields.Int(required=True, validate=validate.OneOf([1, 2, 3, 4, 7])),
    "name": fields.Str(required=True, validate=validate.Length(min=1))
}
