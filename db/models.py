from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, relationship
# With these imports:
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

    # if a user is deleted all his uploads are deletd
    uploads = relationship("Upload", back_populates="user", cascade="all, delete-orphan")


class Upload(Base):
    __tablename__ = 'uploads'

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    finish_time = Column(DateTime)
    status = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship("User", back_populates="uploads")

    def upload_path(self):
        # You can implement this method to generate the path based on metadata
        return f"/uploads/{self.uid}/{self.filename}"

    def set_finish_time(self):
        self.finish_time = datetime.utcnow()


def main():
    # Create a SQLite database
    engine = create_engine('sqlite:///mydatabase.db')

    # Create tables in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

if __name__ == "__main__":
    main()

