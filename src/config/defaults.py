from pydantic import MongoDsn

DEBUG = True
ENVIRONMENT = 'DEV'

SERVICE_NAME = 'translation-service'
SERVICE_VERSION = '0.0.1'
ROOT_PATH = ''
HOST = '0.0.0.0'
PORT = 8000

SWAGGER_URL = '/swagger'
REDOC_URL = '/redoc'

MONGO_DSN = MongoDsn('mongodb://localhost:27017')
