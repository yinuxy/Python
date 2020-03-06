# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 22:48:22 2020

@author: Yinux
"""

import re
import argparse
import time
import json
import requests
import pymongo

def get_answers_by_page(page_no):
    offset = page_no * 10
    url = "https://www.zhihu.com/api/v4/questions/266808424/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=10&sort_by=default&platform=desktop".format(offset)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    r = requests.get(url, verify=False, headers=headers)
    content = r.content.decode("utf-8")
    data = json.loads(content)
    is_end = data["paging"]["is_end"]
    items = data["data"]
    client = pymongo.MongoClient()
    db = client["beauty"]
    if len(items) > 0:
        db.answers.insert_many(items)
    return is_end

def get_answers():
    page_no = 0
    client = pymongo.MongoClient()
    while True:
        print(page_no)
        is_end = get_answers_by_page(page_no)
        page_no += 1
        if is_end:
            break

def query():
    client = pymongo.MongoClient()
    db = client["beauty"]
    items = db.answers.find({"voteup_count": {"$gte": 100}}).sort([("voteup_count", pymongo.DESCENDING)])
    count = 0

    for item in items:
        content = item["content"]
        vote_num = item["voteup_count"]
        author = item["author"]["name"]
        matched = re.findall(r'data-original="([^"]+)"', content)
        print("> 来自 {}\n".format(item["url"]))
        print("> 作者 {}\n".format(author))
        print("> 赞数 {}\n".format(vote_num))
        img_urls = []
        for img_url in matched:
            if img_url not in img_urls:
                print("![]({})".format(img_url))
                img_urls.append(img_url)
        count += len(img_urls)
        print("\n\n")
    print(count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", help="save data", action="store_true", dest="save")
    parser.add_argument("--query", help="query data", action="store_true", dest="query")
    args = parser.parse_args()

    if args.save:
        get_answers()
    elif args.query:
        query()