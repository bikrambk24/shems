# SHEMS — Smart Home Energy Management System

A Django web application that lets homeowners monitor and control their energy usage, administrators manage pricing and accounts, and technicians track faulty appliances. Built for the SWE7302 Advanced Software Development module.

## Features

- Real-time energy monitoring with auto-refreshing dashboard
- Appliance control (on/off, scheduling, fault reporting)
- Three pricing strategies: flat rate, time-of-use, and green energy discount
- Role-based access for homeowners, administrators, and technicians
- Threshold breach notifications via Observer pattern

## Design Patterns

- **Singleton** — `EnergyManagementSystem` ensures a single observer registry
- **Factory** — `ApplianceFactory` creates configured appliances by type
- **Observer** — threshold breaches notify dashboard, audit log, and technicians
- **Strategy** — pricing algorithms swap at runtime without code changes

## Tech Stack

- Python 3.11+
- Django 4.2
- SQLite (default)
- Bootstrap 5 (frontend)

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/bikrambk24/shems.git
cd shems

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Homeowner | `john` | `john123` |
| Administrator | `admin` | `admin123` |
| Technician | `tech1` | `tech123` |

## Running Tests

```bash
python manage.py test
```

Fifteen tests cover all four design patterns and role-based access control.