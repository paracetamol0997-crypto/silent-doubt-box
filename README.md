# Silent Classroom Doubt Box 🎓

> **"Ask without fear. Learn without hesitation."**
>
> An anonymous-feeling private college web portal where students can comfortably ask classroom doubts without peer judgment, and teachers can review, filter, and clarify them with strict privacy separation.

---

## ⚡ Instant One-Click Run (For Friends & Evaluators)

If you extracted this project from a ZIP file on Windows:

1. **Double-click `RUN_PROJECT.bat`** (or right-click `RUN_PROJECT.ps1` -> *Run with PowerShell*).
2. The script will automatically:
   - Check if Python is installed.
   - Install dependencies (`pip install -r requirements.txt`).
   - Run database migrations and seed sample students, teachers, subjects, and doubts.
   - Automatically open **`http://127.0.0.1:8000/`** in your default web browser!
   - Display all demo credentials directly in the terminal console.

*(On macOS/Linux, simply run `./run.sh` in the terminal).*

---

## 1. Problem Statement

In traditional college lecture environments, many students feel shy, nervous, or hesitant to raise their hands and ask doubts in front of the entire class. The fear of being judged by peers or feeling embarrassed often leads students to stay silent and fall behind in their coursework.

Standard public discussion forums, group chats, or classroom feeds do not solve this problem because any question posted is still visible to all classmates, recreating the exact same social pressure and anxiety.

---

## 2. Proposed Solution

**Silent Classroom Doubt Box** provides a dedicated, privacy-first bridge between students and faculty:
- **Private Student Submission:** A student logs in, selects a course subject, and submits their doubt privately.
- **Strict Peer Isolation:** Students can **never** see questions asked by other students. A student only sees their own questions and the teacher's clarifications.
- **Full Faculty Control:** Teachers log in through a separate dashboard where they can see all student questions, filter by subject or status, search by student name or register number, and provide direct, helpful explanations.
- **Immediate Feedback Loop:** Once answered, the doubt status changes to **Clarified**, and the teacher's explanation appears instantly in that specific student's private "My Doubts" section.

---

## 3. Core Features

### 🎒 Student Portal
- **Secure Authentication:** Log in using College Register Number, Student Name, and Password.
- **Distraction-Free Dashboard:** Clean dashboard showing total doubts submitted, pending queries, and clarified answers.
- **Private Doubt Submission:**
  - Dynamic subject selection from database.
  - Large question textarea with real-time character counter and helpful writing tips.
  - Automatic validation preventing empty or trivial submissions.
- **"My Doubts" History:**
  - View only doubts submitted by the currently logged-in student.
  - Filter own doubts by Subject and Status (Pending / Clarified).
  - Clear visual badges and faculty answer display with timestamps and faculty name.
- **Zero Peer Visibility:** No student can see, search, or access another student's doubts.

### 👨‍🏫 Teacher Portal
- **Dedicated Faculty Authentication:** Log in using Teacher ID and Password.
- **Comprehensive Overview Dashboard:**
  - Real-time statistics: Total Enrolled Students, Total Doubts, Pending Clarifications, Clarified Doubts.
  - Priority queue of pending doubts waiting for review.
  - Subject-wise inquiry distribution table.
- **All Student Doubts Feed:**
  - View doubts across all enrolled students and courses.
  - Displays Student Name, Register Number, Subject, Question, Submission Date, and Status.
- **Multi-Filter & Search System:**
  - Filter by Subject (Data Structures, DBMS, Networks, OS, ML, etc.).
  - Filter by Status (Pending Only, Clarified Only, All).
  - Search by Student Name or College Register Number.
  - Filters work simultaneously.
- **Doubt Clarification Engine:**
  - Open any doubt to view the student's question and full context.
  - Write detailed explanations and submit.
  - Automatically updates status to **Clarified**, logs answering faculty and timestamp, and makes the answer immediately visible to the student.
  - Ability to update or refine clarifications at any time.
- **Enrolled Students Directory:**
  - View all registered students with doubt activity statistics.

---

## 4. Privacy & Security Rules

The application enforces privacy at the backend and database levels, not just by hiding UI links:

1. **Role-Based Access Control (RBAC):**
   - Students cannot access `/teacher/*` routes. Attempts return a strict `403 Forbidden` response.
   - Teachers cannot access student-specific question forms.
2. **Strict Horizontal Authorization (Object-Level Ownership):**
   - Accessing `/student/doubt/<id>/` verifies that `doubt.student == request.user`.
   - If Student A attempts URL manipulation to access Student B's doubt ID, the backend immediately rejects the request with a `403 Forbidden` error.
3. **Database Query Isolation:**
   - The student "My Doubts" view queries strictly `Doubt.objects.filter(student=request.user)`.
   - Cross-student data leakage is impossible.
4. **Secure Password Hashing:**
   - All passwords are encrypted and hashed using Django's PBKDF2 with SHA-256 (no plain-text passwords).
