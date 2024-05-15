from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class VintedItem(Base):
    __tablename__ = "VintedItem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    price = Column(String(50))

# Pour créer la base de données si ce n'est pas déjà fait
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
