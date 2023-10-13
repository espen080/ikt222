"""
Module containing database models
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the one-to-many relationship between User and Post
    posts = relationship('Post', back_populates='user')


class Post(BaseModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

    # Define a foreign key relationship to the User table
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define the many-to-one relationship between Post and User
    user = relationship('User', back_populates='posts')
