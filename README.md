# Expense Tracker

A Django web app for tracking expenses and organizing them by category.

## Setup

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd expense-tracker
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Team workflow

- Never commit directly to `main`.
- Create a branch for each task, push it, and open a pull request.
- Another teammate or the lead reviews before merging.
