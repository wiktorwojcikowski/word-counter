# word-counter



# Local run

https://cloud.google.com/python/getting-started/using-cloud-sql
cloud_sql_proxy -instances=word-counter-145910:us-central1:word-counter-db=tcp:3306
pip install -t lib -r requirements.txt
dev_appserver.py ./


# development
pip install -r dev_requirements.txt

virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head


# Deploy on GAE:

pip install -t lib -r requirements.txt

gcould app deploy app.yaml