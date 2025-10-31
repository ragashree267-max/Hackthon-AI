from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Create an engine — this uses an in-memory SQLite database
engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()

# Define a sample table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add data
user = User(name="Alice", email="alice@example.com")
session.add(user)
session.commit()

# Query data
for user in session.query(User):
    print(user.name, user.email)
