# word-counter



# Local run
pip install -t lib -r requirements.txt

https://cloud.google.com/python/getting-started/using-cloud-sql

cloud_sql_proxy -instances=word-counter-145910:us-central1:word-counter-db=tcp:3306

alembic upgrade head

# Deploy on GAE:

gcould app deploy app.yaml