# Copyright (c) 2026, dain and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from learning.learning.doctype.course.course import get_outline


class IntegrationTestLesson(IntegrationTestCase):
	def tearDown(self):
		frappe.db.rollback()

	def test_new_items_go_last_and_outline_follows_position(self):
		course = frappe.get_doc(doctype="Course", title="_Test Position Course").insert()
		ch1, ch2 = (
			frappe.get_doc(doctype="Chapter", title=t, course=course.name).insert() for t in ("C1", "C2")
		)
		l1, l2, l3 = (
			frappe.get_doc(doctype="Lesson", title=t, chapter=ch1.name).insert() for t in ("L1", "L2", "L3")
		)
		self.assertEqual((ch1.position, ch2.position), (1, 2))
		self.assertEqual((l1.position, l2.position, l3.position), (1, 2, 3))

		l3.position, l1.position = 1, 3
		l3.save()
		l1.save()
		ch2.position = 0
		ch2.save()

		outline = get_outline(course.name)
		self.assertEqual([c.name for c in outline], [ch2.name, ch1.name])
		self.assertEqual([l.name for l in outline[1].lessons], [l3.name, l2.name, l1.name])
