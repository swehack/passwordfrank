import web

import settings

db = web.database(
    dbn = settings.DB_ENGINE,
    host = settings.DB_HOST,
    db = settings.DB_NAME,
    user = settings.DB_USER,
    pw = settings.DB_PASS
)

def get_words(results=1024):
    # This is very specific to my wordlist and to avoid bigint errors
    if results > 131072:
        results = 109557

    try:
        q = db.select(
            'wordlist',
            limit = results,
            order = 'id asc'
        )
    except:
        raise

    if not len(q):
        raise IndexError('No results')
    return q

def add_phrase(phrase=None, code=None, maxdays=10, maxviews=10):
    if not phrase:
        raise ModelError('Requires phrase argument')

    if not code:
        raise ModelError('Requires code argument')

    try:
        seq = db.insert(
            'stash',
            maxdays = maxdays,
            maxviews = maxviews,
            phrase = phrase,
            code = code
        )
    except:
        raise
    return seq

def get_phrase(seq=None, code=None, maxdays=None, maxviews=None):
    if seq:
        where = 'id = $seq'
    elif code:
        where = 'code = $code'
    else:
        raise ModelError('Requires ID or code argument')

    try:
        row = db.select(
            'stash',
            vars = {
                'seq':  seq,
                'code': code,
            },
            where = where,
            limit = 1,
            order = 'id asc'
        )
    except:
        raise

    if not len(row):
        raise ModelError('No rows found')

    # Only return first row
    return row[0]

def update_phrase(seq=None):
    try:
        phrase = get_phrase(seq)
    except:
        raise

    try:
        seq = db.update(
            'stash',
            vars = {
                'seq': seq,
            },
            views = phrase.get('views', 1)+1,
            where = 'id = $seq'
        )
    except:
        raise
    return seq

def delete_phrase(seq=None):
    try:
        changed = db.delete(
            'stash',
            vars = {
                'seq': seq,
            },
            where = 'id = $seq'
        )
    except:
        raise
    return changed

class ModelError(Exception): 
    def __init__(self, errstr):
        self.errstr = errstr

    def __str__(self):
        return repr(self.errstr)
