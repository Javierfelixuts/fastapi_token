from typing import Optional
from pydantic import BaseModel
import datetime
from fastapi import Body


""" gRANJAS"""
#Farm Visited
class FarmsVisitedBase(BaseModel):
    frm_visited_date : datetime.datetime
    FARM_frm_visited_id: int
    USER_frm_visited_id : int

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

class FarmCreate(FarmBase):
    
    FARM_TYPES_frm_id : int
    REGION_frm_id: int
class Farm(FarmBase):
    frm_id: int
    FARM_TYPES_frm_id : int
    REGION_frm_id: int

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