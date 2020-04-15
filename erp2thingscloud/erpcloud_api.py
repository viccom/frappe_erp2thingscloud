#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import frappe
import json


@frappe.whitelist(allow_guest=True)
def sn_exists(sn=None):
	if not sn:
		sn = "TRTX011935000026"
	sn_exists = frappe.db.get_value("Serial Number list", {"serial_no": "TRTX011935000026"}, "serial_no")
	print(sn, sn_exists, sn == sn_exists)
	serialno_doc = frappe.get_doc("Serial Number list", sn)
	print("##################::::::::", serialno_doc.sync_status)
	serialno_doc.set("sync_status", 'successful')
	serialno_doc.save()
	print({sn_exists: serialno_doc.sync_status})
	return {sn_exists: serialno_doc.sync_status}
