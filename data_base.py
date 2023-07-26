import os

from dotenv import load_dotenv

from sqlalchemy import Column, Integer, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

load_dotenv()

db_url = os.getenv('db_url')

metadata = MetaData()
engine = create_engine(db_url)
Base = declarative_base()
Base.metadata.create_all(engine)
engine.connect()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    def __init__(
            self,
            sex=None,
            city=None,
            age=None
    ):
        self.profile_sex = sex
        self.profile_city = city
        self.profile_age = age

    def save_user_info_to_database(self, city, sex, age):
        with Session(engine) as session:
            to_bd = User(
                sex=sex, city=city, age=age,
            )
            session.add(to_bd)
            session.commit()


class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = Column(Integer, primary_key=True)
    worksheet_id = Column(Integer, primary_key=True)


def add_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=worksheet_id)
        session.add(to_bd)
        session.commit()


def check_user(engine, profile_id, worksheet_id):
    with Session(engine) as session:
        from_bd = session.query(Viewed).filter(
            Viewed.profile_id == profile_id,
            Viewed.worksheet_id == worksheet_id
        ).first()
        return True if from_bd else False


if __name__ == '__main__':
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
