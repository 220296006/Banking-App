from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field

# Use SQLite as the database
DATABASE_URL = "sqlite:///./test.db"  # This will create a SQLite database file named test.db in your project directory

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(None)
    password: str


Base = declarative_base()


# Create tables
def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
