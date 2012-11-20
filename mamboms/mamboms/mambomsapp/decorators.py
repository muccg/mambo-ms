from __future__ import with_statement

#
# Thread synchronization lock
#
def mutex(lock):
    """mutex decorator. provides generic synchronisation boilerplate."""

    def wrap(f):
        def newFunction(*args, **kw):
            with lock:
                return f(*args, **kw)
        return newFunction
    return wrap


