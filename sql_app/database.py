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

SQLALCHEMY_DATABASE_URL = "postgresql://jjuenqlvmfmbaf:d9712a21a06a52faae9adc0524755ab2fdf2e22cb3f9736d6e66e3879cba2250@ec2-54-156-151-232.compute-1.amazonaws.com:5432/d3c1p7tkqdffbp"

#----- ON LOCAL MACHINE ----
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:J8v5.f675@localhost/granjas_test1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()