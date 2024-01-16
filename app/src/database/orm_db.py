from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_OBJECTHOST = "sqlite:///src/database/database.sqlite3"

engine = create_engine(SQL_OBJECTHOST, echo=True, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocale = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class DatabaseConnection:
    def __init__(self):
        self.session = SessionLocale()