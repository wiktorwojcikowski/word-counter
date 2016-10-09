"""create word table

Revision ID: 3e55fe4a704a
Revises: 
Create Date: 2016-10-09 14:46:37.170821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e55fe4a704a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'word',
        sa.Column('key', sa.String(32), primary_key=True),
        sa.Column('hash', sa.String(50), nullable=False),
        sa.Column('counter', sa.Integer()),
    )
    pass


def downgrade():
    op.drop_table('word')
    pass
