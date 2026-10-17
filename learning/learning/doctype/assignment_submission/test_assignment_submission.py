# Copyright (c) 2026, dain and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

INSTRUCTOR = "_test-instructor@example.com"
STUDENT = "_test-student@example.com"


class IntegrationTestAssignmentSubmission(IntegrationTestCase):
	def setUp(self):
		for email, user_type, roles in (
			(INSTRUCTOR, "System User", ["Instructor"]),
			(STUDENT, "Website User", []),
		):
			if not frappe.db.exists("User", email):
				user = frappe.get_doc(doctype="User", email=email, first_name="Test", user_type=user_type)
				for role in roles:
					user.append("roles", {"role": role})
				user.insert()
		course = frappe.get_doc(doctype="Course", title="_Test Grading Course").insert()
		chapter = frappe.get_doc(doctype="Chapter", title="C1", course=course.name).insert()
		lesson = frappe.get_doc(doctype="Lesson", title="L1", chapter=chapter.name).insert()
		assignment = frappe.get_doc(
			doctype="Assignment", title="A1", lesson=lesson.name, question="Q"
		).insert()
		self.submission = frappe.get_doc(
			doctype="Assignment Submission", assignment=assignment.name, student=STUDENT, answer="v1"
		).insert()

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.db.rollback()

	def test_instructor_can_teach_and_grade_but_not_administer(self):
		allowed = [
			("Course", "create"),
			("Lesson", "delete"),
			("Assignment", "create"),
			("Batch", "write"),
			("Assignment Submission", "write"),
			("Lesson Progress", "read"),
		]
		denied = [
			("Course", "delete"),
			("Batch", "create"),
			("Assignment Submission", "create"),
			("Assignment Submission", "delete"),
			("Lesson Progress", "write"),
			("User", "create"),
			("System Settings", "write"),
			("DocType", "write"),
		]
		for doctype, ptype in allowed:
			self.assertTrue(frappe.has_permission(doctype, ptype, user=INSTRUCTOR), (doctype, ptype))
		for doctype, ptype in denied:
			self.assertFalse(frappe.has_permission(doctype, ptype, user=INSTRUCTOR), (doctype, ptype))

	def test_grading_checks_score_and_records_grader(self):
		frappe.set_user(INSTRUCTOR)
		sub = frappe.get_doc("Assignment Submission", self.submission.name)
		sub.status, sub.score = "Graded", 101
		self.assertRaises(frappe.ValidationError, sub.save)

		sub = frappe.get_doc("Assignment Submission", self.submission.name)
		sub.status, sub.score, sub.feedback = "Graded", 90, "Tốt"
		sub.save()
		self.assertEqual(sub.graded_by, INSTRUCTOR)
