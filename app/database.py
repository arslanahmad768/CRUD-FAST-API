from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite URL
# SQLACLHEMY_DATABASE_URL = "sqlite:///.FASTAPI.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:usman786@localhost/todo"

# check_same_thread':False .is needed only for SQLite. It's not needed for other databases.
# Create a sqlite engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Create a DeclarativeMeta instance
Base = declarative_base()


