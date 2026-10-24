#!/usr/bin/env bash
# Проверка всех эндпоинтов Car Rental через curl.
# Запуск:  bash test_curl.sh
# Другой адрес:  BASE_URL=http://localhost:8000 bash test_curl.sh

BASE_URL="${BASE_URL:-http://localhost:8001}/car_rental"
JSON="Content-Type: application/json"

# Печатает заголовок шага
step() {
    echo
    echo "=============================================="
    echo ">>> $1"
    echo "=============================================="
}

# Выполняет curl и выводит тело ответа + HTTP-статус
# Использование: call METHOD PATH [JSON_BODY]
call() {
    local method="$1" path="$2" body="$3"
    echo "$method $BASE_URL$path"
    if [ -n "$body" ]; then
        echo "Body: $body"
        curl -s -w "\nHTTP status: %{http_code}\n" -X "$method" "$BASE_URL$path" -H "$JSON" -d "$body"
    else
        curl -s -w "\nHTTP status: %{http_code}\n" -X "$method" "$BASE_URL$path"
    fi
}


# ---------------------------------------------- USERS
step "1. USERS: создать пользователя (POST /users)"
call POST /users '{"id": 1, "password": "123", "name": "Ivan", "last_name": "Petrov", "role": "client", "type": "private"}'

step "2. USERS: получить пользователя (GET /users/1)"
call GET /users/1

step "3. USERS: получить всех пользователей (GET /users)"
call GET /users

step "4. USERS: обновить пользователя (PATCH /users/1)"
call PATCH /users/1 '{"id": 1, "password": "123", "name": "Ivan", "last_name": "Petrov", "role": "owner", "type": "private"}'


# ---------------------------------------------- CARS
step "5. CARS: создать объявление об автомобиле (POST /cars)"
call POST /cars '{"id": 1, "category": "sedan", "brand": "Toyota", "price": "50", "owner": 1}'

step "6. CARS: получить объявление (GET /cars/1)"
call GET /cars/1

step "7. CARS: получить все объявления (GET /cars)"
call GET /cars

step "8. CARS: обновить объявление (PATCH /cars/1)"
call PATCH /cars/1 '{"id": 1, "category": "sedan", "brand": "Toyota", "price": "60", "owner": 1}'



# ---------------------------------------------- RENTALS
step "9. RENTALS: создать аренду (POST /rentals)"
call POST /rentals '{"id": 1, "car_id": 1, "user_id": 1, "total_day": 3}'

step "10. RENTALS: получить аренду (GET /rentals/1)"
call GET /rentals/1

step "11. RENTALS: получить все аренды (GET /rentals)"
call GET /rentals

step "12. RENTALS: обновить аренду (PATCH /rentals/1)"
call PATCH /rentals/1 '{"id": 1, "car_id": 1, "user_id": 1, "total_day": 5}'


# ---------------------------------------------- LOGIN
step "13. LOGIN: успешный вход, ожидается токен (POST /login)"
call POST /login '{"name": "Ivan", "password": "123"}'

step "14. LOGIN: неверный пароль, ожидается 401 (POST /login)"
call POST /login '{"name": "Ivan", "password": "wrong_password"}'

step "15. LOGIN: несуществующий пользователь, ожидается 401 (POST /login)"
call POST /login '{"name": "Nobody", "password": "123"}'

step "16. LOGIN: пустое тело, ожидается 422 (POST /login)"
call POST /login '{}'


# ---------------------------------------------- DELETE
step "17. RENTALS: удалить аренду (DELETE /rentals/1)"
call DELETE /rentals/1

step "18. CARS: удалить объявление (DELETE /cars/1)"
call DELETE /cars/1

step "19. USERS: удалить пользователя (DELETE /users/1)"
call DELETE /users/1

echo
echo "Готово."


