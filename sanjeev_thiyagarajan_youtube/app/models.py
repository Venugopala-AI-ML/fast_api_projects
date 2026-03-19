import email

from database import Base, engine
from sqlalchemy import TIME, Boolean, Column, ForeignKey, Index, String, Integer, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


"""this line loading all the Post model"""
Base.metadata.create_all(bind=engine)




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



