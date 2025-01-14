from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ForeignKey, String, Integer, Column, Table
from typing import Annotated
import datetime
from .base import Base

intpk = Annotated[int, mapped_column(primary_key = True)] 


class Books(Base):
    __tablename__ = 'books'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))
    date: Mapped[datetime.date] = mapped_column(default = datetime.date.today())
    authors: Mapped[list['Authors']] = relationship(secondary = 'auth_books_table', back_populates = 'books')
    # genres
    in_store: Mapped[int] = mapped_column(default = 0)



class Authors(Base):
    __tablename__ = 'authors'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime.date | None] = mapped_column(default = None)

    books: Mapped[list['Books']] = relationship(secondary = 'auth_books_table', back_populates = 'authors')

auth_books_table = Table(
    'auth_books_table',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key = True),
    Column('author_id', ForeignKey('authors.id'), primary_key = True)
)

