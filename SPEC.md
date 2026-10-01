# SPEC.md: Plastic Distribution Agency Management System (MVP)

> Read this file fully before writing any code. Follow it exactly. If something is unclear or missing, ask before assuming. Do not add features outside the MVP scope.

## 1. Project overview

An agency sells plastic products from multiple companies to retail stores across different areas. Sales workers visit stores and take orders. The admin manages workers, stock, and orders, and watches worker attendance and live location.

**Goal:** a working, deployed MVP in 2 weeks.

**Users:**
- **Admin:** full access to everything.
- **Worker (sales):** limited access, used from a phone browser (PWA).

## 2. Tech stack (fixed, do not substitute)

| Layer | Choice |
|---|---|
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL |
| ORM / migrations | SQLAlchemy 2.x, Alembic |
| Auth | JWT (access token), bcrypt password hashing |
| Real-time | FastAPI WebSockets |
| Frontend | React + Vite, Tailwind CSS, shadcn/ui |
| Map | Leaflet + OpenStreetMap |
| Charts | Recharts |
| PDF invoices | WeasyPrint (or ReportLab) |
| Files | Cloudinary (selfie on check-in, optional) |
| Deploy | Docker; Render/Railway (backend + DB), Vercel (frontend) |

## 3. Scope

### In scope (MVP)
1. Login with roles (admin, worker)
2. Worker management (add, edit, deactivate)
3. Attendance: check-in / check-out with GPS
4. Live location: workers send position, admin sees a live map
5. Stores: list with area
6. Products and stock (stock changes only through movements)
7. Orders: worker creates, admin manages status
8. Simple PDF invoice per order (no GST)
9. Admin dashboard with summary cards

### Out of scope (phase 2, do NOT build)
GST calculation, payments and dues aging, credit limits, targets and incentives, payroll, leave, multiple godowns, purchase orders and suppliers, offline sync, native mobile app, extra roles (manager/accountant), notifications, activity log.

## 4. Roles and permissions

| Action | Admin | Worker |
|---|---|---|
| Manage workers | Yes | No |
| View all attendance | Yes | Own only |
| Check in / out | No | Yes |
| Send location | No | Yes |
| View live map | Yes | No |
| Manage stores | Yes | Add store (status `pending`), view assigned area stores |
| Manage products | Yes | View only, **cannot see `purchase_price`** |
| Stock movements | Yes | No |
| Create order | Yes | Yes (for own stores) |
| View orders | All | Own only |
| Change order status | Yes | No (can cancel own order while `placed`) |
| Download invoice | Yes | Own orders only |
| Dashboard | Yes | No |

Enforce permissions in the backend with dependencies (`require_admin`, `get_current_user`), never only in the UI.

## 5. Data model

Use UUID primary keys (or integer IDs, but be consistent). All tables have `created_at` and `updated_at` (UTC timestamps). Use `Numeric(12,2)` for all money values, never float.

### users
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| name | str | |
| phone | str, unique | used as login |
| email | str, nullable | |
| password_hash | str | bcrypt |
| role | enum(`admin`,`worker`) | |
| area_id | FK areas, nullable | assigned area for workers |
| is_active | bool | default true; inactive users cannot log in |

### areas
| Column | Type |
|---|---|
| id | PK |
| name | str, unique |

### stores
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| name | str | |
| owner_name | str | |
| phone | str | |
| address | text | |
| area_id | FK areas | |
| latitude, longitude | float, nullable | |
| status | enum(`pending`,`approved`) | worker-added stores start `pending` |
| created_by | FK users | |

### products
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| name | str | |
| company | str | brand/manufacturer |
| category | str | e.g. buckets, chairs, storage |
| sku | str, unique | |
| unit | enum(`piece`,`carton`,`kg`) | |
| purchase_price | Numeric | admin only |
| selling_price | Numeric | |
| low_stock_threshold | int | default 10 |
| is_active | bool | |

### stock_movements
Stock is **never edited directly**. Current stock = sum of movements.

| Column | Type | Notes |
|---|---|---|
| id | PK | |
| product_id | FK products | |
| quantity | int | positive = in, negative = out |
| type | enum(`purchase_in`,`sale_out`,`return_in`,`adjustment`) | |
| order_id | FK orders, nullable | set for `sale_out` / `return_in` |
| note | text, nullable | required for `adjustment` |
| created_by | FK users | |

### orders
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| order_number | str, unique | e.g. `ORD-2026-000123`, sequential |
| store_id | FK stores | |
| worker_id | FK users | |
| status | enum | see section 6 |
| total_amount | Numeric | computed server-side |
| note | text, nullable | |

