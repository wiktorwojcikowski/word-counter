from html2text import html2text
from Crypto.PublicKey import RSA

import urllib2
import re
import operator
import md5
import models
import settings

privKey = RSA.importKey(open(settings.PRIVATE_KEY,'r').read())
pubKey = RSA.importKey(open(settings.PUBLIC_KEY,'r').read())

def strip_tags(html):
    return html2text(html.decode('utf8'))

def count_words(url):
    response = urllib2.urlopen(url)
    html = response.read()
    words = re.split('\W+', strip_tags(html))
    counters = dict()
    for word in words:
        if not word or len(word) < 3 or word.isdigit():
            continue
        if word in ['the', 'and',]:
            continue
        if word in counters:
            counters[word] += 1
        else:
            counters[word] = 1

    top_counters = sorted(counters.items(), key=operator.itemgetter(1))[-10:]
    top_counters = sorted(top_counters, key=operator.itemgetter(0))
    return [{'word': word, 'counter': counter} for word, counter in top_counters]


def store_words(words, session):
    for word in words:
        print word['word']
        m = md5.new()
        m.update(word['word'])
        m.update(settings.SECRET)
        key = m.hexdigest()
        instance = session.query(models.Word).get(key)

        if instance:
            instance.counter += word['counter'];
        else:
            token = pubKey.encrypt(word["word"].encode("utf-8"), 'X')[0].encode('base64')
            new_word = models.Word(key=key, token=token, counter=word['counter'])
            session.add(new_word)
    session.commit()

def decode_word(token):
    return privKey.decrypt(token.decode('base64'))
