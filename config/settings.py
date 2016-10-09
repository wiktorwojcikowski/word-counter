import os

# Google Cloud Project ID
PROJECT_ID = 'word-counter-145910'

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'Password123'
CLOUDSQL_DATABASE = 'wordcounter'
CLOUDSQL_CONNECTION_NAME = 'word-counter-145910:us-central1:word-counter-db'

if os.environ.get('GAE_APPENGINE_HOSTNAME'):
    SQLALCHEMY_DATABASE_URI = (
      'mysql+pymysql://{user}:{password}@localhost/{database}'
      '?unix_socket=/cloudsql/{connection_name}').format(
          user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
          database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)
else:
    SQLALCHEMY_DATABASE_URI = (
      'mysql+pymysql://{user}:{password}@localhost/{database}').format(
          user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
          database=CLOUDSQL_DATABASE)
