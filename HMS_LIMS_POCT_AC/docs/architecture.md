# System Architecture

## Purpose
Web-based POCT Laboratory Management System for management of operators, competency, devices, QC, maintenance, inventory, alerts, reports, and audit records.

## Architectural Layers
1. Presentation: HTML, CSS, Bootstrap, JavaScript, Django Templates.
2. Routing/Controller: Django URL configuration and views.
3. Business/Domain: Python methods and service classes for competency, QC, maintenance, and inventory rules.
4. Persistence: Django Models and ORM.
5. Database: PostgreSQL.
6. Database Administration: DBGate.
7. Development: Visual Studio Code.
8. Source Control: Git + GitHub.

## Scope Boundary
This is not an LIS. Excluded: patient registration, test ordering, specimen accessioning, patient results, billing, EHR interfaces, and clinical decision support.

© 2026 Angeline P. Cardoza. All rights reserved.