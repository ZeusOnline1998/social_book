from sqlalchemy import create_engine, Column, String, Integer, MetaData, DateTime, Date, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base

def get_connection():
    url = "postgresql://postgres:pass@localhost:5432/alchemy_db1"
    engine = create_engine(url)
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    birth_year = Column(Integer)

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    ProductName: Mapped[str]
    PartNumber: Mapped[str]
    ProductLabel: Mapped[str]
    StartingInventory: Mapped[int]
    InventoryReceived: Mapped[int]
    InventoryShipped: Mapped[int]
    InventoryOnHand: Mapped[int]
    MinimumRequired: Mapped[int]
    purchases = relationship("Purchases")
    orders = relationship("Orders")

class Suppliers(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    supplier: Mapped[str]
    purchases = relationship("Purchases", back_populates='suppliers')


class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    NumberReceived: Mapped[int]
    PurchaseDate = Column(Date)
    SupplierId: Mapped[int] = mapped_column(ForeignKey('suppliers.id'))
    suppliers = relationship("Suppliers", back_populates='purchases')
    ProductId: Mapped[int] = mapped_column(ForeignKey('products.id'))
    products = relationship("Products", back_populates='purchases')

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str]
    First: Mapped[str]
    Middle: Mapped[str]
    Last: Mapped[str]
    NumberShipped: Mapped[int]
    OrderDate = Column(Date)
    ProductId: Mapped[int] = mapped_column(ForeignKey('products.id'))
    products = relationship("Products", back_populates='orders')

session = get_connection()

from sqlalchemy import func
q1 = session.query(Products.ProductName, func.count(Products.ProductName))
print(q1)

q2 = session.query(Suppliers.id, Purchases.NumberReceived)\
    .join(Purchases)\
    .order_by(Purchases.NumberReceived)\
    .limit(5)
print(q2)
for id, number_received in q2:
    print(id, number_received)

q3 = session.query(func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name"),
                   Products.ProductLabel.in_(['Dell E310dw Printer', 'HP Spectre x360', 'Legion 5i Pro Gen6']))\
                    .join(Products)
print(q3)

q4 = session.query(Suppliers.supplier, Products.ProductLabel, Purchases.NumberReceived, Purchases.PurchaseDate)\
    .join(Products)\
    .join(Purchases)
print(q4)

q5 = session.query(func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name"))\
    .where(Orders.NumberShipped == func.max(Orders.NumberShipped))
print(q5)

# q6 = Alter table

q7 = session.query(Products)\
    .where(Products.InventoryOnHand.between(250, 450))
print(q7)

q8 = session.query(func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name"), Orders.OrderDate)
print(q8)

q9 = session.query(func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name"))\
    .where(Orders.NumberShipped == func.min(Orders.NumberShipped))
print(q9)

q10 = session.query(func.sum(Products.InventoryShipped))
print(q10)

q11 = session.query(Products.ProductName, Suppliers.supplier)\
        .join(Purchases, Products.id == Purchases.ProductId, isouter=True)\
        .join(Suppliers, Purchases.SupplierId == Suppliers.id, isouter=True)
print(q11)

q12 = session.query(Products.ProductName, func.avg(Products.StartingInventory))
print(q12)

q13 = session.query(func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name"), Orders.NumberShipped)\
        .order_by(Orders.NumberShipped)\
        .limit(10)
print(q13)

name = func.concat(Orders.Title, Orders.First, Orders.Middle, Orders.Last).label("Name")


q14 = session.query(Orders.id, name, Products.ProductLabel, Products.InventoryShipped)\
                .join(Products, isouter=True)
print(q14)

q15 = session.query(Orders.id, name, Products.ProductLabel, Products.InventoryShipped)\
                .join(Products, full=True)
print(q15)

q16 = session.query(Suppliers.supplier, Purchases.PurchaseDate)\
                .join(Purchases)\
                .where(Purchases.PurchaseDate.between('2022-01-01', '2022-03-31'))
print(q16)

q17 = session.query(name, Orders.OrderDate)\
                .where(Orders.OrderDate.between('2022-04-01', '2022-06-31'))
print(q17)

q18 = session.query(func.to_char(Purchases.PurchaseDate, '%b'))
print(q18)

q19 = session.query(func.upper(Orders.First, func.lower(Orders.Last)))\
                .limit(15)
print(q19)

q20 = session.query(func.to_char(Orders.OrderDate, '%d/%B/%Y'))\
                .limit(5)\
                .offset(6)
print(q20)

from sqlalchemy import update

q21 = update(Orders)\
        .where(Orders.id == 4)\
        .values({
            Orders.First: 'Amit',
            Orders.Middle: 'Kumar',
            Orders.Last: 'Sharma'
        })
        # .values(First='Amit', Middle='Kumar', Last='Sharma')

print(q21)

q22 = session.query(Orders.Title, func.count(Orders.Title))\
                .group_by(Orders.Title)
print(q22)

q23 = session.query(Orders)\
            .where(func.char_length(Orders.Last) == func.max(func.char_length(Orders.Last)))
print(q23)

q24 = session.query(name, Products.ProductLabel, Orders.OrderDate)\
                .join(Products)\
                .where(Orders.OrderDate.between('2022-04-07', '2022-07-10'))
print(q24)

from sqlalchemy.sql import text

# q25 Create duplicate table
# session.execute(text('CREATE table dummy as SELECT * from "suppliers"'))
# session.commit()

# q26 Truncate dummy table
# session.execute(text('TRUNCATE "dummy"'))
# session.commit()

# q27 Create duplicate table without values
# session.execute(text('CREATE TABLE dummy2 as SELECT * FROM "suppliers" WHERE 1 = 2'))
# session.commit()

# Self referencing table
# q28 = session.query(Products.ProductName, Products.ProductLabel, Products.InventoryOnHand, Products.InventoryShipped)\
#                 .join(Products, Products.ProductName != Products.ProductName)
# print(q28)
