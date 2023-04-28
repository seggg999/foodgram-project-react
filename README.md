# Проект Foodgram «Продуктовый помощник»

## Описание:
    На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей,
    добавлять понравившиеся рецепты в список «Избранное», а так же скачивать сводный список продуктов,
    необходимых для приготовления одного или нескольких выбранных блюд.
 
## Регистрация и авторизация
    В проекте доступна система регистрации и авторизации пользователей.
 
### Обязательные поля для регистрации пользователя:
    Логин
    Пароль
    Email
    Имя
    Фамилия

### Уровни доступа пользователей:
    1) Гость (неавторизованный пользователь)
    2) Авторизованный пользователь
    3) Администратор

### Что могут делать неавторизованные пользователи:
    Создать аккаунт.
    Просматривать рецепты на главной.
    Просматривать отдельные страницы рецептов.
    Просматривать страницы пользователей.
    Фильтровать рецепты по тегам.

### Что могут делать авторизованные пользователи:
    Входить в систему под своим логином и паролем.
    Выходить из системы (разлогиниваться).
    Менять свой пароль.
    Создавать/редактировать/удалять собственные рецепты
    Просматривать рецепты на главной.
    Просматривать страницы пользователей.
    Просматривать отдельные страницы рецептов.
    Фильтровать рецепты по тегам.
    Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
    Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка   покупок.
    Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
    
### Что может делать администратор
    Администратор обладает всеми правами авторизованного пользователя. 
    Плюс к этому он может:
    изменять пароль любого пользователя,
    создавать/блокировать/удалять аккаунты пользователей,
    редактировать/удалять любые рецепты,
    добавлять/удалять/редактировать ингредиенты.
    добавлять/удалять/редактировать теги.
    Все эти функции нужно реализовать в стандартной админ-панели Django.

### Админка:
    В интерфейс админ-зоны выведены необходимые поля моделей и их фильтры.
    Этот интерфейс доступен по адресу: http://158.160.34.36/admin/

 ## Техническая инфраструктура проекта:
    Проект написан на Python 3.7
    Проект использует базу данных PostgreSQL.
    Используемые в проекте технологиитехнологии: Django, Django_rest_framework, Docker, Gunicorn, NGINX.
    Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) через docker-compose на сервере в Яндекс.Облаке. Образ с проектом размещен на Docker Hub.

## Ресурсы API YaMDb:

    Ресурс 'auth': аутентификация.
    Ресурс 'users': пользователи и управление подписками
    Ресурс 'tags': тэги для рецептов.
    Ресурс 'recipes': рецепты, их создание удаление и редактирование, а также "избранное" и список пакупок.
    Ресурс 'ingredients': Набор ингредиентов для рецепта. Можно использовать предустановленные ингредиенты.
    Ресурс 'redoc' - Подробная документация на эндпоинты сайта.

Каждый ресурс описан в документации доступной по адресу http://158.160.34.36/redoc/: там указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

## Установка:

### Как запустить проект:

    Установите docker:
     `
    sudo apt install docker.io
     `
     
    Установите docker-compose, с этим вам поможет официальная документация.
    
    Скопируйте файлы docker-compose.yaml и nginx/default.conf из папки infra/backend/ этого проекта на сервер в home/<ваш_username>/docker-compose.yaml и  home/<ваш_username>/nginx/default.conf соответственно.
    
    Заполните файл .env и поместите в директорию home/<ваш_username>/ в соответствии с приложенным ниже шаблоном.
    
    При необходимости добавьте внешний ip адрес сервера в файл default.conf в параметр server_name 


    Перейти в каталог с файлом docker-compose.yaml и запустите docker-compose командой:
    `
    sudo docker-compose up
    `
    
    Выполните миграции командой:
    `
    sudo docker-compose exec backend python manage.py makemigrations
    `
    `
    sudo docker-compose exec backend python manage.py migrate
    `
    
    Создайте супер-пользователя командой:
    `
    sudo docker-compose exec backend python manage.py createsuperuser
    `
    
    Соберите и подготовьте статические файлы проекта командой:
    `
    sudo docker-compose exec backend python manage.py collectstatic --no-input
    `

### Шаблон заполнения .env файла:

    SECRET_KEY='your_SECRET_KEY'            - SECRET_KEY от Django
    DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql
    DB_NAME=postgres                        - имя базы данных
    POSTGRES_USER=postgres                  - логин для подключения к базе данных
    POSTGRES_PASSWORD=PASSWORD              - пароль для подключения к БД (установите свой)
    DB_HOST=db                              - название сервиса (контейнера)
    DB_PORT=5432                            - порт для подключения к БД


### Заполнение базы ингредиентов из .csv файла:

    Вы можете автоматически заполнить базу ингредиентов сайта из подготовленного файла ingredients.csv. 
    Для этого выполните команду:
    `
    docker-compose exec web python manage.py csv_to_db


#### IP адрес проекта
#### 158.160.34.36
   `
   name: sega                                                                                                                   
   `
   `
   email: sega@ss.ss                                                                                                           
   `
   `
   pass: 12345                                                                                                                                         
   `
   
#### Автор:

Сергей Долгов

![example event parameter](https://github.com/seggg999/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)
