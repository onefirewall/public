from datetime import datetime
import time
import json
import requests

max_mb = 15000


def clean_not_ofa():
    url = 'http://18.132.202.215:9200/ofa-syslog*/_delete_by_query'
    myobj = {
                "query": {
                    "bool": {
                        "must_not": {
                            "exists": {
                                "field": "ofa_exist"
                            }
                        }
                    }
                }
            }
    y = json.dumps(myobj)
    try:
        x = requests.post(url, data = y, headers = {'Content-type': 'application/json'})
        print(x.text)
    except:
        pass

try:
    clean_not_ofa()
except:
    pass
#rec_clean()
