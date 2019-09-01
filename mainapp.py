from api import create_app
from flask import Flask, g, request
import logging
import time
from flask_caching import Cache

app = create_app()
cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})


@app.before_request
def before_request():
    """
    Save time when the request started.

    :return: None
    """

    g.start = time.time()
    g.cached = False

    # # check cache
    # if not request.values:
    if (request.args.get('cache') != '1'):
        response = cache.get(request.full_path)
        if response:
            g.cached = True
            return response

    return None


@app.after_request
def after_request(response):
    """
    Write out a log entry for the request.

    :return: Flask response
    """

    if 'start' in g:
        response_time = (time.time() - g.start)
    else:
        response_time = 0

    response_time_in_ms = int(response_time * 1000)

    # set cache
    # if not request.values:
    if (g.cached) & (request.args.get('nocache') != '1'):
        response_time_in_ms = 'CACHED'
    # only cache successfully response
    elif (response.status_code == 200) :
        timeout = 3600 #api_config.get_cache_timeout(request.url_rule.rule)
        cacheKey = request.full_path.replace('cache=1','')
        cache.set(cacheKey, response, timeout=timeout)
        logging.info("CACHE_SET key:[%s] is setting cache for [%i]seconds", cacheKey, timeout)

    params = {
        'method': request.method,
        'in': response_time_in_ms,
        'url': request.full_path,
        'ip': request.remote_addr,
        'status': response.status
    }
    logging.info('[APILOG] Time(ms):[%(in)s] Client:[%(ip)s] URL:[%(url)s] Status:[%(status)s]', params)
    return response