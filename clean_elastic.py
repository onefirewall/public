from datetime import datetime
import time
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import requests

max_mb = 15000

def delete_index(index_name):
    url = "http://localhost:9200/" + index_name
    x = requests.delete(url)
    print(x.text)

def needs_clean():
    url = "http://localhost:9200/_cat/indices?h=index,store.size&bytes=mb&format=json"
    r = requests.get(url)

    current_mb = 0
    array_of_indexes = []
    for ind in r.json():
        if ind["index"].startswith("ofa-syslog"): 
            current_mb += int(ind["store.size"])
            array_of_indexes.append(str(ind["index"]))

    array_of_indexes.sort()

    if current_mb>max_mb:
        return array_of_indexes
    else:
        return None


def rec_clean():
    array_index = needs_clean()
    if array_index is not None:
        print("Need to clean")
        delete_index(array_index[0])
        time.sleep(5)
        rec_clean()
    else:
        print("Nothing to clean")

rec_clean()
