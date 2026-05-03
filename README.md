# Qatar Foundation — Admin Portal

A full-stack web application for managing Qatar Foundation opportunities. Built with Flask, SQLite, and a single-page frontend as part of the CertifyMe Intern Assessment.

## Live Demo

[https://qatar-foundation.onrender.com](https://qatar-foundation.onrender.com)

> Note: Hosted on Render free tier — first load may take 30–90 seconds to wake up.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Bcrypt
- **Database:** SQLite
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Deployment:** Render (Gunicorn)

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
| GET | `/api/auth/session` | Check session |
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

---

## User Stories Implemented

### Task 1 — Login & Signup

**US-1.1 — Admin Sign Up**
- Form fields: full name, email, password, confirm password
- All fields required. Email must be valid. Password minimum 8 characters
- Password and confirm password must match
- Duplicate email shows error. On success, redirects to login page

**US-1.2 — Admin Login**
- Form fields: email, password, Remember Me checkbox
- Wrong credentials show generic error — does not reveal which field is wrong
- On success, redirects to dashboard and loads all opportunities for that admin
- Remember Me keeps session active for 30 days. Without it, session ends on browser close

**US-1.3 — Forgot Password**
- Always shows the same success message regardless of whether email exists (privacy protection)
- If email is registered, generates a reset token and logs the reset link internally
- Reset link expires after 1 hour. Expired links show a clear error message

---

### Task 2 — Opportunity Management

**US-2.1 — View All Opportunities**
- Opens on the Opportunity Management tab and loads all opportunities from the database
- Each card shows: opportunity name, category, duration, start date, and description
- All data comes from the database — nothing hardcoded
- Empty state message shown when no opportunities exist yet

**US-2.2 — Add a New Opportunity**
- "Add New Opportunity" button opens a modal form
- Required fields: Opportunity Name, Duration, Start Date, Description, Skills to Gain (comma separated), Category, Future Opportunities
- Optional field: Maximum Applicants
- Category options: Technology, Business, Design, Marketing, Data Science, Other
- All required fields validated on submit. New card appears immediately without page refresh

**US-2.3 — Opportunities Persist After Login**
- All opportunities are stored in the database and fetched on every login
- Logging out and back in shows all previously created opportunities
- Not stored in browser memory or local storage
- Admins cannot see opportunities created by other admin accounts

**US-2.4 — View Opportunity Details**
- Each card has a View Details button that opens a details modal
- Modal shows all fields: name, duration, start date, description, skills, category, future opportunities, and max applicants if provided
- Close button dismisses the modal

**US-2.5 — Edit an Opportunity**
- Each card has an Edit button
- Opens the same form modal pre-filled with existing data
- All required field validations apply
- On success, database is updated and card reflects changes immediately without page refresh
- Only updates that specific opportunity

**US-2.6 — Delete an Opportunity**
- Each card has a Delete button
- Clicking Delete shows a confirmation prompt before proceeding
- On confirm, opportunity is permanently deleted from database and removed from the card view immediately
- On cancel, nothing is deleted
- Only the admin who created the opportunity can delete it

---

## User Story Summary

| Story ID | Task | Title | Timeline |
|---|---|---|---|
| US-1.1 | Task 1 | Admin Sign Up | Day 1 |
| US-1.2 | Task 1 | Admin Login | Day 1 |
| US-1.3 | Task 1 | Forgot Password | Day 1 |
| US-2.1 | Task 2 | View All Opportunities | Day 2 |
| US-2.2 | Task 2 | Add a New Opportunity | Day 2 |
| US-2.3 | Task 2 | Opportunities Persist After Login | Day 2 |
| US-2.4 | Task 2 | View Opportunity Details | Day 2 |
| US-2.5 | Task 2 | Edit an Opportunity | Day 2 |
| US-2.6 | Task 2 | Delete an Opportunity | Day 2 |
