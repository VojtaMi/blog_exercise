from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, Date
from flask_login import UserMixin
from typing import List
from datetime import date

# Create a new SQLAlchemy instance here and import it in app.py
db = SQLAlchemy()


# Base model
class Base(DeclarativeBase):
    pass


# BlogPost model
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)  # Store as Date
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Define the relationship with User
    author: Mapped["User"] = relationship(back_populates="posts")


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)

    # Define the relationship with BlogPost
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author", cascade="all, delete-orphan")