#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Erp2ThingsCloud Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "ThingsCloud Settings",
					"onboard": 1,
					"description": _("ThingsCloud Settings"),
				}
			]
		}
	]
