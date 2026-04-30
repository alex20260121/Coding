# -*- coding: utf-8 -*-

import os
import json
import csv
import time

json_root = os.path.join(os.path.dirname(__file__), "JSON")
json_file = os.path.join(json_root, "redis_cluster_details.json")

def convert_data(filename, raw=False, filter=False) -> list:
    with open(file=filename, mode='r', encoding='utf-8') as f:
        pydata = json.load(f)
    if raw:
        return pydata

    if filter:
        filtered = [ {k: v for k, v in inner['data'].items() if v is not None and v != ""} for inner in pydata ]
        return filtered
    else:
        inner_data = [item['data'] for item in pydata]
        return inner_data

def write_in_csv(data: list):
    top_level_key = []
    seen = set()
    for item in data:
        for k in item:
            if k not in seen:
                seen.add(k)
                top_level_key.append(k)
    instance_key = ["availabilityZone", "instanceName", "internalIp", "cpu", "ram", "disk"]
    headers = top_level_key + instance_key
    target_csv_path = os.path.join(os.path.dirname(__file__), f"redis_cluster_export_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.csv")
    with open(target_csv_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


print(write_in_csv(convert_data(json_file, filter=True)))