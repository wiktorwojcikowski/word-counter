import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init_db(engine):
  Base.metadata.create_all(bind=engine)

class Word(Base):
    __tablename__ = 'word'

    key = sa.Column('key', sa.String(32), primary_key=True)
    hash = sa.Column('hash', sa.String(50), nullable=False)
    counter = sa.Column('counter', sa.Integer())
