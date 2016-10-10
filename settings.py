import os
import logging

SECRET = 'uhkmDhssBGp6TODJbXzafLgFYNjCKxQPgpDtOgrIVTc='

PRIVATE_KEY = 'etc/private.pem'
PUBLIC_KEY = 'etc/public.pem'

env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:Password123@localhost/wordcounter'
