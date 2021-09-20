from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import JSON, SMALLINT, TIMESTAMP
from sqlalchemy_utils import EmailType,URLType
import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    nombre = Column(String)
    apellidos = Column(String)
    hashed_password = Column(String)
    visible_farms = Column(JSON)
    is_active = Column(Boolean,default=True)

    post = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    url = Column(URLType)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="post")
    post_comment = relationship("Comment", back_populates="post_related")

class  Comment(Base):

    __tablename__ ="comments"

    id = Column(Integer,primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    is_active = Column(Boolean,default=True)
    name = Column(String)
    email = Column(EmailType)
    body= Column(String)
    post_id = Column(Integer,ForeignKey("posts.id"))

    post_related = relationship("Post" , back_populates="post_comment")


""" Granjas """


class FarmType(Base):
        __tablename__ = 'farm_types'

        frm_type_id = Column(Integer, primary_key=True, autoincrement=True)
        frm_type_name = Column(String(45), nullable=False)
        frm_type_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        frm_type_enabled = Column(Integer, nullable=False, default="1")

        
class Region(Base):
        __tablename__ = 'regions'

        reg_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        reg_name = Column(String(45), nullable=False)
        reg_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        reg_updated = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
        reg_enabled = Column(Integer, nullable=True,default="1")



class Farm(Base):
        __tablename__ = 'farms'

        frm_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
        frm_name = Column(String(45), nullable=False)
        frm_restriction = Column(JSON)
        frm_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        frm_updated = Column(TIMESTAMP)
        frm_enabled = Column(Integer, nullable=True, default="1")
        farm_types_frm_id = Column(ForeignKey('farm_types.frm_type_id'), primary_key=True, nullable=False, index=True)
        region_frm_id = Column(ForeignKey('regions.reg_id'), primary_key=True, nullable=False, index=True)
        farm_types_frm = relationship('FarmType')
        region_frm = relationship('Region')
        


class FarmsVisited(Base):
        __tablename__ = 'farms_visited'

        frm_visited_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        frm_visited_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
        farm_frm_visited_id = Column(Integer, nullable=False, index=True)
        user_frm_visited_id = Column(Integer, nullable=False, index=True)
        frm_visited_quarantine_nights = Column(SMALLINT, nullable=False)
        #variable para farms_visited se le agregan la cantidad de 1 a 4 dias maximo
        frm_visited_quarentine_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        frm_visited_is_region = Column(SMALLINT, nullable=False)