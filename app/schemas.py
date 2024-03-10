from pydantic import BaseModel

"""Schemas to help with fast api request and response for different apis"""
class AddressBase(BaseModel):

    street: str 
    city: str 
    state: str 
    zip_code: str

class AddressCreate(AddressBase):
    latitude: float 
    longitude: float
class Address(AddressBase):
    id: int
class AddressUpdate(AddressCreate):
    pass
