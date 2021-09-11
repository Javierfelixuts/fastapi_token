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

#SQLALCHEMY_DATABASE_URL = "postgresql://zvyoenyozxvfbb:762a127a058f9ac689deb11eace6af474a3cef320eb1b532d14b795558395ee0@ec2-35-174-122-153.compute-1.amazonaws.com:5432/dbgnbu7uq9h7no"

#----- ON LOCAL MACHINE ----
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:J8v5.f675@localhost/granjas_test1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()