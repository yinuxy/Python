#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Ryan time:2018/11/20

import requests
import json
import random
import time
from datetime import datetime
from datetime import timedelta

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    html = requests.get(url, headers=headers)
    if html.status_code ==200:
        return html.content
    else:
        return none

def parse_data(html):
    json_data = json.loads(html)['cmts']
    comments = []
    try:
        for item in json_data:
            comment = {
                'nickName': item['nickName'],
                'cityName': item['cityName'] if 'cityName' in item else '',
                'content': item['content'].strip().replace('\n', ''),
                'score': item['score'],
                'startTime': item['startTime']
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)

def save():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = '2019-2-05 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/248906.json?_v_=yes&offset=15&startTime=' + start_time.replace(
            ' ', '%20')
        html = None
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)
        comments =parse_data(html)
        start_time = comments[14]['startTime']
        print(start_time)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        for item in comments:
            print(item)
            with open('E:/spiderproject/maoyanMovies_comments/comments.txt', 'a', encoding='utf-8')as f:
                f.write(item['nickName']+','+item['cityName'] +','+item['content']+','+str(item['score'])+ item['startTime'] + '\n')
if __name__ == '__main__':
    url = 'http://m.maoyan.com/mmdb/comments/movie/248906.json?_v_=yes&offset=15&startTime=2018-11-19%2019%3A36%3A43'
    html = get_data(url)
    reusults = parse_data(html)
    save()