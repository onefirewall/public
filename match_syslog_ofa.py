from datetime import datetime
import time
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(['http://localhost:9200/'])

def get_data_syslog():
    time_now = datetime.now()
    time_early = datetime.fromtimestamp(int(time.time()) - (30*60))
    time_now_str = time_now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    time_early_str = time_early.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    res = es.search(
                        index="ofa-syslog*", 
                        body=
                            {
                                "query": {
                                    "range" : {
                                        "@timestamp" : {
                                            "gte" : time_early_str,
                                            "lt" :  time_now_str
                                        }
                                    }
                                },
                                "size": 2000
                            }
                    )

    json_array = []
    for f in res['hits']['hits']:
        json_array.append(f)
    
    return json_array

def update_from_ofa(syslog_array):
    arr = []
    for syslog_events in syslog_array:
        try:
            if syslog_events['_source']['srcip'].startswith("185.86.84")==False:
                arr.append(syslog_events['_source']['srcip'])

            if syslog_events['_source']['dstip'].startswith("185.86.84")==False:
                arr.append(syslog_events['_source']['dstip'])
        except:
            pass
        syslog_events['_source']['ofa_exist'] = False
    
    res = es.search(index="ofa-ips", 
                        body = {
                            "query": {
                                "terms": {
                                    "_id": arr 
                                }
                            },
                            "size": 2000
                        }
                    )
    
    for f in res['hits']['hits']:

        for syslog_events in syslog_array:
            try:
                if f['_source']['src_ip'] == syslog_events['_source']['srcip']:
                    syslog_events['_source']['ofa_exist'] = True
                    syslog_events['_source']['ofa'] = f['_source']
                    syslog_events['_source']['ofa_attack_direcation'] = 'in'
                elif f['_source']['src_ip'] == syslog_events['_source']['dstip']:
                    syslog_events['_source']['ofa_exist'] = True
                    syslog_events['_source']['ofa'] = f['_source']
                    syslog_events['_source']['ofa_attack_direcation'] = 'out'
            except:
                pass
    return syslog_array

def update_syslog(syslog_array):
    try:
        helpers.bulk(es, syslog_array)
    except Exception as e3:
        print(e3)
        print("Error")

syslog_array = get_data_syslog()
syslog_array = update_from_ofa(syslog_array)
update_syslog(syslog_array)

    