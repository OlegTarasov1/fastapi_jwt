"""empty message

Revision ID: e2c84feb9eaf
Revises: d567d0fd3a22
Create Date: 2025-01-17 12:53:29.390162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e2c84feb9eaf'
down_revision: Union[str, None] = 'd567d0fd3a22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('readers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='readers_pkey'),
    sa.UniqueConstraint('username', name='readers_username_key')
    )
    # ### end Alembic commands ###
