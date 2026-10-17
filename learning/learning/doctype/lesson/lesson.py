# Copyright (c) 2026, dain and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from learning.learning.doctype.course.course import next_position


class Lesson(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		chapter: DF.Link
		content: DF.TextEditor | None
		course: DF.Link | None
		position: DF.Int
		title: DF.Data
		video_url: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Lesson"

	def before_insert(self):
		if not self.position:
			self.position = next_position("Lesson", {"chapter": self.chapter})
