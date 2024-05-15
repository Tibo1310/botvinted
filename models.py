from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VintedBot(Base):
    __tablename__ = "VintedBot"

    id = Column(String(36), primary_key=True)
    creation_date = Column(TIMESTAMP)
    last_found_date = Column(TIMESTAMP)
    url_to_search = Column(Text)
    name = Column(String(255))
    id_user = Column(Integer, ForeignKey("User.id"))

    items = relationship("VintedItem", secondary="VintedBotItem", back_populates="bots")
    user = relationship("User", back_populates="bots")

    def __init__(self, id, creation_date, last_found_date, url_to_search, name, id_user):
        self.id = id
        self.creation_date = creation_date
        self.last_found_date = last_found_date
        self.url_to_search = url_to_search
        self.name = name
        self.id_user = id_user

class VintedItem(Base):
    __tablename__ = "VintedItem"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    price = Column(String(50))
    bot_id = Column(String(36), ForeignKey("VintedBot.id"))
