from sqlalchemy.orm import Session
from . import models, schemas
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate):
#     db_item = models.Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

SECRET_KEY = "bfcaa24859af5279d4ec6c1de8f9d2624f6d819b020eba2bcd9fe0483af45ed3"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username== username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, nombre = user.nombre, apellidos = user.apellidos, email= user.email, hashed_password=get_password_hash(user.password), visible_farms=user.visible_farms)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_post(db: Session,user_id:int,title:str,body:str,url:str):
    db_post = models.Post(title=title,body=body,owner_id=user_id,url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db, id: int):
    return db.query(models.Post).filter(models.Post.id== id).first()

def read_users(db):
    return db.query(models.User).all()
    
def post_list(db):
    return db.query(models.Post).all()

def create_comment(db: Session,post_id:int,comment:schemas.CommentBase):
    db_comment = models.Comment(post_id=post_id,**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

""" gRANJAS  """
#Regions
def get_regions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Region).offset(skip).limit(limit).all()

def get_region(db: Session, reg_id: int):
    return db.query(models.Region).filter(models.Region.reg_id == reg_id).first()


def create_region(db: Session, region: schemas.RegionCreate):
    db_region = models.Region(reg_name=region.reg_name, reg_created=region.reg_created )
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region
    
#Farms Visited
def create_farm_visited(db: Session, farm_visited: schemas.FarmVisitedCreate):
    db_farm_visited = models.FarmsVisited(frm_visited_date=farm_visited.frm_visited_date,frm_visited_quarantine_nights=farm_visited.frm_visited_quarantine_nights, farm_frm_visited_id=farm_visited.farm_frm_visited_id, user_frm_visited_id=farm_visited.user_frm_visited_id, frm_visited_is_region=farm_visited.frm_visited_is_region)
    db.add(db_farm_visited)
    db.commit()
    db.refresh(db_farm_visited)
    return db_farm_visited

def get_farm_visited(db: Session, skip: int = 0, limit: int = 100):
    
    return db.query(models.FarmsVisited).offset(skip).limit(limit).all()

def get_last_farm_visited_by_user(db: Session, id_user : int):
    return db.query(models.FarmsVisited).filter(models.FarmsVisited.user_frm_visited_id == id_user).order_by(models.FarmsVisited.frm_visited_date.desc()).first()

def get_farms_visited_by_user(db: Session, user_id : int):
    return db.query(models.FarmsVisited).filter(models.FarmsVisited.user_frm_visited_id == user_id)

#Granjas, Typo de Granjas, Regiones
def create_region_farm(db: Session, farm: schemas.FarmCreate):
    db_farm = models.Farm(frm_name=farm.frm_name, frm_restriction = farm.frm_restriction, farm_types_frm_id= farm.farm_types_frm_id, region_frm_id=farm.region_frm_id)
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

def get_farms(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Farm).offset(skip).limit(limit).all()

def get_farms_by_region(db: Session, region_id):

    return db.query(models.Farm).filter(models.Farm.region_frm_id == region_id).order_by(models.Farm.frm_id).all()


def get_farm(db: Session, frm_id: int):
    return db.query(models.Farm).filter(models.Farm.frm_id == frm_id).first()

def create_farm_type(db: Session, farm_type: schemas.FarmTypeCreate):
    db_farm_type = models.FarmType(frm_type_name=farm_type.frm_type_name, frm_type_created=farm_type.frm_type_created)
    db.add(db_farm_type)
    db.commit()
    db.refresh(db_farm_type)
    return db_farm_type


def get_farm_type(db: Session, farm_type_id: int):
    return db.query(models.FarmType).filter(models.FarmType.frm_type_id == farm_type_id).first()