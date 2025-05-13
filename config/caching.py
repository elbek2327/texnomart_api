from django.core.cache import cache

def cache_log(key, data, timeout=300):
    cache.set(key, data, timeout)

def get_cached_log(key):
    return cache.get(key)

def delete_cached_log(key):
    cache.delete(key)