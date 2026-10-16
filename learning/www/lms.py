import frappe
from frappe.utils import get_fullname

no_cache = 1


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/lms"
		raise frappe.Redirect

	# frappe-ui's jinjaBootData copies each key onto `window` (window.csrf_token, window.user)
	context.boot = {
		"csrf_token": frappe.sessions.get_csrf_token(),
		"site_name": frappe.local.site,
		"user": {
			"name": frappe.session.user,
			"full_name": get_fullname(frappe.session.user),
			"user_image": frappe.db.get_value("User", frappe.session.user, "user_image"),
		},
	}
