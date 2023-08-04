from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

def get_connection():
    url = "postgresql://postgres:pass@localhost:5432/alchemy_db"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()


Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    birth_year = Column(Integer)


# Base.metadata.create_all(engine)

# ulist = [
#     User(name="Gusty", address="Kajiado", birth_year="1982"),
#     User(name="Alexia", address="Pivijay", birth_year="1975"),
#     User(name="Ophelia", address="Tatsuno", birth_year="1989"),
#     User(name="Annabelle", address="Velingrad", birth_year="2006"),
#     User(name="Marty", address="Somita", birth_year="1998"),
# ]

# session.add_all(ulist) # Takes a list of Object

# session.commit() #Commit every changes to the database

# q1 = session.query(User) #Retreives all users from table

# q2 = session.query(User).order_by('User.name') #Orders the data in according to name

# q3 = session.query(User).filter(User.name.like("A%")) #Filter data


# q5 = session.query(User).filter(or_(User.name.like("A%"),User.birth_year > 1992)) #Filter with or operator

# q6 = session.query(User).order_by(User.name.desc()) # Sort in descending order

# session.query(User).count() # Returns the count of the records

# Update record
# q8 = session.query(User).order_by(User.id.desc()).first()
# q8.name = 'Dwayne'
# session.commit()  #Commit the changes to the db

# Delete record
# q9 = session.query(User).order_by(User.id.desc())[1]
# session.delete(q9)
# session.commit()

# print(select(User.name, User.address)) # Select specific column

# print(select(User.name.label("name"), User.address)) # Alias column
