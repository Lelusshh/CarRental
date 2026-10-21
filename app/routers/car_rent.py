from app.views.car_rent import UserModel, CarModel, RentalModel
from fastapi import APIRouter, HTTPException
from app.models import car_rent as model

router = APIRouter(prefix="/car_rental")


@router.post("")
def create_user(user: UserModel):
    if model.get_by_name(user.name, user.last_name):
        raise HTTPException(status_code=409, detail="User already registered")
    return model.create_user(user)

@router.delete("/user_id")
def delete_user(user: UserModel):
    if not model.get_by_name(user.name, user.last_name):
        raise HTTPException(status_code=404, detail="User not found")
    return model.delete_user(user_id)

@router.patch("/user_id")
def update_user(user: UserModel):
    if not model.get_by_name(user.name, user.last_name):
        raise HTTPException(status_code=404, detail="User not found")
    return model.update_user(user_id, user)


@router.post("")
def create_car_ad(car: CarModel):
    return model.create_car_ad(car)

@router.delete("/car_id")
def delete_car(car: CarModel):
    if not model.get_car(car_id):
        raise HTTPException(status_code=404, detail="Car ad not found")
    return model.delete_car(car_id)

@router.patch("/car_id")
def update_car(car: CarModel):
    if not model.get_car(car_id):
        raise HTTPException(status_code=404, detail="Car ad not found")
    return model.update_car(car_id, car)


@router.post("")
def create_rental(rental: RentalModel):
    return model.create_rental(rental)

@router.delete("")
def delete_rental(rental: RentalModel):
    return model.delete_rental(rental_id)

@router.patch("/rental_id")
def update_rental(rental: RentalModel):
    if not model.get_rental(rental_id):
        raise HTTPException(status_code=404, detail="Rental not found")
    return model.update_rental(rental_id, rental)

