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


def post_serial(serialno, supplier, max_retry=1, sleep=None):
	print("-----------------------------------------------")
	print("@@@post_serial :::", serialno, supplier)
	print("-----------------------------------------------")
	if sleep:
		time.sleep(sleep)
	max_retry = max_retry - 1
	send_data = {"sn_list": [serialno]}
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
		print("-----------------------------------------------")
		print("@@@ :::", cloud_server, authorization_code, send_data)
		print("-----------------------------------------------")
		headers = {'HDB-AuthorizationCode': authorization_code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
		r = requests.session().post(cloud_server + "/api/method/iot.hdb_api.batch_add_device", headers=headers, json=send_data, timeout=3)
		print(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ':')))
		if r.status_code != 200:
			print(json.dumps(r.json, sort_keys=True, indent=4, separators=(',', ':')))
			frappe.logger(__name__).error(r.text)
			if max_retry > 0:
				frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.post_serial', serialno=serialno, supplier=supplier, max_retry=max_retry, sleep=60)
			else:
				print("----------------------1-------------------------")
				print("@@@set serialno failed :::", serialno)
				print("-----------------------------------------------")
				sn_exists = frappe.db.get_value("Serial Number list", {"serial_no": serialno})
				print("-----------------------------------------------")
				print("@@@ sn_exists @@@@ :::", sn_exists)
				print("-----------------------------------------------")
				if not sn_exists:
					serialno_doc = frappe.get_doc(
						{"doctype": "Serial Number list", "serial_no": serialno, "sync_status": 'failed'})
					serialno_doc.insert(ignore_permissions=True)
			throw(r.text)
		else:
			frappe.logger(__name__).debug(r.text)
			print("----------------------2-------------------------")
			print("@@@set serialno successful :::", serialno)
			print("-----------------------------------------------")
			sn_exists = frappe.db.get_value("Serial Number list", {"serial_no": serialno})
			print("-----------------------------------------------")
			print("@@@ sn_exists @@@@ :::", sn_exists)
			print("-----------------------------------------------")
			if not sn_exists:
				serialno_doc = frappe.get_doc(
					{"doctype": "Serial Number list", "serial_no": serialno, "sync_status": 'successful'})
				serialno_doc.insert(ignore_permissions=True)
			else:
				serialno_doc = frappe.get_doc("Serial Number list", serialno)
				serialno_doc.update({"sync_status": 'successful'})
				serialno_doc.save()
				pass
	except Exception as ex:
		frappe.logger(__name__).error(ex)
		if max_retry > 0:
			frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.post_serial', serialno=serialno, supplier=supplier, max_retry=max_retry, sleep=60)
		else:
			print("-----------------------3------------------------")
			print("@@@set serialno failed :::", serialno)
			print("-----------------------------------------------")
			sn_exists = frappe.db.get_value("Serial Number list", {"serial_no": serialno}, "serial_no")
			if not sn_exists:
				serialno_doc = frappe.get_doc(
					{"doctype": "Serial Number list", "serial_no": serialno, "sync_status": 'failed'})
				serialno_doc.insert(ignore_permissions=True)
		throw(repr(ex))


def delete_serial(serialno, supplier, max_retry=10, sleep=None):
	pass
