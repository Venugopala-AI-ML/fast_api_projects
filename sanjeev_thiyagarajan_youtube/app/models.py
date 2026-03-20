from sqlalchemy import TIME, Boolean, Column, ForeignKey, Index, String, Integer, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


"""this line loading all the Post model"""

from app.database import Base


class Post(Base):
    __tablename__ = "new_posts"
    id = Column(Integer , primary_key=True, index=True, nullable=False)
    title = Column(String , index=True, nullable=False)
    content = Column(String , index=True, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    phone_number = Column(String, nullable=True)

    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("new_posts.id", ondelete="CASCADE"), primary_key=True)
    user = relationship("User")
    post = relationship("Post")

