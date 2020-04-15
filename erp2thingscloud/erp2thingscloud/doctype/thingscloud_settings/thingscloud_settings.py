# -*- coding: utf-8 -*-
# Copyright (c) 2020, viccom.dong and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import re
import requests


class ThingsCloudSettings(Document):
	def update_thingscloud_status(self, status):
		self.thingscloud_status = status
		self.thingscloud_updated = frappe.utils.now()
		self.save()

	def refresh_status(self):
		status = get_thingscloud_status()
		if status:
			self.update_thingscloud_status("ON")
		else:
			self.update_thingscloud_status("OFF")

	@staticmethod
	def get_thingscloud_server():
		url = frappe.db.get_single_value("ThingsCloud Settings", "erp2thingscloud_url")
		if not url:
			return None
		return gen_server_url(url, "http", 80)
	pass

	@staticmethod
	def get_authorization_code():
		auth = frappe.db.get_single_value("ThingsCloud Settings", "authorization_code")
		if not auth:
			return None
		return auth
	pass

def gen_server_url(server, protocol, port):
	m = re.search("^(.+)://(.+)$", server)
	if m:
		protocol = m.group(1)
		server = m.group(2)

	m = re.search("^(.+):(\d+)$", server)

	if m:
		server = m.group(1)
		port = m.group(2)
	return ("{0}://{1}:{2}").format(protocol, server, port)


def get_thingscloud_status():
	try:
		inf_server = ThingsCloudSettings.get_thingscloud_server()
		if not inf_server:
			frappe.logger(__name__).error("ThingsCloud Configuration missing in ThingsCloudSettings")
			return

		r = requests.session().get(inf_server + "/", params={"q": '''SHOW USERS'''}, timeout=1)
		return r.status_code == 200
	except Exception:
		return False
