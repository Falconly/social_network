<h1 align='center'>Мини-социальная сеть</h1>
Используемые средства разработки:<br>
Python: 3.11.2;<br>
База данных: PostgreSQL 15.3. 


Установка:  
1. Заменить значения переменных окружения (environment) на свои в social_network/social_network/settings.py, docker-compose.yml;  
2. Выполнить в консоли docker-compose up --build или для работы в фоновом режиме docker-compose up -d --build;  
3. Перейти на http://localhost:8000/.  

Создание супер пользователя:  
docker-compose run django python manage.py createsuperuser  
Очистка базы данных:  
docker-compose run django python manage.py flush --no-input  
Возобновление работы контейнера:  
docker-compose up или docker-compose up -d для работы в фоновом режиме.
