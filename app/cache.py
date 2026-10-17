import time

_store: dict = {}


def get(chave):
    item = _store.get(chave)
    if item and item[1] > time.time():
        return item[0]
    return None


def set(chave, valor, ttl):
    _store[chave] = (valor, time.time() + ttl)
