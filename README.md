# Чат

Этот проект представляет собой меесенджер чат. Он разработан на Django с поддержкой обработки запросов по API и включает поддержку веб-сокетов для работы в режиме реального времени.

## Общие сведения

Проект представляет собой мессенджер, предоставляющий возможность общения с коллегами.
Проект разделён на две части:
1. API
2. WEB

В качестве библиотеки API используется Django REST Framework.
В качестве библиотеки WEB используется Django Channels и Django.

> **Важно!**
> В web приложении используется базовая аутентификация и авторизация, а также аутентификация с помощью сессий.
> В API используется встроенная аутентификация с помощью токенов для аутентификации и авторизации.

API и web приложения могут работать одновременно.

Так как чат является закрытым, то только администратор может подключать пользователей к конкретным чатам.
Отписывание от чатов пользователя может производить сам пользователь.

### Используемые технологии
1. Django
2. Django REST Framework
3. Django Channels
4. Postgres
5. Redis
6. Nginx
7. Daphne
8. HTMX

### Используемые инструменты
Приложение разворачивается с помощью Docker-композера.
Для симуляции одностраничного приложения был использован HTMX, который позволяет делать запросы без перезагрузки страницы.
Также через HTMX отправлялись запросы в режиме реального времени с использованием WebSocket.

## Установка и запуск

Для установки зависимостей и запуска проекта выполните следующие команды:

```bash
# Клонировать проект из GitHub
git clone https://github.com/danefremov/rosatom.git

# Перейти в директорию проекта
cd ./rosatom/ros_chat

# Запустите Docker-композер из директории ros_chat
docker-compose up --build

# Запустите миграции базы данных
docker compose exec web python manage.py migrate

# Создайте суперпользователя
docker compose exec web python manage.py createsuperuser

# Запустите сервер в режиме реального времени
Можно переходить по ссылке (localhost) для просмотра сайта или воспользоваться апи.
```


## Основной URL
`http://localhost/`

## Инструкции
При использовании API, необходимо сначала получить токен для аутентификации, используя POST-запрос на адрес `/api/accounts/login/`.
Затем при каждом запросе токен должен передаваться в заголовке `Authorization` как `Token {токен}`.


## Примечания

Так как приложение является учебным проектом, то в настройках Django в файле settings.py была оставлена настройка `DEBUG = True`.  В случае необходимости можно установить `DEBUG = False`.


## Эндпоинты API



### 1. Регистрация
- **URL**: `/api/accounts/register/`
- **Метод**: `POST`
- **Описание**: API для регистрации нового пользователя.
- **Запрос**:
    - **username**: Имя пользователя.
    - **password**: Пароль.
    - **email**: Электронная почта.
  ```json
    {
      "username" : "user1",
      "password" : "password1",
      "email" : "something1@domain.ru"
    }
    ```
- **Ответ**:
  - **Создано (201)**:
    ```json
    {
    "token": "14dd55e72a9a00a015c324cd9baedbeb8e21c907",
    "user": {
        "id": 2,
        "first_name": "",
        "last_name": "",
        "username": "user1",
        "email": "something1@domain.ru"
      }
    }
    ```


### 2. Вход в систему
- **URL**: `/api/accounts/login/`
- **Метод**: `POST`
- **Описание**: Получение токена авторизации для доступа к чатам.
- **Запрос**:
    - **username**: Имя пользователя.
    - **password**: Пароль.
  ```json
    {
      "username" : "user1",
      "password" : "password1"
    }
    ```
- **Ответ**:
  - **Успех (200)**:
    ```json
    {
    "token": "8ea5751fa52a73b9c862cc912e2d7b6361f50219"
    }
    ```




### 3. Получить список чатов
- **URL**: `/chat/`
- **Метод**: `GET`
- **Описание**: Возвращает список всех доступных пользователю чатов.
- **Ответ**:
  - **Успех (200)**:
    ```json
    [
    {
        "id": 1,
        "name": "первый",
        "participants": [
            {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "username": "dan",
                "email": "something2@domain.ru"
            }
        ],
        "created_at": "2024-11-04T10:30:50+03:00"
    }
    ]
    ```

### 4. Сообщения из чата
- **URL**: `/api/chat/{chat_id}/message`
- **Метод**: `GET`
- **Описание**: Получение сообщений из чата, доступных для текущего пользователя.
- **Параметры**:
  - `chat_id` (int): ID чата.
    - **Ответ**:
      - **Успех (200)**:
        ```json
        [
        {
            "id": 7,
            "chat": 1,
            "user": {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "username": "dan",
                "email": "something2@domain.ru"
            },
            "content": "8",
            "timestamp": "2024-11-04T10:31:23.116252+03:00"
        },
        {
            "id": 8,
            "chat": 1,
            "user": {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "username": "dan",
                "email": "something2@domain.ru"
            },
            "content": "Привет!",
            "timestamp": "2024-11-04T11:23:52.903939+03:00"
         }
        ]
        ```

### 5. Добавление в чат пользователя
- **URL**: `/api/chat/{chat_id}/user/{user_id}/`
- **Метод**: `PUT`
- **Описание**: Добавление пользователя в чат суперполььзователем.
- **Параметры**:
  - `chat_id` (int): ID чата.
  - `user_id` (int): ID пользователя.
    - **Ответ**:
      - **Успех (200)**:
        ```json
        {
        "message": "User ove added to chat"
        }
        ```

### 6. Удаление пользователя из чата
- **URL**: `/api/chat/{chat_id}/user/{user_id}/`
- **Метод**: `DELETE`
- **Описание**: Удаление пользователя из чата суперполььзователем.
- **Параметры**:
  - `chat_id` (int): ID чата.
  - `user_id` (int): ID пользователя.
    - **Ответ**:
      - **Успех (200)**:
        ```json
        {
        "message": "User ove removed from chat"
        }
        ```
        

### 7. Отправка сообщений в чат
- **URL**: `ws://{{host}}/ws/api/chat/{chat_id}/`
  - **Описание**: Отправка сообщений в чат по websocket.
  - **Запрос**:
    ```json
    {
     "message": "Hi Postman"
    }
    ```
- **Параметры**:
  - `chat_id` (int): ID чата.


### Также эти эндпоинты лежат в директории postman в проекте
 