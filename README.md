This is total based on FastAPI and sqlite

To run application:

uvicorn app.main:app --reload

About database:
it is .dummy.db


Problem Statement

Create an address book application where API users can create, update and delete
addresses.
The address should:
- contain the coordinates of the address.
- be saved to an SQLite database.
- be validated
API Users should also be able to retrieve the addresses that are within a given distance and
location coordinates.

Docker file if not able to run it locally

Bild the image:-
docker build --no-cache -f  DockerFile -t fastapi .

Run the container:-
docker run -d -p  80:80  --name fastapi fastapi

Stop and Remove the container:-
docker rm -f fastapi
