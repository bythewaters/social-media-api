# Social Media API
- Api service for social network (like instagram, facebook) written on DRF

## Feauters:
- JWT authenticated
- Documentation is located via /api/doc/swagger/
- User registration and authentication
- Create, update, and delete posts
- Like and dislike posts
- Add comments to posts
- Retrieve posts, likes, and comments
- Follow and unfollow users
- Get followers and following lists
- Search for posts by title or created time
- Create your post in date which you choose

## Technologies Used
- Django: A powerful Python web framework for building the backend.
- Django REST Framework: A toolkit for building Web APIs using Django.
- Redis: An in-memory data structure store used for caching and background task management.
- Celery: A distributed task queue system for background processing and scheduling.
- JWT Authentication: JSON Web Token-based authentication for securing API endpoints.
- Swagger: A tool for documenting and testing APIs.

## Installing using GitHub:
 - Open .env.sample and change environment variables on yours !Rename file from .env_sample to .env

```shell
git clone https://github.com/bythewaters/social-media-api.git
cd library-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- Use the following command to load prepared data from fixture(if you need):
  - `python manage.py loaddata social_media_data.json`.

Start celery worker with redis db:
```shell
docker run -d -p 6379:6379 redis
celery -A social_media_api worker
```

## Defaults users:
```
1. Staff:
  email: admin@social.com
  password: social1849

2. Regular user:
  email: test2@user.com
  password: social1849
  
Also you can create your superuser using command:
python manage.py createsuperuser
```

## Getting access:
- Create user via /api/user/register/
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR 
- Install ModHeader extension and create Request header with value ```Bearer <Your access token>```

