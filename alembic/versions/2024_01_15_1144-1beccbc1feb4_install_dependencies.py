"""install dependencies

Revision ID: 1beccbc1feb4
Revises: 
Create Date: 2024-01-15 11:44:05.470071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1beccbc1feb4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION postgis;')
    op.execute('CREATE EXTENSION postgis_topology;')
    op.execute('CREATE EXTENSION moddatetime;')
    
def downgrade() -> None:
    op.execute('DROP EXTENSION IF EXISTS postgis_topology;')
    op.execute('DROP EXTENSION IF EXISTS postgis;')
    op.execute('DROP EXTENSION IF EXISTS moddatetime;')
