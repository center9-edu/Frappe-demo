# Copyright (c) 2026, dain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class Batch(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from learning.learning.doctype.batch_student.batch_student import BatchStudent

		course: DF.Link
		end_date: DF.Date | None
		instructor: DF.Link | None
		start_date: DF.Date
		students: DF.Table[BatchStudent]
		title: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Batch"

	def validate(self):
		if self.end_date and getdate(self.end_date) < getdate(self.start_date):
			frappe.throw(_("End Date cannot be before Start Date"), title=_("Invalid Dates"))
