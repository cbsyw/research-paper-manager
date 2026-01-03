from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(String)
    year = Column(Integer)
    abstract = Column(Text)
    url = Column(String)
    notes = Column(Text)
