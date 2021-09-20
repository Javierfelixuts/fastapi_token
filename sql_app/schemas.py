from typing import Optional
from pydantic import BaseModel
import datetime
from fastapi import Body
from sqlalchemy.sql.sqltypes import JSON


""" gRANJAS"""
#Farm Visited
class FarmsVisitedBase(BaseModel):
    frm_visited_date : datetime.datetime
    frm_visited_quarantine_nights: int
    farm_frm_visited_id: int
    user_frm_visited_id : int
    frm_visited_is_region: int


class FarmVisitedCreate(FarmsVisitedBase):
    pass

class  FarmVisited(FarmsVisitedBase):
    frm_visited_id: int
    class Config:
        orm_mode = True



#Farm
class FarmBase(BaseModel):
    frm_name: str
    frm_created: datetime.datetime
    frm_restriction: list = []


class FarmCreate(FarmBase):
    
    farm_types_frm_id : int
    region_frm_id: int
class Farm(FarmBase):
    frm_id: int
    farm_types_frm_id : int
    region_frm_id: int

    class Config:
        orm_mode = True

#FarmType
class FarmTypeBase(BaseModel):
    frm_type_name : str
    frm_type_created: datetime.datetime

class FarmTypeCreate(FarmTypeBase):
    pass

class FarmType(FarmTypeBase):
    frm_type_id: int
    frm_type_enabled: bool

    class Config:
        orm_mode = True

#Region
class RegionBase(BaseModel):
    reg_name: str
    reg_created: datetime.datetime

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    reg_id: int

    class Config:
        orm_mode = True


""" TOKEN"""

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    nombre: str
    apellidos: str
    visible_farms: list = []

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    password: str
    email: str

class PostBase(BaseModel):
    title:str
    body:str

class PostList(PostBase):
    created_date: Optional[datetime.datetime]
    owner_id: int
    owner: User

    class Config:
        orm_mode=True

class CommentBase(BaseModel):
    name:str
    body:str
    email:str

class CommentList(CommentBase):
    id: int
    post_id:int
    created_date: Optional[datetime.datetime]= Body(None)

    class Config:
        orm_mode= True
