# Pictures service
![Test Image 3](/api.png)
###  Сервис для обработки изображений
***
    
###  Структура  
    pictures
    ├── user_images_service
        ├── config  #папка с настройками базы данных и прочего
        ├── repositories #каталог схем таблиц бд(моделей)
        ├── routers #каталог функций - роутингов 
        ├── schemas
        ├── service
        ├── static
        ├── Dockerfile
        ├── main.py
        ├── requirements.txt
        └── templates
    ├── data
    |   ├── nginx
    |       └──app.conf
    ├── .env
    └─  docker-compose.yml
