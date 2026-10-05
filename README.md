# Plastic Distribution Agency Management System

An MVP for managing a plastic-products distribution agency. The system is planned for an administrator who manages workers, stores, products, stock, and orders, and sales workers who use a mobile-friendly web app while visiting stores.

> **Status:** Project setup and backend data modeling are underway. The initial SQLAlchemy foundation is in place for core domain entities, including user-role and department enums, and the area model. See [SPEC.md](SPEC.md) for the full requirements and working agreement.

## Current backend model foundation

The backend now includes the initial data model layer for the agency domain:

- `USER_ROLE` enum with the current user groups: `admin`, `oworker` (office worker), and `worker`
- `DEPARTMENT` enum with: `operation`, `hr`, and `finance`
- `Area` model with a unique area name and creation/update timestamps

This foundation supports the next steps for authentication, user management, and the wider agency record model.

## Goals

- Give administrators a central view of sales, orders, attendance, stock, and workers.
- Let sales workers check in, share their location while working, manage assigned-area stores, and place orders from a phone browser.
- Keep stock accurate through recorded movements rather than direct quantity edits.
- Provide a simple PDF invoice for each order, without tax calculations in the MVP.

## Planned technology

| Area | Technology |
|---|---|
| Backend API | Python 3.11+, FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy 2.x, Alembic |
| Authentication | JWT access tokens and bcrypt password hashing |
| Live updates | FastAPI WebSockets |
| Frontend | React, Vite, Tailwind CSS, shadcn/ui |
| Maps | Leaflet and OpenStreetMap |
| Charts | Recharts |
| PDF invoices | WeasyPrint or ReportLab |
| Deployment | Docker; planned hosting on Render or Railway and Vercel |

## MVP features

### Administrator

- Manage workers, roles, departments, areas, stores, products, and stock movements.
- Review and approve stores added by workers.
- Manage order statuses and download invoices.
- Review attendance and see active workers on a live map, including route history.
- View dashboard summaries, recent sales, and low-stock products.

### Sales worker

- Use a mobile-first, installable web app (PWA).
- Check in and check out with GPS coordinates.
- Share location while checked in.
- View stores in their assigned area and add pending stores.
- Place orders for approved stores and view their own orders and invoices.

### User and department structure

The current backend model defines the primary access layers for agency staff:

- `admin`: full administrative access
- `oworker`: office-worker access
- `worker`: field sales worker access

Departments currently modeled in the backend are:

- `operation`
- `hr`
- `finance`

## Important business rules

- Access is role-based. The backend enforces permissions for every protected operation.
- Workers cannot see product purchase prices or other workers' orders.
- Stock is calculated from stock movements and cannot go below zero.
- The server calculates order totals and saves the unit price used when the order is placed.
- Stock is checked when an order is approved and deducted when it is dispatched.
- Money uses decimal database types, and timestamps are stored in UTC.

## Out of scope for the MVP

Payments, GST, credit limits, payroll, leave management, purchase orders, multiple warehouses, offline synchronization, a native mobile app, additional department definitions beyond the current agency model, notifications, and activity logs are reserved for a later phase.

## Development setup

`backend/requirements.txt` contains the backend runtime dependencies, and the root `requirements-dev.txt` adds test and seed-data dependencies. From the project root, create and activate a virtual environment in PowerShell, then install the development dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

The backend, database configuration, and Docker Compose setup have not been implemented yet. The frontend has a Vite entry screen. From the project root, start it with:

```powershell
cd frontend
npm install
npm run dev
```

The sign-in screen is only a deployable UI shell; authentication will work once the backend is implemented. The planned API entry point is `backend/app/main.py`.

WeasyPrint may require additional system libraries depending on the operating system. Its Linux/Docker package requirements are noted in `backend/requirements.txt`.

## Project structure

```text
README.md
SPEC.md
requirements-dev.txt
.github/
	workflows/
		deploy-frontend.yml
backend/
	requirements.txt
	app/
		__init__.py
		api/
			routes/
		core/
		models/
		schemas/
		services/
	alembic/
		versions/
	tests/
frontend/
	index.html
	package.json
	package-lock.json
	vite.config.js
	src/
		App.jsx
		main.jsx
		styles.css
		api/
		auth/
		components/
		pages/
			admin/
			worker/
```

This is the initial scaffold. The frontend currently contains a deployable sign-in shell; API modules, database models and migrations, tests, seed data, and the remaining frontend screens will be added in the build order below.

## GitHub Pages deployment

The workflow in `.github/workflows/deploy-frontend.yml` builds the frontend and deploys it to GitHub Pages whenever changes are pushed to `main` (or when manually triggered). In the GitHub repository, open **Settings > Pages** and set the build source to **GitHub Actions**. The project site will be available at `https://vaibhav-learn.github.io/Plastic-product-selling/` after the first successful workflow run.

The production build can be checked locally from `frontend/` with `npm run build`.

## Build order

The project will be delivered in vertical slices, with models, migrations, API behavior, tests, and UI completed for each slice before moving on:

1. Project setup, database connection, migrations, and Docker Compose.
2. Authentication, users, roles, and areas.
3. Stores.
4. Products and stock movements.
5. Orders, status transitions, and invoices.
6. Attendance.
7. Live locations and WebSockets.
8. Dashboard summaries.
9. Frontend authentication, administrator screens, and worker PWA.
10. Seed data, documentation, and deployment.

## Testing plan

Backend tests will use pytest. They will cover stock calculations, order approval and dispatch, valid status transitions, server-calculated totals, role-based data access, attendance rules, location permissions, and access revocation for deactivated users. Run the test suite with `pytest` once the tests and application are implemented.

## Location-sharing limitation

The worker PWA is expected to send location updates while the worker is checked in. Browsers do not reliably allow a PWA to track location while its screen is off or the app is suspended. Reliable background tracking would require a native mobile app and is outside the MVP.

## Security and configuration

Secrets will be supplied through environment variables. A committed `.env.example` will document required settings when backend configuration is implemented; do not commit real credentials or a local `.env` file. The API will restrict CORS to the frontend origin and will never return password hashes.