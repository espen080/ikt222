"""
Module containing database models
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    locked_to = Column(DateTime, default=None)

    # Define the one-to-many relationship between User and Post
    posts = relationship('Post', back_populates='user', lazy='subquery')
    logins = relationship('Login', back_populates='user', lazy='subquery')


class Post(BaseModel):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(String)
    modified_at = Column(String, default="")

    # Define a foreign key relationship to the User table
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define the many-to-one relationship between Post and User
    user = relationship('User', back_populates='posts', lazy='subquery')

class Login(BaseModel):
    __tablename__ = 'logins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime)

    # Define the many-to-one relationship between Login and User
    user = relationship('User', back_populates='logins', lazy='subquery')
