from .base import Base
from .models import Books
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Reader(Base):
    __tablename__ = 'readers'

    id: Mapped[int] = mapped_column(primary_key = True) 
    username: Mapped[str] = mapped_column(unique = True)
    password: Mapped[bytes]
    is_admin: Mapped[bool] = mapped_column(server_default = 'FALSE')
    
    books: Mapped[list['Books']] = relationship()