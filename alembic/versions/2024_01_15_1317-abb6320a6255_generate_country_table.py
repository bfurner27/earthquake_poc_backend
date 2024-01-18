"""generate country table

Revision ID: abb6320a6255
Revises: 1beccbc1feb4
Create Date: 2024-01-15 13:17:07.055195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.sql.functions import current_timestamp
from geoalchemy2 import Geography;


# revision identifiers, used by Alembic.
revision: str = 'abb6320a6255'
down_revision: Union[str, None] = '1beccbc1feb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'countries',
        Column('id', INTEGER, autoincrement=True, primary_key=True, nullable=False),
        Column('name', VARCHAR(150), nullable=False),
        Column('requestId', VARCHAR(100), nullable=False),
        Column('boundaries', Geography),
        Column('modified', TIMESTAMP, server_onupdate=current_timestamp(), server_default=current_timestamp()),
        Column('created', TIMESTAMP, server_default=current_timestamp(), nullable=False)
    )

    op.execute('''
        DROP TRIGGER IF EXISTS countries_moddatetime ON countries;
        CREATE TRIGGER countries_moddatetime
        BEFORE UPDATE ON countries
        FOR EACH ROW
        EXECUTE PROCEDURE moddatetime (modified);
    ''')


def downgrade() -> None:
    op.drop_table('countries')
    op.execute('DROP TRIGGER IF EXISTS countries_moddatetime ON countries;')
