# Expenses Tracker

A Django web app for tracking expenses and organizing them by category.

## Setup

**Requires:** Python 3.14 and Git.
You must accept the GitHub invitation to this repo before cloning.

1. Clone the repo:
   ```bash
   git clone https://github.com/Orion379/expenses-tracker.git
   cd expenses-tracker
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```
   On Windows PowerShell, if activation fails with a "running scripts is disabled" error, run this once and try again:
   ```bash
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your local database:
   ```bash
   python manage.py migrate
   ```
   Each person has their own local database (`db.sqlite3` is not in the repo), so your data will not match your teammates' data.
5. Start the server:
   ```bash
   python manage.py runserver
   ```
   Then open http://127.0.0.1:8000/ in your browser.

## Team workflow

- Never commit directly to `main`.
- Create a branch for each task (`feature/...` for new things, `fix/...` for bugs), push it, and open a pull request.
- The lead reviews and merges the pull request.
- Before starting a new branch, run `git checkout main` and `git pull`.
- After pulling, run `python manage.py migrate` in case teammates changed the models.
- If you install a new package, run `pip freeze > requirements.txt` and commit the updated file.
