# Salvador Da Pascoa - Django

## Description
Back end RESTful application written in Django for the [Salvador da Páscoa](https://www.salvadordapascoa.com.br/) 
project, that links chocolate artisans and customers during the COVID-19 global pandemic.

This project is supported by [COVID Solutions](https://www.covidsolutions.com.br/), a community dedicated to the
idealization and execution of projects that help the community against COVID-19 and its impacts.


## Requirements

- [Python 3.7](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Virtualenv](https://github.com/pypa/virtualenv/)
- [Git](https://git-scm.com/)

## Development

- Create the virtual environment and activate it

        virtualenv -p python3 venv
        source venv/bin/activate
- Install the requirements `pip install -r requirements.txt`
- Start the dockers `docker-compose up` with the database and the localstack
- Run the server with `python manage.py runserver 8000`

You need a `.env`file with your environment variables, here's an example file:
```
LOAD_ENVS_FROM_FILE='True'
ENVIRONMENT='development'
SECRET_KEY='{secret_key}'
DEFAULT_FROM_EMAIL='Salvador da Pascoa <noreply@salvadordapascoa.com.br>'
DATABASE_URL='{database_url}'
SENTRY_DSN='{sentry_key}'
AWS_STORAGE_BUCKET_NAME='{aws_storage_bucket_name}'
```
        