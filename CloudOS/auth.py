#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块: auth
描述: 此模块提供基础的用户授权功能, 返回一个授权token, 但需要注意该token的时效为1分钟.

作者: Fansihong
创建时间: 2026/04/21
初始版本: v1.0.0
"""

import requests

class GetToken:
	"""
	该类初始化实例时需要传入
	:参数: username: CloudOS平台登陆的用户名.
	:参数: password: CloudOS平台登陆用户名的密码.
	"""
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.url = "http://10.148.17.4:11000/sys/oapi/keystone/v3/auth/tokens"
	
	def get_auth_token(self):
		"""
		这个实例函数返回一个己经对用户授权的令牌.
		"""
		headers = {"Content-Type": "application/json", "Accept": "Application/json"}
		body = {
			"auth": {
				"identity": {
					"methods": ["password"],
					"password": {
						"user": {
							"name": self.username,
							"domain": {"name": "default"},
							"password": self.password
						}
					}
				}
			}
		}
		response = requests.post(url=self.url, headers=headers, json=body).headers
		return response["X-Subject-Token"]
