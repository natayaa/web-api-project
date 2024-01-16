from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_OBJECTHOST = "sqlite:///database.sqlite3"

Base = declarative_base()
engine = create_engine(SQL_OBJECTHOST, echo=True, connect_args={"check_same_thread": False})
SessionLocale = sessionmaker(autoflush=False, autocommit=False, bind=engine)