# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erp2thingscloud"
app_title = "Erp2Thingscloud"
app_publisher = "viccom.dong"
app_description = "epr2thingscloud"
app_icon = "octicon  octicon-squirrel"
app_color = "camel"
app_email = "viccom.dong@thingsroot.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erp2thingscloud/css/erp2thingscloud.css"
# app_include_js = "/assets/erp2thingscloud/js/erp2thingscloud.js"

# include js, css files in header of web template
# web_include_css = "/assets/erp2thingscloud/css/erp2thingscloud.css"
# web_include_js = "/assets/erp2thingscloud/js/erp2thingscloud.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erp2thingscloud.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erp2thingscloud.install.before_install"
# after_install = "erp2thingscloud.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erp2thingscloud.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# },
	"Serial No": {
		"after_insert": "erp2thingscloud.controllers.item_serial_event_hooks.after_insert",
		"after_delete": "erp2thingscloud.controllers.item_serial_event_hooks.after_delete"
	}

}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"erp2thingscloud.tasks.resend.resend_failed_serials"
	],
	# "daily": [
	# 	"erp2thingscloud.tasks.daily"
	# ],
	# "hourly": [
	# 	"erp2thingscloud.tasks.hourly"
	# ],
	# "weekly": [
	# 	"erp2thingscloud.tasks.weekly"
	# ]
	# "monthly": [
	# 	"erp2thingscloud.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "erp2thingscloud.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erp2thingscloud.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erp2thingscloud.task.get_dashboard_data"
# }

