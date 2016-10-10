from google.appengine.ext import vendor
from google.appengine.api import users
vendor.add('lib')

import functools
import os.path
import re
import tornado.escape
import tornado.web
import tornado.wsgi
import unicodedata
from math import ceil


import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

import settings
import models
import utils


def admin(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user or not self.current_user.administrator:
            if self.request.method == "GET":
                self.redirect(self.get_login_url())
                return
            raise tornado.web.HTTPError(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = users.get_current_user()
        if user: user.administrator = users.is_current_user_admin()
        return user

    def get_login_url(self):
        return users.create_login_url(self.request.uri)

    def get_template_namespace(self):
        ns = super(BaseHandler, self).get_template_namespace()
        ns['users'] = users
        return ns

    @property
    def db(self):
        return self.application.db

class UrlFetcher(BaseHandler):
    def get(self):
        self.render("words.html", words=[], url='')

    def post(self):
        url = self.get_argument('url', '')
        words = []
        if url:
            words = utils.count_words(url)
            utils.store_words(words, self.db)
        
        max = 0
        for word in words:
            if word['counter'] > max:
                max = word['counter']
        if max < 5:
            max = 5;

        def size(counter):
            return min(int(ceil(counter / ceil(max/5))), 5)

        self.render("words.html", words=words, url=url, size=size)

class WordsAdmin(BaseHandler):

    @admin
    def get(self):
        words = self.db.query(models.Word).order_by(sa.desc(models.Word.counter)).all()
        self.render("admin.html", words=words)

    def post(self):
        if self.get_argument('operation', '') == 'truncate':
            self.db.query(models.Word).delete()
            self.db.commit()
        self.redirect('/admin/')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", UrlFetcher),
            (r"/admin/", WordsAdmin)
        ]
        options = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            xsrf_cookies=True
        )
        tornado.web.Application.__init__(self, handlers, **options)
        engine = sa.create_engine(settings.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=False)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind=engine))

app = tornado.wsgi.WSGIAdapter(Application())