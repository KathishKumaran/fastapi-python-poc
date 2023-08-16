## Create Virtual Environment

* python3 -m venv venv
* source venv/bin/activate

## Initial setup

* pip install fastapi uvicorn
* pip install python-jose
* pip install sqlalchemy databases[postgresql]

## For Migration

* pip install alembic
* pip install psycopg2
* pip install psycopg2-binary(If needed)

### Initialize Alembic:

* alembic init alembic

### In alembic.ini file:

* script_location = alembic
* sqlalchemy.url = postgresql://user:password@localhost/dbname

### In env.py file:

* target_metadata = Base.metadata

### Run Alembic Migration:

* alembic revision --autogenerate -m "create-user-table"

### Apply Migrations:

* alembic upgrade head

## Run the application

* python3 main.py or uvicorn main:app --host 127.0.0.1 --port 3000