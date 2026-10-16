"""Demo data: bench --site <site> execute learning.demo.create_demo_data"""

import frappe
from frappe.utils import add_days, today
from frappe.utils.password import update_password

STUDENT = "student@example.com"
STUDENT_PASSWORD = "demo@1234"

OUTLINE = {
	"Getting Started": {
		"Install Python": "<p>Tải Python 3 tại <a href='https://python.org'>python.org</a> và kiểm tra bằng <code>python3 --version</code>.</p>",
		"Hello World": "<pre>print('Hello, World!')</pre><p>Chạy file bằng <code>python3 hello.py</code>.</p>",
	},
	"Data Types": {
		"Numbers & Strings": "<p>Python có <code>int</code>, <code>float</code> và <code>str</code>.</p>",
		"Lists & Dicts": "<pre>fruits = ['apple', 'banana']\nprices = {'apple': 1.5}</pre>",
	},
}


def create_demo_data():
	if not frappe.db.exists("User", STUDENT):
		frappe.get_doc(
			doctype="User",
			email=STUDENT,
			first_name="Học viên",
			last_name="Demo",
			user_type="Website User",
			send_welcome_email=0,
		).insert(ignore_permissions=True)
		update_password(STUDENT, STUDENT_PASSWORD)

	if frappe.db.exists("Course", "python-basics"):
		print("Demo data already exists")
		return

	course = frappe.get_doc(
		doctype="Course",
		title="Python Basics",
		published=1,
		instructor="Administrator",
		short_intro="Learn Python from scratch.",
		description="<p>A demo course built on Frappe.</p>",
	).insert()

	lesson = None
	for chapter_title, lessons in OUTLINE.items():
		chapter = frappe.get_doc(doctype="Chapter", title=chapter_title, course=course.name).insert()
		for title, content in lessons.items():
			lesson = frappe.get_doc(
				doctype="Lesson", title=title, chapter=chapter.name, content=content
			).insert()

	frappe.get_doc(
		doctype="Assignment",
		title="Write a calculator",
		lesson=lesson.name,
		submission_type="URL",
		question="<p>Build a CLI calculator and submit the repo URL.</p>",
	).insert()

	frappe.get_doc(
		doctype="Batch",
		title="Python Basics - K1",
		course=course.name,
		instructor="Administrator",
		start_date=add_days(today(), 7),
		end_date=add_days(today(), 60),
	).insert()

	frappe.db.commit()
	print(f"Demo data created. Student login: {STUDENT} / {STUDENT_PASSWORD}")
