import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import utils
Base = declarative_base()

def init_db(engine):
  Base.metadata.create_all(bind=engine)

class Word(Base):
    __tablename__ = 'word'

    key = sa.Column('key', sa.String(32), primary_key=True, nullable=False)
    token = sa.Column('token', sa.String(500), nullable=False)
    counter = sa.Column('counter', sa.Integer(), default=0)

    @property
    def word(self):
        return utils.decode_word(self.token)
