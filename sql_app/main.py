from typing import List
from fastapi import Depends, FastAPI, HTTPException, status,File, UploadFile
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.expression import text
from . import crud, models, schemas
from .database import SessionLocal, engine
from jose import JWTError, jwt
from datetime import datetime, timedelta
import  cloudinary
import cloudinary.uploader
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://10.0.0.24:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o Contraseña Incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@app.get('/today/')
def get_current_date():
    return datetime.now()
@app.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/users/")
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)

@app.post("/posts/",status_code=status.HTTP_201_CREATED)
def create_post(
    title:str,body:str,file: UploadFile = File(...), db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)
):
    user_id=current_user.id

    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")

    return crud.create_post(db=db,user_id=user_id,title=title,body=body,url=url)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.read_users(db=db)

@app.get("/posts/")
def post_list(db: Session = Depends(get_db)):
    return crud.post_list(db=db)

@app.post("/posts/{post_id}/comment",response_model=schemas.CommentList)
def create_comment(
        comment:schemas.CommentBase ,post_id:int,db:Session = Depends(get_db)
):
    return  crud.create_comment(db=db,post_id=post_id,comment=comment)

@app.get("/posts/{post_id}")
def post_detail(post_id:int,db: Session = Depends(get_db)):
    post =crud.get_post(db=db, id=post_id)
    comment = db.query(models.Comment).filter(models.Comment.post_id == post_id)
    active_comment = comment.filter(models.Comment.is_active == True).all()

    if post is None:
        raise HTTPException(status_code=404,detail="post does not exist")
    return {"post":post,"active_comment":active_comment}

@app.post("/send_email")
def send_email():
    return 'Email send'


""" gRANHJAS """
#REGION
#Obtener una region por medio del id
@app.get('/region/{reg_id}', response_model=schemas.Region)
def read_region(reg_id: int, db: Session = Depends(get_db)):
    db_region = crud.get_region(db, reg_id=reg_id)
    return db_region

#Obtener un listado de regions con un rango 0 - 100
@app.get("/regions/", response_model=List[schemas.Region])
def read_regions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    regions = crud.get_regions(db, skip=skip, limit=limit)
    return regions

#Agregar una region
@app.post("/regions/", response_model=schemas.Region)
def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    db_region = crud.create_region(db=db, region=region)

    return db_region


#Agreagr item

#Agregar Granja sabiendo el id de la region

@app.get("/farms/", response_model=List[schemas.Farm])
def read_farms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    farms = crud.get_farms(db, skip=skip, limit=limit)
    return farms

@app.get("/farms_by_region/{region_id}", response_model=List[schemas.Farm])
def read_farms_by_regions(region_id: int, db: Session = Depends(get_db)):
    farms = crud.get_farms_by_region(db, region_id)
    return farms

@app.get('/farms/{frm_id}', response_model=schemas.Farm)
def read_farm(frm_id: int, db: Session = Depends(get_db)):
    db_farm = crud.get_farm(db, frm_id=frm_id)
    return db_farm


@app.post("/farms/", response_model=schemas.Farm)
def create_farm_for_region(
    farm: schemas.FarmCreate, db: Session = Depends(get_db)
):
    return crud.create_region_farm(db=db, farm=farm)

#Agregar un tipo de granja
@app.post("/farm_type/", response_model=schemas.FarmType)
def create_farm_type(farm_type: schemas.FarmTypeCreate, db: Session = Depends(get_db)):
    db_farm_type = crud.create_farm_type(db=db, farm_type=farm_type)

    return db_farm_type

@app.post("/farm_visited/", response_model=schemas.FarmVisited)
def create_farm_visited(farm_visited: schemas.FarmVisitedCreate, db: Session = Depends(get_db)):
    db_farm_visited = crud.create_farm_visited(db=db, farm_visited=farm_visited)

    return db_farm_visited

@app.get("/farm_visited/", response_model=List[schemas.FarmVisited])
def read_farm_visited(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    farm_visited = crud.get_farm_visited(db, skip=skip, limit=limit)
    return farm_visited

@app.get("/last_farm_visited_by_user/{user_id}")
def read_farm_visited(user_id : int, db: Session = Depends(get_db)):
    q = db.query(models.FarmsVisited, models.User, models.Farm).from_statement(text('''SELECT *, users.username FROM farms_visited JOIN users ON users.id = farms_visited.user_frm_visited_id JOIN farms ON farms.frm_id = farms_visited.farm_frm_visited_id WHERE user_frm_visited_id = {} order by frm_visited_date desc limit 1  ;'''.format(user_id))).all()
    print(q)
    return q

@app.get('/last_farms_visited_by_user/{user_id}')
def test_sql(user_id: int, db: Session = Depends(get_db)):

    q = db.query(models.FarmsVisited, models.User, models.Farm).from_statement(text('''SELECT *, users.username FROM farms_visited JOIN users ON users.id = farms_visited.user_frm_visited_id JOIN farms ON farms.frm_id = farms_visited.farm_frm_visited_id WHERE user_frm_visited_id = {} order by frm_visited_date desc   ;'''.format(user_id))).all()
    print(q)
    return q

@app.get('/details_visited/{user_id}')
def test_sql(user_id: int, db: Session = Depends(get_db)):

    q = db.query(models.FarmsVisited, models.User, models.Farm).from_statement(text('''SELECT *, users.username FROM farms_visited JOIN users ON users.id = farms_visited.user_frm_visited_id JOIN farms ON farms.frm_id = farms_visited.farm_frm_visited_id WHERE user_frm_visited_id = {} order by frm_visited_date desc   ;'''.format(user_id))).first()
    print(q)
    return q

@app.get('/last_region_visited_by_user/{user_id}')
def last_region_by_user(user_id: int, db: Session = Depends(get_db)):
    q = db.query(models.FarmsVisited,  models.Farm, models.Region).from_statement(text('''SELECT * FROM farms_visited  JOIN farms ON farms.frm_id = farms_visited.farm_frm_visited_id JOIN regions ON regions.reg_id = farms.region_frm_id WHERE farms_visited.user_frm_visited_id = {} ORDER BY frm_visited_id DESC LIMIT 1;'''.format(user_id))).first()
    print(q)
    return q



#RAW SQL QUERY  
""" @app.get('/test_sql/{user_id}')
def test_sql(user_id: int, db: Session = Depends(get_db)):

    q = db.query(models.FarmsVisited, models.User, models.Farm).from_statement(text('''SELECT *, users.username FROM farms_visited JOIN users ON users.id = farms_visited.user_frm_visited_id JOIN farms ON farms.frm_id = farms_visited.farm_frm_visited_id WHERE user_frm_visited_id = {};'''.format(user_id))).all()

    print(q)
    return q
 """



@app.get("/farm_type/{farm_type_id}", response_model=schemas.FarmType)
def read_farm_type(farm_type_id: int, db: Session = Depends(get_db)):
    db_farm_type = crud.get_farm_type(db, farm_type_id=farm_type_id)
    return db_farm_type



# @app.post("/items/", response_model=schemas.Item)
# def create_item_for_user(
#     item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items