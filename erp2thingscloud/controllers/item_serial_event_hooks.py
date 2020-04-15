#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import frappe
import time
import json
import requests
from frappe import _, throw
from erp2thingscloud.erp2thingscloud.doctype.thingscloud_settings.thingscloud_settings import ThingsCloudSettings

def after_insert(doc, method):
	print("@@@serial_no add:::", doc.serial_no, doc.item_code, doc.batch_no, doc.item_name, doc.supplier, doc.item_code)
	frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.post_serial', serialno=doc.serial_no, supplier=doc.supplier)


def after_delete(doc, method):
	print("@@@serial_no delete:::", doc.serial_no, doc.item_code, doc.batch_no, doc.item_name, doc.supplier, doc.item_code)
	frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.delete_serial', serialno=doc.serial_no, supplier=doc.supplier)


def post_serial(serialno, supplier, max_retry=10, sleep=None):
	if sleep:
		time.sleep(sleep)
	max_retry = max_retry - 1
	send_data = {"gates": [{"sn": serialno, "name": serialno + "_name", "desc": serialno + "_desc"}]}
	cloud_server = ThingsCloudSettings.get_thingscloud_server()
	authorization_code = ThingsCloudSettings.get_authorization_code()
	if not supplier:
		frappe.logger(__name__).error(serialno + " doesn't have a supplier, So couldn't send to ThingsCloud")
		return
	if not cloud_server:
		frappe.logger(__name__).error("ThingsCloud url Configuration missing in ThingsCloud Settings")
		return
	if not authorization_code:
		frappe.logger(__name__).error("Authorization Code Configuration missing in ThingsCloud Settings")
		return
	try:
		# r = requests.session().get(cloud_server + "/query", params={"q": ''}, timeout=1)
		headers = {'HDB-AuthorizationCode': authorization_code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
		r = requests.session().post(cloud_server + "/api/method/iot_ui.iot_api.Batch_entry_gates", headers=headers, data=json.dumps(send_data), timeout=3)
		if r.status_code != 200:
			frappe.logger(__name__).error(r.text)
			if max_retry > 0:
				frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.post_serial', db_name=serialno, max_retry=max_retry, sleep=60)
			throw(r.text)
		else:
			frappe.logger(__name__).debug(r.text)
	except Exception as ex:
		frappe.logger(__name__).error(ex)
		if max_retry > 0:
			frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.post_serial', db_name=serialno, max_retry=max_retry, sleep=60)
		throw(repr(ex))


def delete_serial(serialno, supplier, max_retry=10, sleep=None):
	pass
