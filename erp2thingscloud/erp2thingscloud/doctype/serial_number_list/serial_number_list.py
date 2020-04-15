# -*- coding: utf-8 -*-
# Copyright (c) 2020, viccom.dong and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class SerialNumberlist(Document):

	@staticmethod
	def repost_serialno(self):
		print("@@@repost_serialno@@@")
		pass
