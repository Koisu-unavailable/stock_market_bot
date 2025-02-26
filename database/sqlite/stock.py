from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine("sqlite:///stock_prices.db")


class Stock(Base):
    __tablename__ = "stock"
    symbol = Column(String, primary_key=True)
    price = Column(Float)


Base.metadata.create_all(engine)

def _create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_all_stocks():
    session = _create_session()
    stocks = session.query(Stock).all()
    session.close()
    return stocks

def add_stock(symbol: str, price: float) -> None:
    session = _create_session()
    stock = Stock(symbol=symbol, price=price)
    session.add(stock)
    session.commit()
    session.close()
    return

