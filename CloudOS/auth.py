#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

class GetToken:
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
