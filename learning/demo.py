"""Demo data: bench --site <site> execute learning.demo.create_demo_data"""

import frappe
from frappe.utils import add_days, today
from frappe.utils.password import update_password

STUDENT = "student@example.com"
INSTRUCTOR = "instructor@example.com"
DEMO_PASSWORD = "demo@1234"

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


def _ensure_user(email, first_name, user_type, roles=()):
	if frappe.db.exists("User", email):
		return
	user = frappe.get_doc(
		doctype="User",
		email=email,
		first_name=first_name,
		last_name="Demo",
		user_type=user_type,
		send_welcome_email=0,
	)
	for role in roles:
		user.append("roles", {"role": role})
	user.insert(ignore_permissions=True)
	update_password(email, DEMO_PASSWORD)


def create_demo_data():
	_ensure_user(STUDENT, "Học viên", "Website User")
	_ensure_user(INSTRUCTOR, "Giảng viên", "System User", roles=["Instructor"])

	if frappe.db.exists("Course", "python-basics"):
		frappe.db.commit()
		print(f"Demo users ready ({STUDENT}, {INSTRUCTOR} / {DEMO_PASSWORD}); course already exists")
		return

	course = frappe.get_doc(
		doctype="Course",
		title="Python Basics",
		published=1,
		instructor=INSTRUCTOR,
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
		instructor=INSTRUCTOR,
		start_date=add_days(today(), 7),
		end_date=add_days(today(), 60),
	).insert()

	frappe.db.commit()
	print(f"Demo data created. Logins: {STUDENT}, {INSTRUCTOR} / {DEMO_PASSWORD}")
