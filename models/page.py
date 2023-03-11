from db import db


class PageModel(db.Model):
    __tablename__ = "page_data"

    id = db.Column(db.Integer, primary_key=True)
    final_url = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=False)
    final_status_code = db.Column(db.Integer, nullable=True)
    status_code = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    domain_name = db.Column(db.String(100), nullable=False)
