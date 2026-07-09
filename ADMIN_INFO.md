# Django Admin & Search — Setup Notes

## Django Administration

The Django admin panel is already configured and accessible at:

**URL:** `http://127.0.0.1:8000/admin/`

### Default Login Credentials

| Username  | Password   | Role        |
|-----------|------------|-------------|
| `admin`   | `admin123` | Superuser   |
| `akshaya` | `admin123` | Superuser   |

> **Note:** Change passwords in production!

### If you need to reset/create an admin user:
```bash
python manage.py ensure_admin
# or with custom credentials:
python manage.py ensure_admin --username myuser --password mypassword
```

Or using the standard Django way:
```bash
python manage.py createsuperuser
```

---

## Dashboard Search

A global search bar is now available:
- **In the topbar** (visible on all pages) — quick search from anywhere
- **On the Dashboard page** — search with type filter (Orders / Customers / Products)
- **Search Results page** — detailed results at `/dashboard/search/?q=your+query`

### What can be searched:
- **Orders** — by order number, customer name
- **Customers** — by name, email, phone
- **Products** — by name, SKU, description

