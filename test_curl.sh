#!/usr/bin/env bash
# Проверка всех эндпоинтов Car Rental через curl (с поддержкой JWT-токена).
# Запуск:  bash test_curl.sh
# Другой адрес:  BASE_URL=http://localhost:8000 bash test_curl.sh

BASE_URL="${BASE_URL:-http://localhost:8001}/car_rental"
JSON="Content-Type: application/json"
TOKEN=""

# Печатает заголовок шага
step() {
    echo
    echo "=============================================="
    echo ">>> $1"
    echo "=============================================="
}

# Выполняет curl и выводит тело ответа + HTTP-статус.
# Если переменная TOKEN не пустая, автоматически добавляет заголовок Authorization: Bearer $TOKEN
# Использование: call METHOD PATH [JSON_BODY]
call() {
    local method="$1" path="$2" body="$3"
    local auth_args=()
    if [ -n "$TOKEN" ]; then
        auth_args=(-H "Authorization: Bearer $TOKEN")
    fi

    echo "$method $BASE_URL$path"
    if [ -n "$body" ]; then
        echo "Body: $body"
        curl -s -w "\nHTTP status: %{http_code}\n" -X "$method" "$BASE_URL$path" -H "$JSON" "${auth_args[@]}" -d "$body"
    else
        curl -s -w "\nHTTP status: %{http_code}\n" -X "$method" "$BASE_URL$path" "${auth_args[@]}"
    fi
}


# ---------------------------------------------- 1. USERS (создание)
step "1. USERS: создать пользователя (POST /users) → ожидается 200"
call POST /users '{"id": 1, "password": "123", "name": "Ivan", "last_name": "Petrov", "role": "owner", "type": "private"}'


# ---------------------------------------------- 2. LOGIN & получение JWT-токена
step "2. LOGIN: успешный вход и сохранение токена (POST /login) → ожидается 200"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" -H "$JSON" -d '{"name": "Ivan", "password": "123"}')
echo "Response: $LOGIN_RESPONSE"
TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')
echo "Saved TOKEN: $TOKEN"

step "3. LOGIN: неверный пароль (POST /login) → ожидается 401"
call POST /login '{"name": "Ivan", "password": "wrong_password"}'

step "4. LOGIN: несуществующий пользователь (POST /login) → ожидается 401"
call POST /login '{"name": "Nobody", "password": "123"}'

step "5. LOGIN: пустое тело (POST /login) → ожидается 422"
call POST /login '{}'


# ---------------------------------------------- 3. USERS (чтение и обновление с токеном)
step "6. USERS: получить пользователя по имени (GET /users/1?name=Ivan&last_name=Petrov) → ожидается 200"
call GET "/users/1?name=Ivan&last_name=Petrov"

step "7. USERS: получить всех пользователей (GET /users) → ожидается 200"
call GET /users

step "8. USERS: обновить своего пользователя с токеном (PATCH /users/1) → ожидается 200"
call PATCH /users/1 '{"id": 1, "password": "123", "name": "Ivan", "last_name": "Petrov", "role": "owner", "type": "private"}'


# ---------------------------------------------- 4. CARS
step "9. CARS: создать объявление об автомобиле (POST /cars) → ожидается 200"
call POST /cars '{"id": 1, "category": "sedan", "brand": "Toyota", "price": "50", "owner": 1}'

step "10. CARS: получить объявление (GET /cars/1) → ожидается 200"
call GET /cars/1

step "11. CARS: получить все объявления (GET /cars) → ожидается 200"
call GET /cars

step "12. CARS: обновить объявление с токеном (PATCH /cars/1) → ожидается 200"
call PATCH /cars/1 '{"id": 1, "category": "sedan", "brand": "Toyota", "price": "60", "owner": 1}'


# ---------------------------------------------- 5. RENTALS
step "13. RENTALS: создать аренду (POST /rentals) → ожидается 200"
call POST /rentals '{"id": 1, "car_id": 1, "user_id": 1, "total_day": 3}'

step "14. RENTALS: получить аренду (GET /rentals/1) → ожидается 200"
call GET /rentals/1

step "15. RENTALS: получить все аренды (GET /rentals) → ожидается 200"
call GET /rentals

step "16. RENTALS: обновить аренду (PATCH /rentals/1) → ожидается 200"
call PATCH /rentals/1 '{"id": 1, "car_id": 1, "user_id": 1, "total_day": 5}'


# ---------------------------------------------- 6. DELETE (удаление с токеном)
step "17. RENTALS: удалить аренду (DELETE /rentals/1) → ожидается 200"
call DELETE /rentals/1

step "18. CARS: удалить объявление с токеном (DELETE /cars/1) → ожидается 200"
call DELETE /cars/1

step "19. USERS: удалить своего пользователя с токеном (DELETE /users/1) → ожидается 200"
call DELETE /users/1


echo
echo "Готово."
