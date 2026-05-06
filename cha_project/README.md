# Coruscant Health Administration

Coruscant Health Administration is a Django medical management system built for four main flows:

- patient registration and health data upload
- doctor reports and medical orders
- department order processing
- emergency patient intake

## Tech stack

- Python
- Django
- SQLite locally
- PostgreSQL on Render through `DATABASE_URL`

## Main features

- role-based login for patient, doctor, administrator, emergency, and department users
- patient health record tracking
- doctor reports and service orders
- encrypted document upload
- emergency patient registration

## Local setup

1. Create a virtual environment.
2. Install packages:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

5. Run tests:

```bash
python manage.py test
```

## Render deployment

This project is prepared for Render with:

- `render.yaml`
- `build.sh`
- `Procfile`
- `DATABASE_URL` support
- `/health/` health check

### Recommended Render steps

1. Push this project to GitHub.
2. In Render, create a new Blueprint and connect the repo.
3. Render will read `render.yaml` and create:
   - one web service
   - one free PostgreSQL database
4. After the first deploy finishes, open the generated `onrender.com` URL.

## Environment variables

Use these values in production:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `ENCRYPTION_KEY`

## Project URL

The current project URL should be written to:

- `my_coruscant_health_administration_url.txt`
