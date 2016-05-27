from app import db
from models import Article



query = Article.query.filter(Article.title !=  None).all()
print('done')


# Get unique list of all covered securities
covered = set()


# Get unique list of all tagged topics