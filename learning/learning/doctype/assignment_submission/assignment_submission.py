# Copyright (c) 2026, dain and contributors
# For license information, please see license.txt

# import frappe
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
		score: DF.Int
		status: DF.Literal["Submitted", "Graded"]
		student: DF.Link
	# end: auto-generated types

	_DOCTYPE_NAME = "Assignment Submission"
