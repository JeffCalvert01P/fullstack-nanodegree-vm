import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
 
class Users(Base):
    __tablename__ = 'users'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email_addr = Column(String(100), nullable=False)

    @property
    def serialize(self):
        return {
	    'id' : self.id,
            'name' : self.name,
	    'email_addr' : self.email_addr
	    }
 
class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category) 
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship(Users)
    filetype = Column(String(4))


    @property
    def serialize(self):
        return {
	    'name' : self.name,
	    'id' : self.id,
	    'description' : self.description,
	    'price' : self.price,
	    'category_id' : self.category_id,
	    'user_id' : self.user_id
	    }
	
engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)
