# Qatar Foundation — Admin Portal

A full-stack admin portal for managing Qatar Foundation opportunities. Admins can sign up, log in, and fully manage opportunities through a clean single-page dashboard.

## Live Demo

[https://qatar-foundation.onrender.com](https://qatar-foundation.onrender.com)

> Hosted on Render free tier — first load may take 30–90 seconds to wake up.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Bcrypt
- **Database:** SQLite
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Deployment:** Render (Gunicorn)

---

## Features

### Authentication

- **Sign Up** — Admins can create an account with full name, email, and password. All fields are validated — email format, minimum 8-character password, and password confirmation match. Duplicate emails are rejected with a clear error.

- **Login** — Secure login with email and password. Includes a Remember Me option that keeps the session active for 30 days. Without it, the session ends when the browser closes. Wrong credentials always return a generic error to prevent revealing which field is incorrect.

- **Forgot Password** — Admins can request a password reset by entering their email. A time-limited reset token is generated and logged internally. The reset link expires after 1 hour. The same success message is always shown regardless of whether the email exists, protecting user privacy.

- **Logout** — Clears the session and returns the admin to the login page.

---

### Opportunity Management

All opportunities are tied to the logged-in admin account and stored in the database. Admins only ever see and manage their own opportunities — never those of other accounts.

- **View Opportunities** — The Opportunity Management tab loads all opportunities created by the logged-in admin directly from the database. Each card displays the opportunity name, category, duration, start date, and a short description. If no opportunities exist yet, a friendly empty state message is shown instead of a blank page.

- **Add Opportunity** — A modal form lets admins create a new opportunity with the following fields: Opportunity Name, Duration, Start Date, Description, Skills to Gain (comma separated), Category, Future Opportunities, and an optional Maximum Applicants field. Category options include Technology, Business, Design, Marketing, Data Science, and Other. All required fields are validated before submission. The new opportunity card appears instantly on the dashboard without a page refresh.

- **View Details** — Each opportunity card has a View Details button that opens a modal showing all saved fields including skills, category, future opportunities, and maximum applicants if set.

- **Edit Opportunity** — Each card has an Edit button that opens the same form modal pre-filled with the existing data. Any field can be updated. On save, the database is updated and the card reflects the changes immediately without a page refresh.

- **Delete Opportunity** — Each card has a Delete button. Clicking it shows a confirmation prompt to prevent accidental deletions. On confirmation, the opportunity is permanently removed from the database and disappears from the dashboard instantly. Only the admin who created the opportunity can delete it.

- **Data Persistence** — All opportunities are stored in the database and persist across sessions. Logging out and back in always restores the full list of previously created opportunities.

---

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

---

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

---

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

---

## API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/signup` | Create admin account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/session` | Check current session |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with token |

### Opportunities

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/opportunities` | List all opportunities for logged-in admin |
| POST | `/api/opportunities` | Create a new opportunity |
| GET | `/api/opportunities/<id>` | Get single opportunity details |
| PUT | `/api/opportunities/<id>` | Update an opportunity |
| DELETE | `/api/opportunities/<id>` | Delete an opportunity |
