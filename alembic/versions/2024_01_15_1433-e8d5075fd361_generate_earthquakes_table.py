"""generate earthquakes table

Revision ID: e8d5075fd361
Revises: abb6320a6255
Create Date: 2024-01-15 14:33:22.892305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP, FLOAT
from sqlalchemy.sql.functions import current_timestamp
from geoalchemy2 import Geometry;


# revision identifiers, used by Alembic.
revision: str = 'e8d5075fd361'
down_revision: Union[str, None] = 'abb6320a6255'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'earthquakes',
        Column('id', INTEGER, autoincrement=True, primary_key=True, nullable=False),
        Column('providerId', VARCHAR(100)),
        Column('date', TIMESTAMP, nullable=False),
        Column('depth', FLOAT),
        Column('magnitude', FLOAT, nullable=False),
        Column('type', VARCHAR(100)),
        Column('coordinates', Geometry('POINT')),
        Column('modified', TIMESTAMP, server_onupdate=current_timestamp(), server_default=current_timestamp()),
        Column('created', TIMESTAMP, server_default=current_timestamp(), nullable=False)
    )

    op.execute('''
        DROP TRIGGER IF EXISTS earthquakes_moddatetime ON earthquakes;
        CREATE TRIGGER earthquakes_moddatetime
        BEFORE UPDATE ON earthquakes
        FOR EACH ROW
        EXECUTE PROCEDURE moddatetime (modified);
    ''')


def downgrade() -> None:
    op.drop_table('earthquakes')
    op.execute('DROP TRIGGER IF EXISTS earthquakes_moddatetime ON earthquakes;')
