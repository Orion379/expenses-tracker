# ExpenseTracker Frontend

Responsive multi-page HTML/CSS/JavaScript frontend based on the supplied ExpenseTracker ERD.

## Pages
login.html, register.html, dashboard.html, profile.html, accounts.html, income.html, expenses.html, categories.html, budgets.html, recurring.html, wishlist.html, notifications.html, logout.html.

## Run
Open `login.html` in a browser, or serve this directory with a local static server:
`python -m http.server 8000`
Then visit `http://localhost:8000/login.html`.

## Demo behavior
- Records and demo user profile are stored in browser LocalStorage.
- Add, edit, delete and search are implemented for account, income, expense, category, budget, recurring-expense and wishlist records.
- Dashboard totals, recent transactions and budget usage use locally stored demo data.
- Three accent themes are available under Profile.
- Login accepts any non-empty credentials for demonstration.

## Important backend integration notes
This is a frontend prototype, not production authentication or a secure financial application. Do not store real passwords or financial data in LocalStorage. Connect forms to Django views/API endpoints, use Django's password hashing and session authentication, enforce per-user ownership on the server, add CSRF protection, and validate all input server-side. The ERD does not define profile fields beyond the User entity's username, email and password_hash; profile name/currency fields in this prototype are frontend convenience fields.
