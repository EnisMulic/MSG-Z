"""add/drop pk youtube

Revision ID: 24cc81d266c7
Revises: 11503172cc9a
Create Date: 2020-01-10 09:04:36.160412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24cc81d266c7'
down_revision = '11503172cc9a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('Youtube_pkey', 'Youtube', type_='primary')
    op.create_primary_key("Yotube_pkey", "Youtube", ["Id"])


def downgrade():
    pass
