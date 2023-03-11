from marshmallow import Schema, fields


class PageRequestSchema(Schema):
    url = fields.Str(required=True)


class PageResponseSchema(Schema):
    domain_name = fields.Str(required=True)
    final_status_code = fields.Int(required=True)
    final_url = fields.Str(required=True)
    status_code = fields.Int(required=True)
    title = fields.Str(required=True)
    url = fields.Str(required=True)


class DomainRequestSchema(Schema):
    domain = fields.Str(required=True)


class DomainResponseSchema(Schema):
    active_page_count = fields.Int(required=True)
    total_page_count = fields.Int(required=True)
    url_list = fields.List(fields.String(), required=True)
