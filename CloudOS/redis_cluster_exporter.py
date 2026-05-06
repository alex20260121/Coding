#!/usr/bin/env python3.13

# -*- coding: utf-8 -*-

"""
CloudOS平台服务组件台账导出脚本.
使用方法:
    cluster_exporter.py serverName
    serverName: [mysql], [redis], [mongodb], [rabbitmq], [kafka], [elasticsearch]
"""

import os
import sys
import time
import json
import csv

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

json_data_source_dir = os.path.join(os.path.dirname(__file__), "json")
csv_data_output_dir = os.path.join(os.path.dirname(__file__), "csv")

if not os.path.exists(csv_data_output_dir):
    os.mkdir(csv_data_output_dir)

def cluster_data(server_name: str = sys.argv[1]) -> list:
    """
    读取JSON文件内的集群信息, 将其转换为Python可解析的数据类型, 返回字典"data"内容.
    """
    json_file = os.path.join(json_data_source_dir, f"{server_name}_cluster_details.json")
    with open(file=json_file, mode="r", encoding="utf-8") as f:
        pydata = json.load(f)

    cluster_data = []
    for data in pydata:
        cluster_data.append(data["data"])
    return cluster_data

def extract_top_key(non_null_value: bool = True) -> list:
    """
    提取cluster_data()函数的键, 参数non_null_value的值为布尔类型(True|False),
    True: 过滤掉空值的键;
    False: 提取所有键
    """
    if not non_null_value:
        seen = set()
        all_keys = []
        for item in cluster_data():
            for key in item:
                if key not in seen:
                    seen.add(key)
                    all_keys.append(key)
        return all_keys
    else:
        seen = set()
        has_value_key = []
        for item in cluster_data():
            for key, value in item.items():
                if key not in seen and value is not None and value != "":
                    seen.add(key)
                    has_value_key.append(key)
        return has_value_key

# 设置csv输出文件路径
csv_file_name = f"{sys.argv[1]}_cluster_export_{time.strftime('%Y%m%d%H%M%S', time.localtime())}.csv"
csv_file_path = os.path.join(csv_data_output_dir, csv_file_name)

# 设置csv表头
custom_key = ['availabilityZone', 'instanceName', 'internalIp', 'cpu', 'ram', 'disk']
tb_header = extract_top_key() + custom_key
tb_header.remove('availabilityZone')
tb_header.remove('nodeGroups')
tb_header.remove('info')

# 将内容写入csv文件
with open(file=csv_file_path, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=tb_header, extrasaction='ignore')
    writer.writeheader()
    for cluster in cluster_data():
        base_info = {k: v for k, v in cluster.items() if k in tb_header}
        node_groups = cluster.get('nodeGroups', [])
        for group in node_groups:
            group_specs = {
                'cpu': group.get('cpu'),
                'ram': group.get('ram'),
                'disk': group.get('disk'),
                'availabilityZone': group.get('availabilityZone')
            }
            instance = group.get('instances', [])
            for inst in instance:
                row_data = {**base_info, **group_specs}
                row_data['instanceName'] = inst.get('instanceName')
                row_data['internalIp'] = inst.get('internalIp')
                writer.writerow(row_data)