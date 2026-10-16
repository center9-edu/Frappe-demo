import frappe

from learning.learning.doctype.course.course import get_outline

no_cache = 1


def get_context(context):
	course_name, lesson_name = frappe.form_dict.course, frappe.form_dict.lesson
	course = frappe.db.get_value(
		"Course", {"name": course_name, "published": 1}, ["name", "title", "route"], as_dict=True
	)
	if not course or not frappe.db.exists("Lesson", {"name": lesson_name, "course": course.name}):
		raise frappe.DoesNotExistError

	chapters = get_outline(course.name)
	lessons = [l for ch in chapters for l in ch.lessons]
	i = next(i for i, l in enumerate(lessons) if l.name == lesson_name)

	context.course = course
	context.chapters = chapters
	context.lesson = frappe.get_doc("Lesson", lesson_name)
	context.prev = lessons[i - 1] if i > 0 else None
	context.next = lessons[i + 1] if i + 1 < len(lessons) else None
	context.position = f"{i + 1}/{len(lessons)}"
	context.assignments = frappe.get_all(
		"Assignment", {"lesson": lesson_name}, ["title", "submission_type", "question"], order_by="creation"
	)
	context.title = f"{context.lesson.title} · {course.title}"
