from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

pony_handlers = Table(
    "pony_handlers",
    Base.metadata,
    Column("pony_id", ForeignKey("ponies.id"), primary_key=True),
    Column("handler_id", ForeignKey("handlers.id"), primary_key=True))


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))

    ponies = relationship("Pony", back_populates="owner")


class Pony(Base):
    __tablename__ = "ponies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    birth_year = Column(Integer)
    breed = Column(String(255))
    owner_id = Column(Integer, ForeignKey("owners.id"))

    owner = relationship("Owner", back_populates="ponies")
    handlers = relationship("Handler",
                            secondary=pony_handlers,
                            back_populates="ponies")


class Handler(Base):
    __tablename__ = "handlers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    employee_id = Column(String(12))

    ponies = relationship("Pony",
                          secondary=pony_handlers,
                          back_populates="handlers")


db_url = "sqlite:///dev.db"

engine = create_engine(db_url)

SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()

# pony_query = session.query(Pony).filter(Pony.name.like("%u%"))
# print(pony_query)

# pony_id_4_query = session.query(Pony).get(4)

# owner_query = session.query(
#     Owner.first_name, Owner.last_name).order_by(Owner.last_name)

# print(owner_query)

# hirzai_owners = session.query(Owner).join(Pony).filter(Pony.breed == "Hirzai")

# for owner in hirzai_owners:
#     print(owner.first_name, owner.last_name)

owners_and_ponies = session.query(Owner).options(joinedload(Owner.ponies))

for owner in owners_and_ponies:
    print(owner.first_name, owner.last_name)
    for pony in owner.ponies:
        print('\t', pony.name)

hirzai_owners_andPonies = session.query(Owner).join(
    Pony).filter(Pony.breed).options(joinedload(Owner.ponies))

session.close()
engine.dispose()
