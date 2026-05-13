#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
功能: 导出Cloud os平台Redis集群信息台账.
使用方法: python3 redis_cluster_exporter.py 'username' 'password'
参数: username 登陆cloudos的用户名.
      password 登陆cloudos的用户名密码
示例: python3 redis_cluster_exporter.py 'fansihong' 'mypassword'
"""

# 导入相关处理模块
import os
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

# 提取出clusterId集群的id)
cluster_id = [x.get('id') for x in plt_client.redis_clusters(token=client_auth.get_auth_token()).get('data')]

# 提取cluster_data(集群信息)
cluster_data = [plt_client.redis_cluster_details(id, client_auth.get_auth_token()).get('data') for id in cluster_id]

# 设置csv存储目录&&存储路径
csv_root_dir = os.path.join(os.path.dirname(__file__), 'csv')
if not os.path.exists(csv_root_dir):
	os.mkdir(csv_root_dir)
csv_file_path = os.path.join(csv_root_dir, f'redis_cluster_export_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv')

# 设置csv表头
seen = set()
top_level_key = []
for data in cluster_data:
	for key, value in data.items():
		if key not in seen and value is not None and value != '':
			seen.add(key)
			top_level_key.append(key)
top_level_key.remove('availabilityZone')
top_level_key.remove('nodeGroups')
top_level_key.remove('info')
custom_header = ['availabilityZone', 'instanceName', 'internalIp', 'cpu', 'ram', 'disk']
tb_header = top_level_key + custom_header

# 写入csv文件
with open(file=csv_file_path, mode='w', newline='', encoding='utf-8-sig') as f:
	writer = csv.DictWriter(f, fieldnames=tb_header, extrasaction='ignore')
	writer.writeheader()
	
	for cluster in cluster_data:
		base_info = {k: v for k, v in cluster.items() if k in tb_header}
		for group in cluster.get('nodeGroups', []):
			group_spec = {"availabilityZone": group.get('availabilityZone', []), 'cpu': group.get('cpu'), 'ram': group.get('ram'), 'disk': group.get('disk')}
			for inst in group.get('instances'):
				row = {**base_info, **group_spec}
				row['instanceName'] = inst.get('instanceName')
				row['internalIp'] = inst.get('internalIp')
				writer.writerow(row)
				print(f'{row} 写入完成')
