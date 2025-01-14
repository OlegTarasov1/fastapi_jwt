from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Reader(Base):
    __tablename__ = 'readers'

    id: Mapped[int] = mapped_column(primary_key = True) 
    username: Mapped[str]
    password: Mapped[bytes]
    is_admin: Mapped[bool] = mapped_column(server_default = 'FALSE')