5. **CSRF & Session Protection:**
   - All forms are protected against Cross-Site Request Forgery via Django CSRF tokens.

---

## 5. Technology Stack

- **Backend:** Python 3.12, Django 5.1.15
- **Frontend:** Semantic HTML5, CSS3 (Modern College Portal Design System with CSS variables and responsive flex/grid layouts), Vanilla JavaScript (no heavy node dependencies)
- **Database:** SQLite (default for development; clean Django ORM ready for PostgreSQL deployment)
- **Architecture:** Model-View-Template (MVT) with custom authentication, authorization decorators, and forms

---

## 6. Database Design

```
+-----------------------------------------------------------------+
|                              User                               |
+-----------------------------------------------------------------+
| id (PK)                                                         |
| username (varchar)                                              |
| role ('STUDENT' | 'TEACHER')                                    |
| name (varchar)                                                  |
| register_number (varchar, unique, for students e.g. 23CSE101)   |
| teacher_id (varchar, unique, for teachers e.g. T101)            |
| password (PBKDF2 hash)                                          |
| email (varchar)                                                 |
| created_at (datetime)                                           |
+-----------------------------------------------------------------+
               | 1                                     | 1
               | student                               | answered_by
               | (role=STUDENT)                        | (role=TEACHER)
               v M                                     v M
+-----------------------------------------------------------------+        +---------------------+
|                             Doubt                               |        |       Subject       |
+-----------------------------------------------------------------+        +---------------------+
| id (PK)                                                         |        | id (PK)             |
| student_id (FK -> User)                                         | >----+ | name (varchar)      |
| subject_id (FK -> Subject)                                      |      | | code (varchar)      |
| question (text)                                                 |      +-| description (text)  |
| status ('PENDING' | 'CLARIFIED')                                |        | created_at (dt)     |
| teacher_answer (text, nullable)                                 |        +---------------------+
| answered_by_id (FK -> User, nullable)                           |
| created_at (datetime)                                           |
| answered_at (datetime, nullable)                                |
+-----------------------------------------------------------------+
```

---

## 7. Demo Credentials for Evaluation

The database is pre-seeded with realistic students, teachers, subjects, and doubts:

### Student Accounts
| Register Number | Student Name | Password | Status |
| :--- | :--- | :--- | :--- |
| `23CSE101` | Rahul Kumar | `rahul@123` | Has 1 Pending & 1 Clarified doubt |
| `23CSE102` | Priya Sharma | `priya@123` | Has 1 Pending & 1 Clarified doubt |
| `23CSE103` | Arjun Patel | `arjun@123` | Has 1 Pending doubt |
| `23CSE104` | Sneha Reddy | `sneha@123` | Has 1 Pending doubt |

### Teacher Accounts
| Teacher ID | Teacher Name | Role / Department | Password |
| :--- | :--- | :--- | :--- |
| `T101` | Dr. Ramesh Sharma | Senior Professor, Computer Science | `teacher@123` |
| `T102` | Prof. Anjali Verma | Associate Professor, Information Tech | `teacher@123` |

*(Tip: Both login pages feature one-click autofill buttons for immediate testing!)*

---

## 8. Installation & Setup Instructions

### Prerequisites
- Python 3.10+ installed
- pip installed

### 1. Clone / Open the Project Directory
```powershell
cd "c:\Users\Princ\Documents\doubt box"
```

### 2. Install Dependencies (if not already installed)
```powershell
pip install django
```

### 3. Run Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Demo Data
Populates subjects, demo students, teachers, and sample doubts:
```powershell
python manage.py seed_data
```

### 5. Start the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
**`http://127.0.0.1:8000/`**

---

## 9. Running Automated Tests

Run the complete test suite verifying all 18 security, isolation, and functional test cases:
```powershell
python manage.py test core
```

---

## 10. End-to-End Walkthrough Demonstration

### Scenario: Private Doubt Submission to Teacher Clarification

1. **Student Login:**
   - Navigate to `http://127.0.0.1:8000/login/student/`.
   - Click the **Rahul Kumar** quick autofill button (or enter `23CSE101`, `Rahul Kumar`, `rahul@123`).
   - Click **Login as Student**.

2. **Submit a Doubt:**
   - Click **Ask a Doubt** in the navigation bar.
   - Select Subject: `Data Structures`.
   - Enter Question: *"Sir, I am not understanding how recursion works. Can you please explain?"*
   - Click **Submit Doubt Privately**.
   - Notice the success banner: *"Your doubt has been submitted privately. Your teacher will review it soon."*
   - The doubt appears in Rahul's **My Doubts** list with status **Pending**.

3. **Verify Privacy Isolation (Student B Check):**
   - Click **Logout**.
   - Log in as **Priya Sharma** (`23CSE102`, `Priya Sharma`, `priya@123`).
   - Open **My Doubts**.
   - Confirm that Priya **cannot** see Rahul's question. She only sees her own doubts.
   - If Priya attempts to access `/student/doubt/<rahul_doubt_id>/`, she is blocked with **403 Forbidden**.

