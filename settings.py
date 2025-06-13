import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# telegram credentials
telegram_key = os.environ["TELEGRAM_CREDENTIALS"]

# gigachat credentials
gigachat_key = os.environ["GIGACHAT_CREDENTIALS"]

# rabbitmq credentials
rabbitmquser = os.environ["RABBITMQUSER"]
rabbitmqpass = os.environ["RABBITMQPASS"]
rabbitmqhost = os.environ["RABBITMQHOST"]
rabbitmqport = os.environ["RABBITMQPORT"]
RABBITMQ_URL = f"pyamqp://{rabbitmquser}:{rabbitmqpass}@{rabbitmqhost}:{rabbitmqport}//"

# postgresql credentials
databaseuser = os.environ["DATABASE_USER"]
databasepass = os.environ["DATABASE_PASSWORD"]
databasename = os.environ["DATABASE_NAME"]
databasehost = os.environ["DATABASE_HOST"]
databaseport = os.environ["DATABASE_PORT"]
DATABASE_URL=f"postgresql+psycopg2://{databaseuser}:{databasepass}@{databasehost}:{databaseport}/{databasename}"

