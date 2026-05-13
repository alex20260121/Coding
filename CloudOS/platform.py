#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块名: platform
描述: 该模块实现了CloudOS平台一些功能，如获取平台基础信息.
"""

import time
import requests

class BasicInfo:

	def __init__(self):
		self.address = "https://10.148.17.4"
		self.headers = {"Accept": "application/json, text/plain, */*"}
		self.body = {"t": int(time.time() * 100)}
	
	def redis_clusters(self, token):
		uri = "/api/dbaas/mppIaasCluster/app/v1.0/v1/bigdata/clusters"
		self.headers.update({"Servicename": "redis", "X-Auth-Token": token})
		response = requests.get(url=self.address + uri, headers=self.headers, json=self.body, verify=False).json()
		return response

	def redis_cluster_details(self, clusterId, token):
		uri = f"/api/dbaas/mppIaasCluster/app/v1.0/v1/bigdata/cluster/{clusterId}"
		self.headers.update({"Servicename": "redis", "X-Auth-Token": token})
		response = requests.get(url=self.address + uri, headers=self.headers, json=self.body, verify=False).json()
		return response

	def rabbitmq_clusters(self, token):
		uri = "/api/mqs/app/v1.0/iaasCluster/v1/bigdata/cluster"
		self.headers.update({"Servicename": "rabbitmq", "X-Auth-Token": token})
		self.body.update({"withDetail": "true"})
		response = requests.get(url=self.address + uri, headers=self.headers, json=self.body, verify=False).json()
		return response

	def rabbitmq_cluster_details(self, clusterId, token):
		uri = f"/api/mqs/app/v1.0/iaasCluster/v1/bigdata/cluster/{clusterId}"
		self.headers.update({"Servicename": "rabbitmq", "X-Auth-Token": token})
		self.body.update({"withDetail": "true"})
		response = requests.get(url = self.address + uri, headers=self.headers, json=self.body, verify=False).json()
		return response

	def mongodb_clusters(self, token):
		uri = f"/api/dbaas/mppIaasCluster/app/v1.0/v1/bigdata/clusters"
		self.headers.update({"Servicename": "mongodb", "X-Auth-Token": token})
		response = requests.get(url=self.address + uri, headers=self.headers, json=self.body, verify=False).json()
		return response
