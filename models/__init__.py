from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