### order_items
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| order_id | FK orders | |
| product_id | FK products | |
| quantity | int, > 0 | |
| unit_price | Numeric | **copied from product at order time**; later price changes must not alter old orders |
| line_total | Numeric | quantity x unit_price |

### attendance
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| worker_id | FK users | |
| date | date | |
| check_in_at | timestamptz | |
| check_in_lat, check_in_lng | float | |
| check_in_photo_url | str, nullable | Cloudinary |
| check_out_at | timestamptz, nullable | |
| check_out_lat, check_out_lng | float, nullable | |

Unique constraint: one attendance row per (worker_id, date).

### locations
| Column | Type | Notes |
|---|---|---|
| id | PK | |
| worker_id | FK users | index |
| latitude, longitude | float | |
| accuracy | float, nullable | metres |
| recorded_at | timestamptz | index (worker_id, recorded_at) |

## 6. Business rules

### Order status flow
`placed` -> `approved` -> `packed` -> `dispatched` -> `delivered`
Also: `cancelled` (allowed from `placed` or `approved` only).

- Only admin can move an order forward.
- Only allowed transitions are valid; reject anything else with 400.
- **Stock check on approve:** reject approval if any item's current stock is less than the ordered quantity (return which product is short).
- **Stock deduction on dispatch:** when status becomes `dispatched`, create one `sale_out` movement (negative quantity) per item, in a single database transaction with the status change.
- If a dispatched order is later cancelled or returned, create a `return_in` movement. (For MVP, returns are handled by an admin action `POST /orders/{id}/return` on delivered/dispatched orders.)

### Stock
- `current_stock(product) = SUM(stock_movements.quantity)`.
- Never allow current stock to go below 0.
- Low stock = current stock <= `low_stock_threshold`.

### Attendance
- A worker can check in once per day. A second check-in returns 400.
- Check-out requires an existing check-in for that day with no check-out.
- Location updates are accepted only while the worker is checked in and not checked out.

### Location
- Worker client sends location every 60 to 120 seconds while checked in.
- Server stores every point in `locations` and broadcasts the latest to connected admins via WebSocket.
- Live map shows each worker's latest point, name, last-seen time, and marks workers with no update for 10+ minutes as "stale".
- Route history: admin can select a worker and a date to see the day's path as a polyline.

### Orders and prices
- Server calculates `line_total` and `total_amount`. Never trust totals from the client.
- Workers can only order for stores in `approved` status.
- Inactive products cannot be ordered.

### Invoice
- One PDF per order, generated on demand: agency header, order number, date, store details, item table (product, qty, unit price, line total), grand total, worker name. No tax logic in MVP.

### Auth
- Login with phone + password, returns JWT (expiry 12 hours).
- Deactivated users are rejected on every request, not just at login.
- Never return `password_hash` in any response.

## 7. API design

Base path `/api/v1`. JSON in/out. Use Pydantic schemas for all requests and responses. Paginate list endpoints (`?page=&page_size=`). Standard error format: `{ "detail": "message" }`.

### Auth
- `POST /auth/login`
- `GET /auth/me`

### Workers (admin)
- `GET /workers`, `POST /workers`, `GET /workers/{id}`, `PATCH /workers/{id}`
- `PATCH /workers/{id}/deactivate`

### Areas (admin)
- `GET /areas`, `POST /areas`

### Stores
- `GET /stores` (admin: all; worker: own area, approved + own pending)
- `POST /stores` (worker creates as `pending`; admin creates as `approved`)
- `PATCH /stores/{id}` (admin)
- `PATCH /stores/{id}/approve` (admin)

### Products and stock
- `GET /products` (hide `purchase_price` for workers; include `current_stock`)
- `POST /products`, `PATCH /products/{id}` (admin)
- `POST /stock/movements` (admin; types `purchase_in`, `adjustment`)
- `GET /stock/movements?product_id=`
- `GET /stock/low`

### Orders
- `POST /orders` (worker or admin)
- `GET /orders?status=&store_id=&worker_id=&date_from=&date_to=`
- `GET /orders/{id}`
- `PATCH /orders/{id}/status` (admin)
- `POST /orders/{id}/cancel`
- `POST /orders/{id}/return` (admin)
- `GET /orders/{id}/invoice` (returns PDF)

### Attendance
- `POST /attendance/check-in` (body: lat, lng, optional photo)
- `POST /attendance/check-out` (body: lat, lng)
- `GET /attendance?date=&worker_id=` (admin: all; worker: own)
- `GET /attendance/today` (admin: who is present, absent, late)

### Location
- `POST /locations` (worker; body: lat, lng, accuracy)
- `GET /locations/latest` (admin; latest point per active worker)
- `GET /locations/history?worker_id=&date=` (admin)
- `WS /ws/locations` (admin only, authenticate via token query param; server pushes `{worker_id, name, lat, lng, recorded_at}` on every new point)

