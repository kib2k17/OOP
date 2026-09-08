poct_lms_capstone - Main Module
© 2026 Angeline P. Cardoza. all rights reserved.
Email: cnt.angelinecardoza@gmail.com
ID number: 201212198



# POCT Laboratory Management System (Capstone)

Web-based Computer Science capstone implemented with **Python, Django, PostregeSQL, Bootstrap, JavaScript, Git/GitHub, Visual Studio Code, and DBGate**.

## Scope
This is a **Laboratory Management System**, not a Laboratory Information System (LIS). It manages POCT operations such as operators, competencies, devices, quality control, maintenance, inventory, alerts, reposrts, users/ roles, and audit trails. It intenionally excludes patient registration, physician orders, patient-result reporting, billing, EHR interfaces, and specimen accessioning.

## Technology Stack
- Python 3.12+
- Django 5.x
- PostgreSQL
- Django ORM
- Bootstrap 5
- HTML5/CSS3/JavaScript
- Chart.js
- DBGate for database administration
- Visual Studio Code
- Git and GitHub
- Django test framework / pytest compatible

## Quick Start
1. Create and Active a virtual environment.
2. Install dependencies: 'pip install -r requirements.txt'
3. Copy '.env.example' to '.env' and update PostgreSQL settings.
4. Create the database in PostgreSQL.
5. Run 'python manage.py makemigrations' then 'python manage.py migrate' .
6. Run 'python manage.py createsuperuser' .
7. Optional sample data: 'python manage.py seed_demo' .
8. Start server: 'python manage.py runserver' .
9. Open 'http://127.0.0.1:8000/' .

## DBGate
Connect DBGate to the same PostgreSQL server using values in '.env' . DBGate is used for viewing tables, relationships, indexes, constraints, and running administrative SQL. Normal application data access should remain through Django ORM.

## Main Modules
- Authentication / role-based access
- Dashboard
- Operators and departments
- Test methods
- POCT devices
- Competency management
- Quality control and corrective action
- Maintainance
- Inventory/ lot / expiration tracking
- Alerts
- Reports
- Audit trail

## Architecture
Browser -> Django Templates/UI -> URL Router -> Views -> Services/Domain Logic -> Django Models/ORM -> PostgreSQL. DBGate provides database administration and inspection. VS Code is the development environment; Git and GitHub provide source control.

## Important Academic Note
Use synthetic/ demo data only. Do not use real patient or employee information in a student capstone repository.