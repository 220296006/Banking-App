from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Use SQLite as the database
DATABASE_URL = "sqlite:///./test.db"  # This will create a SQLite database file named test.db in your project directory

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# Create a session for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Create tables
def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()