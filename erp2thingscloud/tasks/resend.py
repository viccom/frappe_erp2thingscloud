#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import frappe
import time
import json
import requests
from erp2thingscloud.erp2thingscloud.doctype.thingscloud_settings.thingscloud_settings import ThingsCloudSettings


@frappe.whitelist(allow_guest=True)
def resend_failed_serials():
	failed_serials_doc = frappe.get_all("Serial Number list", ["name", "sync_status", "serial_no"], filters={"sync_status": ["!=", "successful"], })
	# for doc in failed_serials_doc:
	# 	print(doc.name, doc.sync_status, doc.serial_no)
	if failed_serials_doc:
		send_data = {"sn_list": [v.name for v in failed_serials_doc]}
		cloud_server = ThingsCloudSettings.get_thingscloud_server()
		authorization_code = ThingsCloudSettings.get_authorization_code()
		headers = {'HDB-AuthorizationCode': authorization_code, 'Content-Type': 'application/json',
		           'Accept': 'application/json'}
		try:
			r = requests.session().post(cloud_server + "/api/method/iot.hdb_api.batch_add_device", headers=headers, json=send_data, timeout=3)
			if r.status_code == 200:
				result = r.json().get('message')
				# print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ':')))
				if result.get('done'):
					for sn in result.get('done'):
						serialno_doc = frappe.get_doc("Serial Number list", sn)
						serialno_doc.set("sync_status", 'successful')
						serialno_doc.save()
				return True
			else:
				return False
		except Exception as ex:
			frappe.logger(__name__).error(ex)
	else:
		return False
