## Requirements
Python3 + Postgres


## for local development
0) Install requirements:
`pip install -r requirements.txt`


1) Create postgres user:
`$ createuser -U postgres -P -s -e <your_new_username>`


2) Create a new - empty - database:
`$ createdb -U <username> <your_new_databasename>`


3) Edit the settings.py file:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': '<databasename>',

        'USER': '<username>',

        'PASSWORD': '<password>',

        'HOST': 'localhost',

        'PORT': '5432',
    }
}


4) Make and migrate migrations:
`python manage.py makemigrations && python manage.py migrate`


5) Get staticfiles in order:
`python manage.py collectstatic`


6) Run the application:
`python manage.py runserver`