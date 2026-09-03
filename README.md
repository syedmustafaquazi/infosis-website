# Infosis SecuritySystem L.L.C — Updated Django Website

A responsive corporate website for Infosis SecuritySystem L.L.C with service/solution detail pages and a database-backed enquiry system.

## Features
- Responsive corporate home page
- Hero slider
- Services and Solutions dropdowns
- Separate responsive detail interface for every service/solution
- Technology partner and client logo sections
- Contact/enquiry form
- Enquiries saved in SQLite database
- Staff enquiry dashboard
- Django Admin
- Email notification support via SMTP environment variables

## Run on Windows / VS Code

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Django Admin: http://127.0.0.1:8000/admin/

## Important
Run the website with `python manage.py runserver`. Do not open `templates/index.html` directly with Live Server or by double-clicking it, because Django template tags such as `{% static %}` and `{% url %}` need Django to render them.

## Enquiry data
Every valid enquiry is saved in `db.sqlite3` in the `enquiries_enquiry` table. Staff users can review and change status from the dashboard.