### Dashboard (admin)
- `GET /dashboard/summary` returns: today's sales total, today's order count, orders by status, workers present / absent, low-stock count, top worker this month.

## 8. Frontend screens

### Admin (desktop-first, responsive)
1. Login
2. Dashboard: summary cards, sales-last-7-days chart, low-stock list
3. Live Map: Leaflet map with worker markers (updating over WebSocket), side list of workers with last-seen; click a worker to view route history by date
4. Attendance: table by date with check-in / out times and location links
5. Workers: list, add/edit form, activate/deactivate
6. Stores: list with filters (area, status), add/edit, approve pending
7. Products and Stock: list with current stock, add/edit product, stock-in form, movement history
8. Orders: table with filters and status badges, order detail page with status action buttons and invoice download

### Worker (mobile-first PWA, big buttons)
1. Login
2. Home: today's status, big **Check in / Check out** button, location-sharing indicator
3. Stores: list of assigned-area stores, add new store
4. New Order: choose store, add products with quantity, review total, submit
5. My Orders: list and detail

### Worker location behaviour
- After check-in, use `navigator.geolocation.watchPosition` and send a point at most every 60 to 120 seconds.
- Use the Screen Wake Lock API to keep the screen on where supported.
- Show a clear banner: "Location sharing is ON" while checked in. Stop sending after check-out.
- Known limitation (document in README): a PWA cannot track reliably when the screen is off. A native app is phase 2.

## 9. Suggested folder structure

```
agency-app/
  SPEC.md
  README.md
  docker-compose.yml
  backend/
    app/
      main.py
      core/        (config.py, security.py, database.py)
      models/      (one file per table)
      schemas/     (pydantic)
      api/
        deps.py    (get_current_user, require_admin)
        routes/    (auth, workers, stores, products, stock, orders,
                    attendance, locations, dashboard)
      services/    (order_service.py, stock_service.py, invoice_service.py,
                    ws_manager.py)
    alembic/
    tests/
    seed.py
    requirements.txt
  frontend/
    src/
      api/         (axios client, per-resource hooks)
      components/
      pages/
        admin/
        worker/
      auth/        (AuthContext, ProtectedRoute)
    package.json
```

Keep business logic (stock, order transitions) in `services/`, not inside route functions.

## 10. Seed data (`backend/seed.py`)

Create:
- 1 admin (`9999999999` / `admin123`) and 5 workers (`password123`)
- 4 areas, 15 stores spread across areas (with lat/lng)
- 30 products across 4 companies and 5 categories, each with initial `purchase_in` stock
- 25 orders in mixed statuses, with matching stock movements for dispatched ones
- 7 days of attendance and several hours of location points for 3 workers (so the map and route history demo well)

## 11. Testing requirements

Write pytest tests for at least:
1. Stock is computed correctly from movements
2. Approval fails when stock is insufficient
3. Dispatch creates the correct `sale_out` movements atomically
4. Invalid status transitions are rejected
5. Order totals are computed server-side and `unit_price` is frozen at order time
6. Worker cannot see other workers' orders, and cannot see `purchase_price`
7. Double check-in is rejected; location POST rejected when not checked in
8. Deactivated user cannot access any endpoint

## 12. Non-functional rules

- All secrets in environment variables (`.env`, with `.env.example` committed).
- CORS restricted to the frontend origin.
- Input validation on every endpoint (positive quantities, valid lat/lng ranges, phone format).
- Use database transactions for anything that touches more than one table.
- Store all timestamps in UTC; the frontend displays in IST (Asia/Kolkata).
- No `print` debugging in committed code; use `logging`.
- Small, focused commits with clear messages.

## 13. Build order (vertical slices)

Finish each slice (model, migration, API, tests, then UI) before starting the next.

1. Project setup, DB connection, Alembic, Docker Compose
2. Auth, users, roles, areas
3. Stores
4. Products and stock movements
5. Orders and status flow
6. Attendance
7. Locations and WebSocket
8. Dashboard summary and invoice PDF
9. Frontend: auth and layout, then admin screens, then worker PWA
10. Seed script, README, deployment

## 14. Working agreement for the AI assistant

- Implement **one slice at a time** and stop for review after each.
- Before starting a slice, list the files you will create or change.
- Never change the schema without telling me first and creating an Alembic migration.
- Do not add features, libraries, or roles that are not in this spec.
- After each slice, run the tests and show me the results.
- Explain any non-obvious logic in short comments, since I must be able to explain this code myself.
- If the spec conflicts with itself or is missing something, ask instead of guessing.
