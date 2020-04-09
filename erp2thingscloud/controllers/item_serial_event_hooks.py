#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import frappe
import time
import requests
from frappe import _, throw
from erp2thingscloud.erp2thingscloud.doctype.thingscloud_settings.thingscloud_settings import ThingsCloudSettings

def after_insert(doc, method):
	frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.after_insert', db_name=doc.domain)


def after_delete(doc, method):
	frappe.enqueue('erp2thingscloud.controllers.item_serial_event_hooks.after_insert', db_name=doc.domain)


def post_serial(serialno, max_retry=10, sleep=None):
	if sleep:
		time.sleep(sleep)
	max_retry = max_retry - 1

	inf_server = ThingsCloudSettings.get_thingscloud_server()
	if not inf_server:
		frappe.logger(__name__).error("ThingsCloud url Configuration missing in ThingsCloud Settings")
		return

	try:
		r = requests.session().get(inf_server + "/query", params={"q": ('''CREATE DATABASE "{0}"''').format(serialno)}, timeout=1)

		if r.status_code != 200:
			frappe.logger(__name__).error(r.text)
			if max_retry > 0:
				frappe.enqueue('iot.controllers.cloud_company_hooks.create_influxdb', db_name=serialno, max_retry=max_retry, sleep=60)
			throw(r.text)
		else:
			frappe.logger(__name__).debug(r.text)
	except Exception as ex:
		frappe.logger(__name__).error(ex)
		if max_retry > 0:
			frappe.enqueue('iot.controllers.cloud_company_hooks.create_influxdb', db_name=serialno, max_retry=max_retry, sleep=60)
		throw(repr(ex))


def delete_serial(serialno, max_retry=10, sleep=None):
	pass
