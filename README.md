# CampusFlow OCMS Backend (PDF Manual Aligned)

This project is aligned to the OCMS blueprint in your PDF:
- Required apps: `accounts`, `courses`, `enrollments`, `reviews`, `dashboard`
- Auth: JWT (access + refresh + blacklist)
- Database: PostgreSQL
- Caching: Redis (fallback to local memory cache only if Redis client is unavailable)
- API features: pagination, filtering, searching, ordering
- Frontend: minimal HTML/CSS/JS integration at `/`

## Project Structure
- `accounts`: custom user model (email login), roles (`STUDENT`, `INSTRUCTOR`, `ADMIN`)
- `courses`: category, course, module, lecture
- `enrollments`: enrollment, lecture progress
- `reviews`: course rating/feedback
- `dashboard`: admin analytics (cached)

## Setup
1. Create and activate venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Configure PostgreSQL and Redis env vars (optional; defaults provided)
```bash
export POSTGRES_DB=ocms_db
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export REDIS_URL=redis://127.0.0.1:6379/1
```
4. Run migrations and create admin
```bash
python manage.py migrate
python manage.py createsuperuser
```
5. Start server
```bash
python manage.py runserver
```

## Key Endpoints
- JWT: `/api/token/`, `/api/token/refresh/`
- Accounts: `/api/accounts/register/`, `/api/accounts/me/`
- Courses: `/api/courses/categories/`, `/api/courses/courses/`, `/api/courses/modules/`, `/api/courses/lectures/`, `/api/courses/courses/top/`
- Enrollments: `/api/enrollments/enrollments/`, `/api/enrollments/lecture-progress/`
- Reviews: `/api/reviews/`
- Dashboard stats (admin role): `/api/dashboard/stats/`

## Test
```bash
python manage.py test -v 2
```
