#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块名: platform
描述: 该模块实现了CloudOS平台一些功能, 如获取平台基础信息, 导出信息到CSV文件.
"""

import time
import requests

class RabbitMQ:
	"""
	该类定义了云平台RabbitMQ中间件的一些抽象实现.
	"""
	def __init__(self):
		self.basic_url = "http://10.148.17.4"

	def cluster_info(self, client_auth):
		"""
		该类方法对应 Cloudos 5.0 WebUI RabbitMQ中间件集群管理页, 返回一个字典对象.
		"""
		uri = "/api/mqs/app/v1.0/iaasCluster/v1/bigdata/cluster"
		url = self.basic_url + uri
		headers = {"Accept": "application/json, text/plain, */*", "servicename": "rabbitmq", "x-auth-token": client_auth}
		body = {"t": int(time.time() * 100), "withDetail": "true"}
		response = requests.get(url=url, headers=headers, json=body).json()
		return response
	
	def cluster_details(self, clusterId, client_auth):
		"""
		这个类方法根据对应的集群ID, 返回该集群的详细信息.
		:参数: clusterId 集群ID这个集群ID可以从cluster_info类方法获取.
		"""
		uri = f"/api/mqs/app/v1.0/iaasCluster/v1/bigdata/cluster/{clusterId}"
		url = self.basic_url + uri
		headers = {"Accept": "application/json, text/plain, */*", "servicename": "rabbitmq", "x-auth-token": client_auth}
		body = {"t": int(time.time() * 100), "withDetail": "true"}
		response = requests.get(url=url, headers=headers, json=body).json()
		return response
	

