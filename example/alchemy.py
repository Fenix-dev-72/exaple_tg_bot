#python + crud + database
#python + sqlalchemy + databse
from typing import Optional

# ORM:
#     syns
#     async

# engine => database connect
# Base => classlarga inhert uchun ishlatiladi
                #mosel classlarni table qilib shakilantiradi

from sqlalchemy import create_engine, String, ForeignKey, insert, delete, update, select  # slqalchemy kutubxonasi
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session  # base kutubxonasi
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin

#databse_nomi + psycopg2://database_user:password@lacalhost :port/ulanyaotgan dabase nomi
engine = create_engine("postgresql+psycopg2://postgres:samandar7282@localhost:5432/gym")
session = Session(engine) #databsega insert update delate select uchun ishlatiladi

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
           return f"Address(id={self.id!r}, email_address={self.email_address!r})"

Base.metadata.create_all(engine) #databseni tablega qarab shklantirib yartadi

insert_query = insert(User).values(id=1,name="alice", fullname="kamilova") #insert qoshish amali
insert_query2 = insert(User).values(id=2,name="alice", fullname="kamilova")
delete_query = delete(User).where(User.id == 1)
update_query = update(User).where(User.id == 1).values(name="Sarvinoz")
select_query = select(User)         #comit qilinmaydi malumot olingani sababli

session.execute(select_query).fetchall() #exe cute qilgandan song
# session.commit() #commit qilsh kerak aks holda bu malumot saqlanmaydi



