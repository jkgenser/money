from app import db
from sqlalchemy.dialects.postgresql import JSON


class Articles(db.Model):
    __tablename__ = 'articles'

    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    pub_date = db.Column(db.Date())
    author = db.Column(db.String())
    author_url = db.Column(db.String())
    article_url = db.Column(db.String())
    covered = db.Column(JSON)
    summary = db.Column(JSON)
    body = db.Column(JSON)
    tags = db.Column(JSON) # not sure what field type it is going to be yet, JSON for now
    prim_topic = db.Column(db.String())




    # def __init__(self, url, result_all, result_no_stop_words):
    #     self.url = url
    #     self.result_all = result_all
    #     self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<article_id {}>'.format(self.article_id)