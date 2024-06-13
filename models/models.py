from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    # Email validation is done in the schema
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )
    password: Mapped[str] = mapped_column(String(100))
    posts: Mapped[list["Posts"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )


class Posts(Base):
    __tablename__ = "posts"

    postID: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    post: Mapped[str] = mapped_column(String(1000))
    user_email: Mapped[str] = mapped_column(
        ForeignKey("users.email", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship(back_populates="posts")
