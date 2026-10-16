# Copyright (c) 2026, dain and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Course(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.TextEditor | None
		image: DF.AttachImage | None
		instructor: DF.Link | None
		published: DF.Check
		route: DF.Data | None
		short_intro: DF.SmallText | None
		title: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Course"

	def get_context(self, context):
		context.chapters = get_outline(self.name)
		context.lessons = [l for ch in context.chapters for l in ch.lessons]
		context.assignment_count = frappe.db.count("Assignment", {"course": self.name})
		context.instructor_name = self.instructor and frappe.db.get_value(
			"User", self.instructor, "full_name"
		)
		context.batches = frappe.get_all(
			"Batch",
			{"course": self.name, "start_date": [">=", frappe.utils.today()]},
			["title", "start_date", "end_date"],
			order_by="start_date",
		)


def get_outline(course):
	chapters = frappe.get_all("Chapter", {"course": course}, ["name", "title"], order_by="creation")
	lessons = frappe.get_all("Lesson", {"course": course}, ["name", "chapter", "title"], order_by="creation")
	for ch in chapters:
		ch.lessons = [l for l in lessons if l.chapter == ch.name]
	return chapters
