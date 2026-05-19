# 🛡️ ServiceNow CSA Exam Preparation Platform

An advanced, high-fidelity, and feature-rich Django web application designed for students and administrators preparing for the **ServiceNow Certified System Administrator (CSA)** exam. 

This platform features a professional, high-density, "single-screen" dashboard, adaptive mock tests, study plans, practice quizzes, and an ultra-secure, exclusive administration panel.

---

## 🌟 Key Features

### 💻 Student Portal & Study Engine
*   **🎯 Adaptive Mock Tests**: A custom single-question-per-slide test engine designed to eliminate global scrolling, offering an authentic exam environment.
*   **📖 Topic-Wise Practice Quizzes**: Segmented practice quizzes mapping directly to official ServiceNow CSA syllabus areas.
*   **📊 Performance Analytics**: Instant feedback, scoring, and correction logs to review wrong answers.
*   **📚 Resource Hub & Syllabus Tracker**: Track your study progress through different core modules of the ServiceNow system.

### 🛡️ WhiteDevil Security & Admin Control Panel
*   **🔑 Multi-Factor Admin Approvals**: Safe admin dashboard requiring mandatory OTP/approval for key operations.
*   **🕵️ Active Session Monitor**: Real-time session auditing with remote device termination to stop compromised logins.
*   **📜 Comprehensive Audit Logging**: Complete historical tracking of user logins, session activity, and score logs.
*   **🛠️ Live Question Manager**: A dedicated interface for admins to create, update, and manage the CSA question bank dynamically.

---

## 🚀 Quick Start

### 1. Prerequisites
*   Python 3.10+
*   Pip (Python Package Installer)

### 2. Setup the Environment
Clone this repository and navigate to the project directory:
```bash
cd ServiceNow
```

Install django:
```bash
pip install django
```

### 3. Initialize & Populate the Database (Backend Data)
This project comes with all backend database records pre-packaged in a portable JSON format. Recreate the complete test bank, user accounts, and syllabus instantly:

```bash
# 1. Run migrations to build database tables
python manage.py migrate

# 2. Load the packed backend data (questions, practice exams, users, history)
python manage.py loaddata backend_data.json
```

*(Optional) Seed fresh data using the custom seeder scripts:*
```bash
python seed_questions.py
python seed_syllabus.py
python seed_resources.py
```

### 4. Start the Application
Run the Django local development server:
```bash
python manage.py run server
# Or: python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your web browser to access the application!

---

## 📁 Directory Structure
```text
ServiceNow/
├── servicenow_csa/       # Core project settings and URL configuration
├── users/                # User authentication, profiles, and administration
├── mocktest/             # Mock test logic, slides, and state engines
├── practice/             # Practice quizzes and topic-wise systems
├── syllabus/             # Syllabus tracker and modular course content
├── question_manager/     # Admin-only dashboard for managing the exam bank
├── dashboard/            # Core user portal and UI dashboard
├── templates/            # Global HTML templates
├── static/               # CSS styling, Javascript components, and assets
├── backend_data.json     # Complete backend database dump (questions, users, etc.)
└── manage.py             # Django project manager CLI
```

---

## 🎨 Premium UI/UX Design System
The frontend is built using a custom vanilla CSS design system incorporating:
*   **Sleek Dark Mode & HSL Tailored Colors**: High contrast, professional dark-blue aesthetic that reduces eye strain during long study sessions.
*   **Micro-Animations & Transitions**: Fluid animations for test navigation, hover effects, and modal popups.
*   **Ultra-Responsive Glassmorphism**: Cards and controls that adapt beautifully to desktops, tablets, and mobile devices.

---
*Created and maintained by manufacturing experts and ServiceNow professionals.*
