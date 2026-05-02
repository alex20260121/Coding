#!/usr/bin/env python3.13

# -*- coding: utf-8 -*-
"""
Documentation:
Cloud OS 5.0 Component Service Exporter: Exports corresponding cluster information based on the platform's component services to a CSV file.
cluster_exporter.py [serverName]
    serverName: Pass in the component service name.
"""

import os
import sys
import json
from csv import DictWriter as dw
from time import strftime as sftm, localtime as lt

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

server_name = sys.argv[1]

json_data_root = os.path.join(os.path.dirname(__file__), 'json')
if not os.path.exists(json_data_root):
    os.mkdir(json_data_root)

csv_data_root = os.path.join(os.path.dirname(__file__), 'csv')
if not os.path.exists(csv_data_root):
    os.mkdir(csv_data_root)

def convert_python_data():
    json_file_name = os.path.join(json_data_root, f'{server_name}_cluster_details.json')
    with open(file=json_file_name, mode='r', encoding='utf-8') as f:
        pydata = json.load(f)
    for item in pydata:
        yield(item['data'])
    
def all_top_key():
    top_level_key = []
    seen = set()
    for data in convert_python_data():
        for key in data:
            if key not in seen:
                seen.add(key)
                top_level_key.append(key)
    return top_level_key

def csv_writer(default: bool = True, *args):
    csv_file_name = os.path.join(csv_data_root, f'{server_name}_cluster_{sftm("%Y%m%d%H%M%S", lt())}.csv')
    data = [x for x in convert_python_data()]
    if default:
        top_key = all_top_key()
        with open(file=csv_file_name, mode='w', newline='', encoding='utf-8') as f:
            csv_writer = dw(f, fieldnames=top_key)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        promt = f"Write to the CSV file using the default mode({csv_file_name})."
        return promt


if __name__ == "__main__":
    result = csv_writer()
    print(result)
