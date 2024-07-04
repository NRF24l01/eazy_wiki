from colorama import Fore
from os import path
from random import randint
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

db_path = "instance/db.db"
db_uri = f"sqlite:///{db_path}"

Base = declarative_base()

# Models
class Wiki(Base):
    __tablename__ = 'wiki'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    desc = Column(String(250))
    path_to_md = Column(String(75))
    path_to_logo = Column(String(75))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(10))
    can_read = Column(Boolean)
    can_write = Column(Boolean)

# Database setup
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

print(f"{Fore.CYAN}Try to open sqlite3 db: {db_path}")

if path.isfile(db_path):
    print(f"{Fore.GREEN}File detected. Try to connect")
else:
    print(f"{Fore.RED}File not found. Do migrate and upgrade firstly, or change path to file.")

print(Fore.GREEN+"Connected")

can_saw = input(Fore.MAGENTA+"User can see private articles? (y-yes): ")
can_edit = input("User can edit or create new articles? (y-yes): ")

csb = can_saw.lower() == "y"
cer = can_edit.lower() == "y"

print(f"{Fore.CYAN}Start creating user.")
if csb:
    print("He can see private articles")
else:
    print("He can't see private articles")
if cer:
    print("He can edit articles")
else:
    print("He can't edit articles")

key = "".join([str(randint(0, 9)) for _ in range(6)])

print(f"His key will be {Fore.RED}{key}")

new_user = User(key=key, can_read=csb, can_write=cer)
session.add(new_user)
session.commit()

print(Fore.GREEN+"Success")
