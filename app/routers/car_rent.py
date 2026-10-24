from app.views.car_rent import UserModel, CarModel, RentalModel, UserLogin
from fastapi import APIRouter, HTTPException
from app.models import car_rent as model

router = APIRouter(prefix="/car_rental")


@router.post("/login")
def login(user: UserLogin):
    user = model.login(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid password or username")
    token = model.create_token(user["id"], user["name"], user["role"])
    return {"access_token": token, "token_type": "bearer"}

@router.post("/users")
def create_user(user: UserModel):
    if model.get_by_name(user.name, user.last_name):
        raise HTTPException(status_code=409, detail="User already registered")
    return model.create_user(user)

@router.delete("/users/{user_id}")
def delete_user(user_id):
    if not 
        raise HTTPException(status_code=404, detail="User not found")
    return model.delete_user(user_id)

@router.patch("/users/{user_id}")
def update_user(user_id, user: UserModel):
    if not model.get_by_name(user.name, user.last_name):
        raise HTTPException(status_code=404, detail="User not found")
    return model.update_user(user_id, user)

@router.get("/users/{user_id}")
def get_user_by_name(name: str, last_name: str):
    if not model.get_by_name(name, last_name):
        raise HTTPException(status_code=404, detail="User not found")
    return model.get_by_name(name, last_name)

@router.get("/users")
def get_all_users():
    return model.get_all_users()


@router.post("/cars")
def create_car_ad(car: CarModel):
    return model.create_car_ad(car)

@router.delete("/cars/{car_id}")
def delete_car(car_id):
    if not model.get_car(car_id):
        raise HTTPException(status_code=404, detail="Car ad not found")
    return model.delete_car(car_id)

@router.patch("/cars/{car_id}")
def update_car(car_id, car: CarModel):
    if not model.get_car(car_id):
        raise HTTPException(status_code=404, detail="Car ad not found")
    return model.update_car(car_id, car)

@router.get("/cars/{car_id}")
def get_car(car_id):
    if not model.get_car(car_id):
        raise HTTPException(status_code=404, detail="Car ad not found")
    return model.get_car(car_id)

@router.get("/cars")
def get_all_car():
    return model.get_all_car()


@router.post("/rentals")
def create_rental(rental: RentalModel):
    return model.create_rental(rental)

@router.delete("/rentals/{rental_id}")
def delete_rental(rental_id):
    return model.delete_rental(rental_id)

@router.patch("/rentals/{rental_id}")
def update_rental(rental_id, rental: RentalModel):
    if not model.get_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found")
    return model.update_rental(rental_id, rental)

@router.get("/rentals/{rental_id}")
def get_rental(rental_id):
    if not model.get_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found")
    return model.get_rental(rental_id)

@router.get("/rentals")
def get_all_rentals():
    return model.get_all_rentals()


