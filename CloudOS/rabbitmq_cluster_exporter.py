#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
功能: 导出RabbitMQ集群的信息至csv文件中.
使用方法: python3 rabbitmq_cluster_exporter.py 'username' 'userpassword'
参数: username: 登陆cloudos用户名, password: 登陆密码.
示例: python3 rabbitmq_cluster_exporter.py 'fansihong 'mypasswd'
"""

import os
import json
import sys
import time
import csv
from auth import GetToken
from platform import BasicInfo as bsci

if len(sys.argv) != 3:
	print(__doc__)
	sys.exit(1)

client_auth = GetToken(sys.argv[1], sys.argv[2])
plt_client = bsci()

cluster_id = []
for cluster_data in plt_client.rabbitmq_clusters(client_auth.get_auth_token()).get('data'):
	cluster_id.append(cluster_data['id'])

cluster_info = []
for id in cluster_id:
	cluster_info.append(plt_client.rabbitmq_cluster_details(id, client_auth.get_auth_token()).get('data'))

seen = set()
top_level_key = []

for cluster in cluster_info:
	for key, value in cluster.items():
		if key not in seen and value is not None and value != "":
			seen.add(key)
			top_level_key.append(key)
custom_key = ["zone", "instanceName", "internalIp", "cpu", "ram", "disk", 'rabbitmq_policy', 'logPath', 'version', 'dataPath']
table_headers = top_level_key + custom_key
removing = ['availabilityZone', 'nodeGroups', 'serviceProperties']

for i in removing:
    table_headers.remove(i)

csv_root_dir = os.path.join(os.path.dirname(__file__), 'CSV')
if not os.path.exists(csv_root_dir):
	os.mkdir(csv_root_dir)
csv_out_file = os.path.join(csv_root_dir, f'rabbitmq_cluster_exporter_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv')

with open(file=csv_out_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=table_headers, extrasaction='ignore')
    writer.writeheader()
    for cluster in cluster_info:
        basic_info = {k: v for k, v in cluster.items() if k in table_headers}
        basic_info.update({'zone': cluster.get('availabilityZone').get('zone')})
        properties = {
            'rabbitmq_policy': cluster.get('serviceProperties').get('rabbitmq_policy'),
            'logPath': cluster.get('serviceProperties').get('logPath'),
            'version': cluster.get('serviceProperties').get('version'),
            'dataPath': cluster.get('serviceProperties').get('dataPath')
        }
        for group in cluster.get('nodeGroups'):
            hardware = {'cpu': group.get('cpu'), 'ram': group.get('ram'), 'disk': group.get('disk')}
            for inst in group.get('instances'):
                row = {**basic_info, **hardware, **properties}
                row.update({'instanceName': inst.get('instanceName'), 'internalIp': inst.get('internalIp')})
                writer.writerow(row)
