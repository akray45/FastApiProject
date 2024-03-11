from fastapi import FastAPI, HTTPException, Response, status
from db.database import SESSION, engine
from app import models 
from app.schemas import AddressSchema, AddressCreate, AddressUpdate
"""To create all the requred table"""
models.Base.metadata.create_all(engine)

"""NOTE:
I tried to use geoalchemy2 which is very handy working with spatial data, request.
For some reason the libspatial lite that it uses under the hood was not getting installed on my linux 
laptop. 
Tried best to work with normal way to find close address to given address. Not prefect and not a wise decision
but this is the best i could come with for now. Would continue to improve and find the setup solution on laptop.
"""


app = FastAPI()

@app.get("/")
def get_health() -> Response:
    """Returns the health of the application"""
    return Response(content= "Application is up and running", status_code= status.HTTP_200_OK)
@app.post("/create-address")
def create_address(address: AddressCreate):
    """Post request which accepts schema AddressCreate and creates an instance of Address in db"""
    address_obj = models.Address(**address.dict())
    session = SESSION()
    try:
        session.add(address_obj)
        session.commit()
        session.refresh(address_obj)
        return address_obj
    finally:
        session.close()

@app.get("/get-close-addresses") 
def get_close_addresses(latitude: float, longitude: float, distance: float):
    """Get request which takes latitude, longitude and distance as query
    return list of address if close to given data else null """
    session = SESSION()
    try:
        query = f"""
                SELECT addresses.latitude, addresses.longitude,
    -- Calculate distance using Haversine formula
    6371 * 2 * ASIN(
        SQRT(
            POWER(SIN((RADIANS({latitude}) - RADIANS(addresses.latitude)) / 2), 2) +
            COS(RADIANS({latitude})) * COS(RADIANS(addresses.latitude)) *
            POWER(SIN((RADIANS({longitude}) - RADIANS(addresses.longitude)) / 2), 2)
        )
    ) AS distance
FROM addresses
WHERE 
    -- Filter addresses within given distance
    6371 * 2 * ASIN(
        SQRT(
            POWER(SIN((RADIANS({latitude}) - RADIANS(addresses.latitude)) / 2), 2) +
            COS(RADIANS({latitude})) * COS(RADIANS(addresses.latitude)) *
            POWER(SIN((RADIANS({longitude}) - RADIANS(addresses.longitude)) / 2), 2)
        )
    ) <= {distance};
                """
        addresses_results = session.execute(query)
        if not addresses_results:
            return []
        addresses = [{"id": row.id, "street": row.street, "city": row.city, "state": row.state, "zip_code": row.zip_code} for row in addresses_results]
        return addresses
    except Exception as ex:
        print(ex)
    finally:
        session.close()
@app.delete("/delete-address")
def delete_address(id: int) -> Response:
    """Deletes the obj from the db
    First tries to query database to see if the id is available or not then proceed to delete if present in db"""
    session = SESSION()
    try:
        address_obj = session.query(models.Address).filter(models.Address.id == id).first()
        if address_obj:
            session.delete(address_obj)
            session.commit()
            return Response(status_code= status.HTTP_200_OK, content= {"message": 'Delete was successful'})
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Given id is not present")
    except Exception as ex:
        print(ex)
    finally:
        session.close()
@app.get("/get-all-addresses")
def get_all_addresses():
    """Gives list of the obj present in database"""
    session = SESSION()
    try:
        all_addresses = session.query(models.Address).all()
        print(all_addresses)
        return all_addresses
    except Exception as ex:
        print(ex)
    finally:
        session.close()
@app.post("/update-address/{address_id}")
def update_address(address_id: int, address: AddressUpdate):
    """Gets address_id to query db then update the attributes depending on address obj in post request"""
    session = SESSION()
    try:
        address_obj = session.query(models.Address).filter(models.Address.id == address_id).first()
        if not address_obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Given address is not found")
        address_obj.city = address.city 
        address_obj.street = address.street
        address_obj.zip_code = address.zip_code
        address_obj.latitude = address.latitude
        address_obj.longitude = address.longitude
        session.commit()
        session.refresh(address_obj)
        return address_obj
    except Exception as ex:
        print(ex)
    finally:
        session.close()

        
