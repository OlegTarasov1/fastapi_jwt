"""empty message

Revision ID: bee10a6acd4f
Revises: 75ee715f7647
Create Date: 2025-01-11 15:01:10.965753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bee10a6acd4f'
down_revision: Union[str, None] = '75ee715f7647'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('authors', 'birth_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('authors', 'birth_date',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
