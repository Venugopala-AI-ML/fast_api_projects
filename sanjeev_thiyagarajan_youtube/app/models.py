from sqlalchemy import TIME, Boolean, Column, ForeignKey, Index, String, Integer, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


"""this line loading all the Post model"""

from app.database import Base



class Post(Base):
    __tablename__ = "new_posts"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("app.models.User", back_populates="posts")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("app.models.Post", back_populates="owner")  # ✅ added this

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {'extend_existing': True}  # ✅ added this
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("new_posts.id", ondelete="CASCADE"), primary_key=True)  # ✅ "new_posts" not "posts"