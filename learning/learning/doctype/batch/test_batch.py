# Copyright (c) 2026, dain and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestBatch(IntegrationTestCase):
	def test_end_date_before_start_date(self):
		batch = frappe.get_doc(doctype="Batch", title="_Test", start_date="2026-02-01", end_date="2026-01-31")
		self.assertRaises(frappe.ValidationError, batch.validate)

		batch.end_date = "2026-02-01"
		batch.validate()
