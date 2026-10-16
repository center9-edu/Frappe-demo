# Learning: Demo LMS trên Frappe

App demo để học Frappe Framework: một hệ thống LMS nhỏ gồm **Course, Chapter, Lesson, Assignment, Batch**, có hai lớp giao diện:

| Giao diện | URL | Công nghệ | Dành cho |
|---|---|---|---|
| Website công khai | `/`, `/courses`, `/course/<slug>` | Jinja template + CSS riêng | Khách xem danh mục khoá học |
| Ứng dụng học viên | `/lms` | Vue 3 + [frappe-ui](https://ui.frappe.io) (SPA) | Học viên đã đăng nhập: ghi danh, học, nộp bài |
| Quản trị (Desk) | `/desk` | Desk có sẵn của Frappe | Giảng viên/Admin: soạn khoá học, chấm bài |

## Yêu cầu

| Thành phần | Phiên bản đã chạy thử |
|---|---|
| Frappe Framework | `develop` (v17) |
| Python | 3.14 |
| Node.js | 24 (tối thiểu 20.19) + Yarn 1.22 |
| MariaDB | 11.8 |
| Redis | 7+ |
| bench CLI | `uv tool install frappe-bench` |

Trên macOS: `brew install mariadb@11.8 redis node yarn` rồi `brew services start mariadb@11.8`.

## Cài đặt

```bash
# 1. Tạo bench với Frappe develop
bench init my-bench --frappe-branch develop
cd my-bench

# 2. Lấy app này (tự cài Python deps, yarn install và build frontend)
bench get-app git@github.com:center9-edu/Frappe-demo.git

# 3. Tạo site và cài app
bench new-site mysite.localhost
bench --site mysite.localhost install-app learning
bench --site mysite.localhost set-config developer_mode 1
bench use mysite.localhost

# 4. (Tuỳ chọn) Tạo dữ liệu mẫu: 1 khoá học, 4 bài, 1 bài tập, 1 lớp, 1 học viên
bench --site mysite.localhost execute learning.demo.create_demo_data

# 5. Chạy
bench start
```

Sau đó mở:

- http://localhost:8000: website công khai
- http://localhost:8000/lms: ứng dụng học viên, đăng nhập bằng `student@example.com` / `demo@1234` (tài khoản do bước 4 tạo, chỉ dùng cho môi trường local)
- http://localhost:8000/desk: quản trị, đăng nhập bằng `Administrator` / mật khẩu đặt ở bước 3

## Phát triển

```bash
bench start                              # luôn cần: web server, redis, worker...

# Sửa giao diện /lms có hot reload (terminal thứ 2)
cd apps/learning/frontend && yarn dev    # Vite chuyển tiếp API sang :8000

# Build lại /lms sau khi sửa .vue (nếu không dùng yarn dev)
bench build --app learning

# Test
bench --site mysite.localhost set-config allow_tests true
bench --site mysite.localhost run-tests --app learning
```

Khi bật `developer_mode`, mọi chỉnh sửa DocType trên Desk sẽ được ghi ngược vào file JSON trong `learning/learning/doctype/`. Nhớ commit các file đó.

## Cấu trúc

```
learning/                         ← repo
├── package.json                  ← script "build": bench build gọi để build frontend
├── frontend/                     ← SPA /lms (Vue 3 + frappe-ui + Tailwind)
│   └── src/
│       ├── router.js             ← route của /lms
│       ├── api.js                ← gọi /api/v2/method/learning.api.*
│       └── pages/                ← Courses, CourseDetail, Lesson, Submissions
└── learning/                     ← Python package
    ├── hooks.py                  ← home_page, website_route_rules
    ├── api.py                    ← API whitelist cho SPA (kiểm tra đăng nhập + ghi danh)
    ├── demo.py                   ← dữ liệu mẫu
    ├── www/                      ← trang theo file: courses, learn, lms (shell của SPA)
    ├── templates/lms_base.html   ← layout Jinja dùng chung
    ├── public/css/learning.css   ← style website công khai → /assets/learning/css/
    ├── tests/test_api.py
    └── learning/doctype/         ← module "Learning"
        ├── course/               ← có web view: /course/<slug>
        ├── chapter/  lesson/  assignment/
        ├── batch/  batch_student/        ← ghi danh = có tên trong bảng students của Batch
        └── lesson_progress/  assignment_submission/
```

`learning/public/frontend/` và `learning/www/lms.html` được sinh ra khi build, đã có trong `.gitignore`.

## Bản đồ route

| URL | Xử lý bởi |
|---|---|
| `/` | `hooks.py` → `home_page = "courses"` → `www/courses.py` + `.html` |
| `/courses` | `www/courses.py` + `courses.html` |
| `/course/<slug>` | DocType Course (`has_web_view`), route lưu trong cột `route` → `doctype/course/course.py` + `templates/course.html` |
| `/course/<slug>/learn/<lesson>` | `website_route_rules` → `www/learn.py` + `learn.html` |
| `/lms/*` | `website_route_rules` → `www/lms.py` (bắt đăng nhập, chèn `boot`) → Vue Router trong `frontend/src/router.js` |
| `/api/v2/method/learning.api.<fn>` | hàm `<fn>` có `@frappe.whitelist()` trong `learning/api.py` |

## Luồng nghiệp vụ

1. Admin soạn **Course → Chapter → Lesson → Assignment** và mở **Batch** trên Desk.
2. Học viên vào `/lms`, chọn khoá học rồi bấm **Ghi danh** vào một lớp.
3. Học viên học từng bài, bấm **Đánh dấu hoàn thành** (tạo `Lesson Progress`), và nộp bài tập (tạo `Assignment Submission`).
4. Giảng viên chấm bài tại `/desk/assignment-submission`: đặt Status = Graded, nhập Score và Feedback. Học viên thấy điểm và nhận xét ngay trong bài học.

## Lỗi thường gặp khi cài

| Triệu chứng | Nguyên nhân / cách xử lý |
|---|---|
| `This project is configured to use pnpm because ~/package.json has a "packageManager" field` | Có file `package.json` thừa ở thư mục home. Xoá hoặc đổi tên nó |
| `The Yarn Plug'n'Play manifest forbids importing "vue"` | Có `~/.pnp.cjs` (và `~/yarn.lock`) thừa ở home. Xoá hoặc chuyển đi chỗ khác |
| `Can't connect to server on '127.0.0.1'` khi `new-site` | MariaDB chưa chạy: `brew services start mariadb@11.8` |
| Không đăng nhập được MariaDB bằng `root` | Đặt mật khẩu: `mariadb -u $USER -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '...';"` |
| `localhost:8000` báo Not Found | Chưa có site mặc định: `bench use mysite.localhost` rồi khởi động lại `bench start` |
| `Cannot connect to redis_cache` | `bench start` chưa chạy |

## License

MIT
