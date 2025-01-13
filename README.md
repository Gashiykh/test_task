Данный проект представляет собой REST API сервис для управления заказами (Order), разработанный с использованием подхода Clean Architecture.
 В проекте реализованы основные функции управления заказами, такие как создание, обновление, получение и мягкое удаление заказов. Сервис поддерживает авторизацию пользователей с различными ролями, кэширование данных, логирование действий и метрики.

Стек технологий:
• Python 3.11
• Django/Django REST Framework
• PostgreSQL
• Redis
• Docker/Docker Compose
• Swagger/OpenAPI

Основные функции

Заказы:
- Список заказов: GET /api/orders/
- Детальный просмотр заказа: GET /api/orders/{order_id}
- Создание заказа: POST /api/orders/
- Обновление заказа: PATCH /api/orders/{order_id}/
- Фильтрация заказов: GET /api/orders?status={status}&min_price={min_price}&max_price={max_price}
- Мягкое удаление заказа: DELETE /api/orders/{order_id}/

Авторизация:
- Авторизация пользователя: POST /auth/login/

Роли: 

 User (username=dev, password=dev)
 Admin (username=admin, password=admin)

User: может создавать, получать и обновлять свои заказы
Admin: доступ ко всем операциям с заказами

Модели

Сущности:

1. Заказы
2. Продукты
3. Пользователи

Связь:
Заказы <--> Продукты (многие ко многим)
Пользователи <--> Заказы (один ко многим)

Кэширование:
Кэширование данных о заказах в оперативной памяти
Автоматическое обновление кэша при изменении состояния заказа

Логирование:
Логирование всех действий пользователей (создание, обновление, удаление заказов)

События:
Логирование изменении состояния заказа

Метрики:
Доступ к метрикам через эндпоинт: GET /metrics

Документация: 
Swagger: GET /docs/swagger/
(для проверки запросов рекомендую использовать Postman)

Тестирование:
Покрыл unit-тестами основные crud операции

Как запустить проект:

Создать общую сеть: docker network create test_network

Запуск докера: docker-compose up --build 
