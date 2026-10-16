import frappe

no_cache = 1


def get_context(context):
	courses = frappe.get_all(
		"Course",
		{"published": 1},
		["name", "title", "short_intro", "image", "route", "instructor"],
		order_by="creation desc",
	)
	lesson_counts = dict(
		frappe.get_all("Lesson", fields=["course", {"COUNT": "name"}], group_by="course", as_list=True)
	)
	for c in courses:
		c.lesson_count = lesson_counts.get(c.name, 0)
		c.instructor_name = c.instructor and frappe.db.get_value("User", c.instructor, "full_name")

	context.courses = courses
	context.title = "Khoá học"
