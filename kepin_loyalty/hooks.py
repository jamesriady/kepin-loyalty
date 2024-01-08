# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "kepin_loyalty"
app_title = "Kepin Loyalty"
app_publisher = "James Riady"
app_description = "Kepin Loyalty System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jamesriady1998@gmail.com"
app_license = "\'kepin_loyalty\' created at /home/frappe/frappe-bench/apps/kepin_loyalty"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kepin_loyalty/css/kepin_loyalty.css"
# app_include_js = "/assets/kepin_loyalty/js/kepin_loyalty.js"

# include js, css files in header of web template
# web_include_css = "/assets/kepin_loyalty/css/kepin_loyalty.css"
# web_include_js = "/assets/kepin_loyalty/js/kepin_loyalty.js"

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
# get_website_user_home_page = "kepin_loyalty.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "kepin_loyalty.install.before_install"
# after_install = "kepin_loyalty.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kepin_loyalty.notifications.get_notification_config"

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
	"Sales Invoice": {
		"on_submit": "kepin_loyalty.accounts.doctype.sales_invoice.sales_invoice.on_claim_loyalty_point",
		"on_cancel": "kepin_loyalty.accounts.doctype.sales_invoice.sales_invoice.on_cancel_claim_loyalty_point"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"kepin_loyalty.tasks.all"
# 	],
# 	"daily": [
# 		"kepin_loyalty.tasks.daily"
# 	],
# 	"hourly": [
# 		"kepin_loyalty.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kepin_loyalty.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kepin_loyalty.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kepin_loyalty.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kepin_loyalty.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "kepin_loyalty.task.get_dashboard_data"
# }