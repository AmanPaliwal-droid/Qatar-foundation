# Qatar Foundation Admin Portal

A full-stack web application for managing Qatar Foundation opportunities. Built with Flask, SQLite, and a single-page frontend.

## Features

- Admin authentication (signup, login, logout)
- Password reset via token
- Create, view, edit, and delete opportunities
- Session management with remember me
- Responsive admin dashboard UI

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Bcrypt
- **Database:** SQLite
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Deployment:** Render (Gunicorn)

## Project Structure

```
Qatar-foundation-main/
├── Backend/
│   ├── app.py               # Flask app factory
│   ├── extensions.py        # DB and Bcrypt instances
│   ├── models.py            # Admin, Opportunity, PasswordResetToken models
│   └── routes/
│       ├── auth.py          # Signup, login, logout, password reset
│       └── opportunities.py # CRUD endpoints for opportunities
├── templates/
│   └── admin.html           # Single-page frontend
├── static/
│   ├── admin.css            # Styles
│   └── admin.js             # Frontend logic
├── requirements.txt
├── render.yaml              # Render deployment config
└── .gitignore
```

## Local Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/Qatar-foundation.git
   cd Qatar-foundation/Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Deployment (Render)

| Setting | Value |
|---|---|
| Root Directory | `Backend` |
| Build Command | `pip install -r ../requirements.txt` |
| Start Command | `gunicorn "app:create_app()"` |
| Runtime | Python 3 |

**Environment Variables:**

| Key | Value |
|---|---|
| `SECRET_KEY` | Any long random string |

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/signup` | Create admin account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/session` | Check session |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with token |

### Opportunities
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/opportunities` | List all opportunities |
| POST | `/api/opportunities` | Create opportunity |
| GET | `/api/opportunities/<id>` | Get single opportunity |
| PUT | `/api/opportunities/<id>` | Update opportunity |
| DELETE | `/api/opportunities/<id>` | Delete opportunity |

## Live Demo

[https://qatar-foundation.onrender.com](https://qatar-foundation.onrender.com)

> Note: Hosted on Render free tier — first load may take 30–90 seconds to wake up.
