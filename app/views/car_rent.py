from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    password: str
    name: str
    last_name: str
    role: str
    type: str

class CarModel(BaseModel):
    id: int
    category: str
    brand: str
    price: str
    owner: int

class RentalModel(BaseModel):
    id: int
    car_id: int
    user_id: int
    total_day: int

class UserLogin(BaseModel):
    name: str
    password: str
