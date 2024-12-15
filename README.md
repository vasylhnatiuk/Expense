# Expense Tracker API

This is a Django-based API for tracking expenses, allowing users to categorize and view their expenses based on different filters such as date range and category summary. The project includes tests, migrations, and sample data for a complete setup.

## Features

- **User Authentication**: Allows users to log in and track their expenses.
- **Expense Management**: Add, edit, and delete expenses.
- **Category Summary**: Get total expenses per category for a specific month.
- **Date Range Filter**: Retrieve expenses within a specific date range.


## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api

2. **Set up the Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate

3. **Run Migrations**:

   ```bash
   python manage.py migrate

5. **Load Sample Data**

   ```bash
   python manage.py shell < load_test_data.py
6. **Run the tests**

   ```bash
   python manage.py test
   
