import csv
import time
import json

filename = 'd:\\Coding\\CloudOS\\JSON\\kafka_cluster_data.json'

with open(file=filename, mode='r', encoding='utf-8') as f:
    cluster_data = json.load(f)

top_level_key = []
seen = set()

for cluster in cluster_data:
    for key, value in cluster.items():
        if key not in seen and value is not None and value != '' and not isinstance(value, (dict, list)):
            seen.add(key)
            top_level_key.append(key)

custom_key = ['availabilityZone', 'instanceName', 'internalIp', 'cpu', 'ram', 'disk', 'version', 'url', 'dataPath', 'logPath']
tab_headers = top_level_key + custom_key

print(tab_headers)