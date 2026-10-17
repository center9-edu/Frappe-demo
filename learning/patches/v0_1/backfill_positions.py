import frappe


def execute():
	"""Number existing chapters and lessons in their old (creation) order."""
	for course in frappe.get_all("Course", pluck="name"):
		chapters = frappe.get_all("Chapter", {"course": course}, ["name", "position"], order_by="creation")
		for i, ch in enumerate(chapters, 1):
			if not ch.position:
				frappe.db.set_value("Chapter", ch.name, "position", i, update_modified=False)
			lessons = frappe.get_all(
				"Lesson", {"chapter": ch.name}, ["name", "position"], order_by="creation"
			)
			for j, lesson in enumerate(lessons, 1):
				if not lesson.position:
					frappe.db.set_value("Lesson", lesson.name, "position", j, update_modified=False)
