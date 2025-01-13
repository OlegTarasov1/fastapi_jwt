"""empty message

Revision ID: 35eae8ce8e8d
Revises: 245d0cd262a6
Create Date: 2025-01-11 10:48:07.789168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35eae8ce8e8d'
down_revision: Union[str, None] = '245d0cd262a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genres')
    op.drop_table('conn_table')
    op.drop_table('authors')
    op.drop_table('books')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('books_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('book_title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('published', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('in_store', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='books_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('authors',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('authors_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('bio', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='authors_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('conn_table',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], name='conn_table_author_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='conn_table_book_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='conn_table_pkey')
    )
    op.create_table('genres',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='genres_pkey')
    )
    # ### end Alembic commands ###
