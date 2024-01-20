"""add foreign key from earthquakes to country

Revision ID: 1272bbe951fb
Revises: e8d5075fd361
Create Date: 2024-01-20 16:22:21.426480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1272bbe951fb'
down_revision: Union[str, None] = 'e8d5075fd361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('earthquakes', sa.Column('countryId', sa.INTEGER, sa.ForeignKey('countries.id'), nullable=True, server_default = sa.Null()))


def downgrade() -> None:
    op.drop_column('earthquakes', 'countryId')
