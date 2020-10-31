###################################################
#                                                 #
#           © OneFirewall Alliance LTD            #
#                                                 #
###################################################

from datetime import datetime
from elasticsearch import Elasticsearch
from datetime import datetime
import time

print("-----------------------------------------------------")
print("|      Start Client Download from remote elkall     |")
print("-----------------------------------------------------")

elk_connection_string = ""
try:
    f = open("elk_connection_string.txt", "r")
    elk_connection_string = str(f.read())
    f.close()
except:
    print("No file with elk_connection_string string")

#print(elk_connection_string)

#es = Elasticsearch([elk_connection_string])
es = Elasticsearch([elk_connection_string],verify_certs=False, ssl_show_warn=False)

def get_data_syslog():
    time_now =  datetime.fromtimestamp(int(time.time()) - (24*60*60))
    time_early = datetime.fromtimestamp(int(time.time()) - (24*60*60+2*60))
    time_now_str = time_now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    time_early_str = time_early.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    print("From:\t", time_early_str)
    print("To:\t", time_now_str)
    #return
    res = es.search(
                        index="logs_ai_2020*", 
                        body=
                            {
                                "query": {
                                    "range" : {
                                        "time" : {
                                            "gte" : time_early_str,
                                            "lt" :  time_now_str
                                        }
                                    }
                                },
                                "size": 10000
                            }
                    )

    json_array = []
    for f in res['hits']['hits']:
        json_array.append(f)
    
    return json_array

def write_hits_in_file(syslog_array):
    if len(syslog_array)<=0:
        print("Nothing to write")
        return
    list_of_traffic = open('poc_traffic.txt','a')
    
    
    
    for hit in syslog_array:

        clean_time = datetime.strptime(str(hit['_source']['time']), '%Y-%m-%dT%H:%M:%S.%f%z')
        clean_time_output = clean_time.strftime('%b_%d,_%Y_@_%H:%M:%S.000')

        clean_event_time = datetime.strptime(str(hit['_source']['event_time_str']), '%Y-%m-%dT%H:%M:%S.%f%z')
        clean_event_time_output = clean_event_time.strftime('%b_%d,_%Y_@_%H:%M:%S.000')

        clean_event_time_str = datetime.strptime(str(hit['_source']['event_time']), '%Y-%m-%dT%H:%M:%S.%f%z')
        clean_event_time_str_output = clean_event_time_str.strftime('%b_%d,_%Y_@_%H:%M:%S.000')


        list_of_traffic.write(str(hit['_id']).replace(" ", "_") + " " + 
                                str(hit['_source']['device_ip']).replace(" ", "_") + " " + 
                                str(hit['_source']['device_type']).replace(" ", "_") + " " + 
                                str(hit['_source']['ec_activity']).replace(" ", "_") + " " + 
                                str(hit['_source']['action']).replace(" ", "_") + " " + 
                                str(hit['_source']['event_desc']).replace(" ", "_") + " " + 
                                str(clean_time_output) + " " + 
                                str(clean_event_time_str_output).replace(" ", "_") + " " + 
                                str(clean_event_time_output) + " " + 
                                str(hit['_source']['event_cat_name']).replace(" ", "_") + " " + 
                                str(hit['_source']['ip_dst']).replace(" ", "_") + " " + 
                                str(hit['_source']['ip_dstport']).replace(" ", "_") + " " + 
                                str(hit['_source']['ip_src']).replace(" ", "_") + " " + 
                                str(hit['_source']['net_direction']).replace(" ", "_") + " " + 
                                str(hit['_source']['direction']).replace(" ", "_") + " " + 
                                str(hit['_source']['protocol']).replace(" ", "_") + " " + 
                                str(clean_time_output) + " " + 
                                "\n")
    list_of_traffic.close()


syslog_array = get_data_syslog()
print("Entries found: ", len(syslog_array))
write_hits_in_file(syslog_array)
