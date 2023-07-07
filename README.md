## Install virtualenv and activate the virtual environment
```
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```
## Install dependencies
```
$ pip install -r requirements.txt
```
## Create migrations and apply them to the database
```
$ python manage.py makemigrations
$ python manage.py migrate
```
## Run the server
```
$ python manage.py runserver
```
## Run Celery Beat (scheduler)
```
$ celery -A config beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
## Run Celery Worker (processor)
```
$ celery -A config worker -l info
```
