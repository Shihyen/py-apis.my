from flask_restful import Resource
from flask import current_app
from flask import request
import requests
from bs4 import BeautifulSoup
from utils import cache_util
import json
import urllib.parse
import logging

from functools import lru_cache

bitly_access_token = 'c9cde67a6b149291d9168e7a1126a8e7bc07833e'
group_guid = 'Bj2kfhCTp1E'

logger = logging.getLogger(__name__)

class ApiMetaProxy(Resource):
# 使用情況，懶得去DB撈文章的資料
# [x] 1. 依據天下集團的文章ID取得文章網頁的meta，用type區分頻道
# [x] 2. 依據網址取得網頁的meta
# [x] 3. 輸出成json
# [x] 4. default cache for 1h, cache to build, nocache to revoke
# [x] 5. 網址換成短網址
# [x] 6. 可以自行定義utm參數

    def __init__(self):
        self.url_pattern = {
            'cw': 'https://www.cw.com.tw/article/articleLogin.action?id={}',
            'futurecity': 'https://futurecity.cw.com.tw/article/{}',
            'opinion': 'https://opinion.cw.com.tw/blog/profile/{}',
            'ch': 'https://www.commonhealth.com.tw/article/article.action?nid={}',
            'cheers': 'https://www.cheers.com.tw/article/article.action?id={}'
        }

        pass

    def get_utm_url(self, url, utm):
        parsed_url = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qsl(parsed_url.query)
        qs.extend(utm)
        parts = list(parsed_url)
        parts[4] = urllib.parse.urlencode(qs)
        return urllib.parse.urlunparse(parts)

    def get_bitly_url(self, url):
        bitly = 'https://api-ssl.bitly.com/v4/shorten'
        headers = {
            'Authorization': 'Bearer {}'.format(bitly_access_token),
            'Content-Type': 'application/json'
        }
        params = {
            "long_url": url,
            "group_guid": group_guid
        }
        res = requests.request('post', json=params, headers=headers, url=bitly)
        data = json.loads(res.text)
        logger.info("Exception: %s " % data)
        return data.get('link')

    def json_return(self, code='0000', error='', items=[]):
        if code != '0000':
            success = False
        else:
            success = True

        return {'success': success, 'code': code, 'error': error, 'items': items }

    def get(self):

        article_id = request.args.get('id')
        article_type = request.args.get('type')
        url = request.args.get('url')
        utm_campaign = request.args.get('utm_campaign')
        utm_medium = request.args.get('utm_medium')
        utm_source = request.args.get('utm_source')

        meta_keys = [{'name': 'keywords'},{'name':'description'},{'property':'og:title'},{'property':'og:image'},{'property':'og:url'},{'property':'og:description'}]

        # get product url from id
        if (article_id is not None) & (article_type is not None) & (article_type in self.url_pattern):
            url = self.url_pattern[article_type].format(article_id)

        # get url content & beautiful soup
        res = requests.request('get', url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        
        # construct meta data
        meta = {
            'id': article_id,
            'title': soup.title.string,
        }

        for item in meta_keys:
            key = str(list(item.values())[0])
            value = (soup.find(attrs=item))
            if value is not None:
                value = value['content']
            meta[key] = value

        # check if utm parameters
        if utm_campaign is not None:
            utm = [
                ('utm_campaign', utm_campaign),
                ('utm_medium', utm_medium),
                ('utm_source', utm_source)
            ]
            url = self.get_utm_url(url, utm)

        # split keywords to list
        if meta['keywords']:
            meta['keywords'] = meta['keywords'].split(',')
        
        # shorten url
        meta['shorten'] = self.get_bitly_url(url)
            
        return self.json_return(items=[meta])
