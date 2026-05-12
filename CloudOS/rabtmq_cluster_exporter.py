#!/usr/bin/env python3.13

# -*- coding: utf-8 -*-

"""
离线导出CloudOS平台RabbitMQ集群信息,需要将在线抓取的信息存储到JSON目录内
使用方法: 
    python3 rabtmq_cluster_exporter.py
"""

import os
import csv
import time
import json

json_root_dir = os.path.join(os.path.dirname(__file__), 'JSON')
json_in_file = os.path.join(json_root_dir, 'rabbitmq_cluster_details.json')

with open(file=json_in_file, mode='r', encoding='utf-8') as f:
    cluster_data = json.load(f)

seen = set()
top_level_key = []
for cluster in cluster_data:
    for k, v in cluster.items():
        if k not in seen and v is not None and v !='':
            seen.add(k)
            top_level_key.append(k)

csv_root_dir = os.path.join(os.path.dirname(__file__), 'CSV')
if not os.path.exists(csv_root_dir):
    os.mkdir(csv_root_dir)
csv_out_file = os.path.join(csv_root_dir, f'rabbitmq_cluster_exporter_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv')

custom_key = ["zone", "instanceName", "internalIp", "cpu", "ram", "disk"]
table_headers = top_level_key + custom_key

with open(file=csv_out_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=table_headers, extrasaction='ignore')
    writer.writeheader()
    for cluster in cluster_data:
        basic_info = {k: v for k, v in cluster.items() if k in table_headers}
        basic_info.update({'zone': cluster.get('availabilityZone').get('zone')})
        for group in cluster.get('nodeGroups'):
            hardware = {'cpu': group.get('cpu'), 'ram': group.get('ram'), 'disk': group.get('disk')}
            for inst in group.get('instances'):
                row = {**basic_info, **hardware}
                writer.writerow(row)