from app.views.car_rent import UserModel, CarModel, RentalModel
from pathlib import Path
from sqlalchemy import (
    JSON, Column, Integer, String, MetaData, Table, create_engine, inspect, select, ForeignKey
)

db_path = Path(__file__).resolve().parents[2] / "car_rent.db"
engine = create_engine(f"sqlite:///{db_path}")
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String, nullable = False),
    Column("last_name", String, nullable = False),
    Column("role", String, nullable = False),
    Column("type", String, nullable = False),
)

cars = Table(
    "cars",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("category", String, nullable = False),
    Column("brand", String, nullable = False),
    Column("price", String, nullable = False),
    Column("owner", Integer, ForeignKey("users.id"), nullable = False),
)

rentals = Table(
    "rentals",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("car_id", Integer, ForeignKey("cars.id"), nullable = False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable = False),
    Column("total_day", Integer, nullable = False),
)

def init_db():
    with engine.begin() as connection:
        metadata.create_all(connection)



#ALL AROUND USER:

def create_user(user: UserModel):
    query = users.insert().values(**user.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": result.inserted_primary_key[0], **user.model_dump()}

def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"message": f"User {user_id} deleted successfully"}

def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()
        return dict(result) if result else None
def get_by_name(name: str, last_name: str):
    query = users.select().where(users.c.name == name, users.c.last_name == last_name)
    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()
        return dict(result) if result else None

def get_all_users():
    query = users.select()
    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()
        return dict(result)

def update_user(user_id: int, user: UserModel):
    query = users.update().where(users.c.id == user_id).values(**user.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": user_id, **user.model_dump()}


#ALL AROUND CARS:

def create_car_ad(car: CarModel):
    query = cars.insert().values(**car.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": result.inserted_primary_key[0], **car.model_dump()}

def delete_car(car_id: int):
    query = cars.delete().where(cars.c.id == car_id)
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"messag": f"Ad of car {user_id} deleted successfully"}

def get_car(car_id: int):
    query = cars.select().where(cars.c.id == car_id)
    with engine.connect() as connection:
        result = connection.execute(query).mappings().first().all()
        return dict(result) if result else None

def get_all_car():
    query = cars.select()
    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()
        return [dict(row) for row in result]

def update_car(car_id: int, car: CarModel):
    query = cars.update().where(cars.c.id == car_id).values(**car.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": car_id, **car.model_dump()}


#ALL AROUND RENTALS:

def create_rental(rental: RentalModel):
    query = rentals.insert().values(**rental.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": result.inserted_primary_key[0], **rental.model*dump()}

def delete_rental(rental_id: int):
    query = rentals.delete().where(rentals.c.id == rental_id)
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"messag": f"Rental {rental_id} deleted successfully"}

def get_rental(rental_id: int):
    query = rentals.select().where(rentals.c.id == rental_id)
    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()
        return dict(result) if result else None

def get_all_rentals():
    query = rentals.select()
    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()
        return [dict(row) for row in result]

def update_rental(rental_id: int, rental: RentalModel):
    query = rentals.update().where(rentals.c.id == rental_id).values(**rental.model_dump())
    with engine.begin() as connection:
        result = connection.execute(query)
        return {"id": rental_id, **rental.model_dump()}