4. **Teacher Login & Clarification:**
   - Log out and go to `http://127.0.0.1:8000/login/teacher/`.
   - Use **Dr. Ramesh Sharma** (`T101`, `teacher@123`).
   - On the Teacher Dashboard, Rahul's doubt is visible in the priority pending queue.
   - Navigate to **All Student Doubts**.
   - Filter by `Data Structures` or search `Rahul Kumar`.
   - Click **Answer Doubt**.
   - Write the clarification: *"Recursion is a technique where a function calls itself to solve smaller subproblems, until it hits the base condition..."*
   - Click **Submit Answer**. Status updates to **Clarified**.

5. **Student Reviews Answer:**
   - Log out and log back in as **Rahul Kumar**.
   - Go to **My Doubts**.
   - Rahul now sees Dr. Ramesh Sharma's detailed clarification with the timestamp and status badge **Clarified**.

---

## 11. Project Directory Structure

```
doubt box/
├── manage.py
├── README.md
├── db.sqlite3
├── doubtbox_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Configuration, AUTH_USER_MODEL, static & template paths
│   ├── urls.py               # Main URL dispatcher with custom 403 & 404 handlers
│   └── wsgi.py
├── core/
│   ├── admin.py              # Django Admin registrations
│   ├── apps.py
│   ├── decorators.py         # @student_required and @teacher_required RBAC guards
│   ├── forms.py              # Student/Teacher login forms, Doubt & Answer forms with validation
│   ├── models.py             # User (AbstractUser), Subject, Doubt models
│   ├── tests.py              # 18 automated tests verifying all functional & privacy requirements
│   ├── urls.py               # Application routing for student & teacher portals
│   ├── views.py              # Controllers enforcing ownership checks & role permissions
│   └── management/
│       └── commands/
│           └── seed_data.py  # Demo seed script for instant evaluation
├── templates/
│   ├── base.html             # Common navbar, user role badge, flash messages, footer
│   ├── landing.html          # Public home page with 5-step workflow & credentials
│   ├── auth/
│   │   ├── student_login.html# Student login form with quick autofill
│   │   └── teacher_login.html# Teacher login form with quick autofill
│   ├── student/
│   │   ├── dashboard.html    # Clean student overview
│   │   ├── ask_doubt.html    # Private doubt submission form
│   │   ├── my_doubts.html    # Private doubt history (isolated to current student)
│   │   └── doubt_detail.html # Single doubt view with ownership check
│   ├── teacher/
│   │   ├── dashboard.html    # Metrics, pending queue, subject breakdown
│   │   ├── all_doubts.html   # Master feed with combined search & filters
│   │   ├── answer_doubt.html # Teacher answer input form
│   │   └── students_list.html# Enrolled student directory
│   └── errors/
│       ├── 403.html          # Privacy violation & access denied error template
│       └── 404.html          # Page not found error template
└── static/
    ├── css/
    │   └── style.css         # Modern college portal design system
    └── js/
        └── main.js           # Client scripts (mobile toggle, alerts, quick autofill)
```

---

## 12. Free Cloud Hosting Guide (Render.com / Railway)

This repository is pre-configured with `render.yaml`, `Procfile`, and `build.sh` for instant cloud deployment.

### Option A: Deploy on Render.com (Free)
1. Go to [Render.com](https://render.com/) and sign in with GitHub.
2. Click **New +** $\rightarrow$ **Web Service**.
3. Select your repository: **`paracetamol0997-crypto/silent-doubt-box`**.
4. Render will auto-detect the configuration, or set:
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn doubtbox_project.wsgi:application`
5. Click **Deploy Web Service**!
6. Once deployed, Render will provide a live URL like `https://silent-doubt-box.onrender.com`.

### Option B: Deploy on Railway (Free)
1. Go to [Railway.app](https://railway.app/) and sign in with GitHub.
2. Click **New Project** $\rightarrow$ **Deploy from GitHub repo**.
3. Select **`paracetamol0997-crypto/silent-doubt-box`**.
4. Railway will automatically build using the `Procfile` and start your app!

### Option C: Deploy on Vercel
1. Go to [Vercel.com](https://vercel.com/) and sign in with GitHub.
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import **`paracetamol0997-crypto/silent-doubt-box`**.
4. Vercel automatically detects `vercel.json` and configures the Python serverless function.
5. Click **Deploy**!
> **Note on Vercel & Databases:** Vercel functions are serverless and ephemeral. For full persistent data across serverless instances, connect a free PostgreSQL database (e.g. from [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/)) by adding a `DATABASE_URL` environment variable in your Vercel Project Settings. If no `DATABASE_URL` is provided, the app will run with the bundled demo SQLite database in `/tmp`.

---

## 13. License
Created for College Academic Learning and Privacy Support. All rights reserved.
