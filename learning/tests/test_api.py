import frappe
from frappe.tests import IntegrationTestCase

from learning import api

STUDENT = "lms-api-test@example.com"


class TestLearningAPI(IntegrationTestCase):
	def setUp(self):
		if not frappe.db.exists("User", STUDENT):
			frappe.get_doc(
				doctype="User", email=STUDENT, first_name="Test", user_type="Website User"
			).insert()
		self.course = frappe.get_doc(doctype="Course", title="_Test API Course", published=1).insert()
		chapter = frappe.get_doc(doctype="Chapter", title="Ch 1", course=self.course.name).insert()
		self.lessons = [
			frappe.get_doc(doctype="Lesson", title=f"L{i}", chapter=chapter.name).insert().name
			for i in (1, 2)
		]
		self.assignment = (
			frappe.get_doc(doctype="Assignment", title="A1", lesson=self.lessons[1], question="Q")
			.insert()
			.name
		)
		self.batch = (
			frappe.get_doc(
				doctype="Batch", title="_Test API Batch", course=self.course.name, start_date="2099-01-01"
			)
			.insert()
			.name
		)
		frappe.set_user(STUDENT)

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.db.rollback()

	def test_lessons_and_submissions_require_enrollment(self):
		self.assertRaises(frappe.PermissionError, api.get_lesson, self.course.name, self.lessons[0])
		self.assertRaises(frappe.PermissionError, api.set_lesson_completed, self.lessons[0])
		self.assertRaises(frappe.PermissionError, api.submit_assignment, self.assignment, "answer")

	def test_enroll_progress_and_submit(self):
		api.enroll(self.batch)
		self.assertTrue(api.get_course(self.course.name)["enrolled"])

		self.assertEqual(api.set_lesson_completed(self.lessons[0])["progress"], 50)
		self.assertEqual(api.get_course(self.course.name)["next_lesson"], self.lessons[1])
		self.assertEqual(api.set_lesson_completed(self.lessons[0], False)["progress"], 0)

		api.submit_assignment(self.assignment, "v1")
		api.submit_assignment(self.assignment, "v2")
		subs = frappe.get_all("Assignment Submission", {"student": STUDENT}, ["answer", "status"])
		self.assertEqual(subs, [{"answer": "v2", "status": "Submitted"}])

	def test_graded_submission_is_locked(self):
		api.enroll(self.batch)
		name = api.submit_assignment(self.assignment, "v1")["name"]
		frappe.db.set_value("Assignment Submission", name, "status", "Graded")
		self.assertRaises(frappe.ValidationError, api.submit_assignment, self.assignment, "v2")

	def test_lesson_must_belong_to_course(self):
		api.enroll(self.batch)
		other = frappe.get_all("Lesson", {"course": ["!=", self.course.name]}, pluck="name", limit=1)
		if other:
			self.assertRaises(frappe.DoesNotExistError, api.get_lesson, self.course.name, other[0])

	def test_guest_is_rejected(self):
		frappe.set_user("Guest")
		self.assertRaises(frappe.AuthenticationError, api.get_courses)
