import frappe
from frappe import _
from frappe.utils import get_fullname, today

from learning.learning.doctype.course.course import get_outline


def _user():
	if frappe.session.user == "Guest":
		frappe.throw(_("Vui lòng đăng nhập"), frappe.AuthenticationError)
	return frappe.session.user


def _enrolled_courses(user):
	batches = frappe.get_all("Batch Student", {"student": user, "parenttype": "Batch"}, pluck="parent")
	return set(frappe.get_all("Batch", {"name": ["in", batches]}, pluck="course")) if batches else set()


def _check_enrolled(user, course):
	if course not in _enrolled_courses(user):
		frappe.throw(_("Bạn chưa ghi danh khoá học này"), frappe.PermissionError)


def _published_course(course):
	if not frappe.db.exists("Course", {"name": course, "published": 1}):
		raise frappe.DoesNotExistError(_("Không tìm thấy khoá học"))


def _completed_lessons(user, course):
	return set(frappe.get_all("Lesson Progress", {"student": user, "course": course}, pluck="lesson"))


def _percent(done, total):
	return round(done * 100 / total) if total else 0


@frappe.whitelist()
def get_session():
	user = _user()
	return {
		"user": user,
		"full_name": get_fullname(user),
		"user_image": frappe.db.get_value("User", user, "user_image"),
	}


@frappe.whitelist()
def get_courses():
	user = _user()
	enrolled = _enrolled_courses(user)
	courses = frappe.get_all(
		"Course",
		{"published": 1},
		["name", "title", "short_intro", "image", "instructor"],
		order_by="creation desc",
	)
	lesson_counts = dict(
		frappe.get_all("Lesson", fields=["course", {"COUNT": "name"}], group_by="course", as_list=True)
	)
	done_counts = dict(
		frappe.get_all(
			"Lesson Progress",
			{"student": user},
			["course", {"COUNT": "name"}],
			group_by="course",
			as_list=True,
		)
	)
	for c in courses:
		c.lesson_count = lesson_counts.get(c.name, 0)
		c.instructor_name = c.instructor and get_fullname(c.instructor)
		c.enrolled = c.name in enrolled
		c.progress = _percent(done_counts.get(c.name, 0), c.lesson_count)
	return courses


@frappe.whitelist()
def get_course(course: str):
	user = _user()
	_published_course(course)
	doc = frappe.get_doc("Course", course)
	completed = _completed_lessons(user, course)

	chapters = get_outline(course)
	lessons = [l for ch in chapters for l in ch.lessons]
	for l in lessons:
		l.completed = l.name in completed

	batches = frappe.get_all(
		"Batch",
		{"course": course},
		["name", "title", "start_date", "end_date"],
		or_filters=[["end_date", ">=", today()], ["end_date", "is", "not set"]],
		order_by="start_date",
	)
	for b in batches:
		students = frappe.get_all("Batch Student", {"parent": b.name, "parenttype": "Batch"}, pluck="student")
		b.student_count = len(students)
		b.is_member = user in students

	return {
		"name": doc.name,
		"title": doc.title,
		"short_intro": doc.short_intro,
		"description": doc.description,
		"image": doc.image,
		"instructor_name": doc.instructor and get_fullname(doc.instructor),
		"chapters": chapters,
		"batches": batches,
		"enrolled": course in _enrolled_courses(user),
		"progress": _percent(len(completed), len(lessons)),
		"lesson_count": len(lessons),
		"next_lesson": next(
			(l.name for l in lessons if not l.completed), lessons[0].name if lessons else None
		),
	}


@frappe.whitelist(methods=["POST"])
def enroll(batch: str):
	user = _user()
	doc = frappe.get_doc("Batch", batch)
	_published_course(doc.course)
	if doc.end_date and str(doc.end_date) < today():
		frappe.throw(_("Lớp này đã kết thúc"))
	if not any(s.student == user for s in doc.students):
		doc.append("students", {"student": user})
		doc.save(ignore_permissions=True)
	return {"course": doc.course}


@frappe.whitelist()
def get_lesson(course: str, lesson: str):
	user = _user()
	_published_course(course)
	_check_enrolled(user, course)
	if not frappe.db.exists("Lesson", {"name": lesson, "course": course}):
		raise frappe.DoesNotExistError(_("Không tìm thấy bài học"))

	completed = _completed_lessons(user, course)
	chapters = get_outline(course)
	lessons = [l for ch in chapters for l in ch.lessons]
	for l in lessons:
		l.completed = l.name in completed
	i = next(i for i, l in enumerate(lessons) if l.name == lesson)

	doc = frappe.get_doc("Lesson", lesson)
	assignments = frappe.get_all(
		"Assignment",
		{"lesson": lesson},
		["name", "title", "question", "submission_type"],
		order_by="creation",
	)
	for a in assignments:
		a.submission = frappe.db.get_value(
			"Assignment Submission",
			{"assignment": a.name, "student": user},
			["name", "answer", "status", "score", "feedback", "modified"],
			as_dict=True,
		)

	return {
		"name": doc.name,
		"title": doc.title,
		"content": doc.content,
		"video_url": doc.video_url,
		"completed": lesson in completed,
		"course_title": frappe.db.get_value("Course", course, "title"),
		"chapters": chapters,
		"assignments": assignments,
		"position": i + 1,
		"total": len(lessons),
		"progress": _percent(len(completed), len(lessons)),
		"prev": lessons[i - 1] if i > 0 else None,
		"next": lessons[i + 1] if i + 1 < len(lessons) else None,
	}


@frappe.whitelist(methods=["POST"])
def set_lesson_completed(lesson: str, completed: bool = True):
	user = _user()
	course = frappe.db.get_value("Lesson", lesson, "course")
	_check_enrolled(user, course)
	existing = frappe.db.get_value("Lesson Progress", {"student": user, "lesson": lesson})
	if completed and not existing:
		frappe.get_doc(doctype="Lesson Progress", student=user, lesson=lesson).insert(ignore_permissions=True)
	elif not completed and existing:
		frappe.delete_doc("Lesson Progress", existing, ignore_permissions=True)
	return {
		"progress": _percent(
			len(_completed_lessons(user, course)), frappe.db.count("Lesson", {"course": course})
		)
	}


@frappe.whitelist(methods=["POST"])
def submit_assignment(assignment: str, answer: str):
	user = _user()
	course = frappe.db.get_value("Assignment", assignment, "course")
	_check_enrolled(user, course)
	if not answer.strip():
		frappe.throw(_("Bài nộp không được để trống"))

	name = frappe.db.get_value("Assignment Submission", {"assignment": assignment, "student": user})
	if name:
		doc = frappe.get_doc("Assignment Submission", name)
		if doc.status == "Graded":
			frappe.throw(_("Bài đã được chấm, không thể nộp lại"))
		doc.answer = answer
		doc.save(ignore_permissions=True)
	else:
		doc = frappe.get_doc(
			doctype="Assignment Submission", assignment=assignment, student=user, answer=answer
		).insert(ignore_permissions=True)
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def get_my_submissions():
	user = _user()
	rows = frappe.get_all(
		"Assignment Submission",
		{"student": user},
		["name", "assignment", "course", "status", "score", "feedback", "modified"],
		order_by="modified desc",
	)
	for r in rows:
		r.assignment_title, r.lesson = frappe.db.get_value("Assignment", r.assignment, ["title", "lesson"])
		r.course_title = frappe.db.get_value("Course", r.course, "title")
	return rows
