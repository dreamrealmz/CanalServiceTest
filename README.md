# Разворачивание проекта
- cp example.env .env (изначально там уже заполнены данные, с которыми можно эксплуатировать проект)
- заполнить .env файл
- docker-compose build
- docker-compose up

# при контейнеров впервые 
- docker exec -it <название контейнера>_web_1 python manage.py migrate
- docker exec -it <название контейнера>_web_1 python manage.py createsuperuser
