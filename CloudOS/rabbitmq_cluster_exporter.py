#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os

# Json文件目录.
json_data_dir = os.path.join(os.path.dirname(__file__), "JSON")
# Json文件路径.
json_file = os.path.join(json_data_dir, 'cluster_details.json')

# 打开Json文件转换为Python可解析的数据类型.
with open(file=json_file, mode='r', encoding='utf-8') as f:
    pydata = json.loads(f.read())

# 过滤选择要输出的key
keys = [
        "realIp",
        "neutronManagementNetworkName",
        "projectName",
        "username",
        "availabilityZone",
        "nodeNumber",
        "status",
        "name",
        "nodeGroups"
        ]

# 列表推导将过滤的key更新到字典，外层为list，内层为字典.
filter_data = [
        {k: v for k, v in data['data'].items() if k in keys}
        for data in pydata
        ]

# 将这些数据拍扁，有嵌套的key拼接为如, 'nodeGroups.0.instance.name: xxxx"
def flatten_key(d, parent_key='', sep='.'):
    result = {}
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            result.update(flatten_key(v, new_key))
    elif isinstance(d, list):
        for i, e in enumerate(d):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            result.update(flatten_key(e, new_key))
    else:
        result[parent_key] = d
    new_dict = {k: v for k, v in result.items() if v}
    return new_dict

export_csv_file = os.path.join(os.path.dirname(__file__), 'cluster_information.csv')

# 去重key
seen = set()
headers = []
for item in [flatten_key(x) for x in filter_data]:
    for k in item:
        if k not in seen:
            seen.add(k)
            headers.append(k)

# 将数据写入到csv文件
with open(file=export_csv_file, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    writer.writerows([flatten_key(x) for x in filter_data])

