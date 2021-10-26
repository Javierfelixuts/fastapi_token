from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import cloudinary

cloudinary.config(
    cloud_name= "hnduusros",
    api_key= "927131722149478",
    api_secret ="he5lFnOeoeRDBmV9z9QKCTxhLn0"
)

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app2.db" + connect_args={'check_same_thread': False}
# ------ ON HEROKU APP -------

#SQLALCHEMY_DATABASE_URL = "postgresql://lruazgbimufqhz:d0706b73cba7e4f40e24773a3fd1dad7ce91370aa1cef7f1d240f44a02f9f29a@ec2-18-209-143-227.compute-1.amazonaws.com:5432/ddrhju6ehvq9vi"

#----- ON LOCAL MACHINE ----
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1191a76ae02f21ed789f3d06431c3ba6919a906de38b8f6508445551f612569f@ec2-54-91-188-254.compute-1.amazonaws.com/d8glm43g7e6qb7"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:J8v5.f675@localhost/granjas_test1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()