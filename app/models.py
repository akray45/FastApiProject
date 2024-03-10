from sqlalchemy import Integer, String, Column, Float 

from db.database import Base


class Address(Base):
    """The address table to store the data in sqlite database"""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=False)
    city = Column(String, index=False)
    state = Column(String, index=False)
    zip_code = Column(String, index=False)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index= True)
