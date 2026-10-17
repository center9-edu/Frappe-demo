# Copyright (c) 2026, dain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AssignmentSubmission(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		answer: DF.LongText
		assignment: DF.Link
		course: DF.Link | None
		feedback: DF.SmallText | None
		graded_by: DF.Link | None
		score: DF.Int
		status: DF.Literal["Submitted", "Graded"]
		student: DF.Link
	# end: auto-generated types

	_DOCTYPE_NAME = "Assignment Submission"

	def validate(self):
		if self.status != "Graded":
			return
		if not 0 <= (self.score or 0) <= 100:
			frappe.throw(_("Điểm phải từ 0 đến 100"), title=_("Điểm không hợp lệ"))
		if any(self.has_value_changed(f) for f in ("status", "score", "feedback")):
			self.graded_by = frappe.session.user
