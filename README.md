# Library Database System

A desktop application for managing a library's database, built with Python, Tkinter, and Oracle SQL. It provides a graphical interface for setting up the database, running queries, and managing customer records.

## Features

- **Database setup from the GUI:** create, drop, and seed all tables with sample data
- **Relational schema with 7 tables:** `Book`, `Customer`, `Book_Loan`, `Member_Fine_Info`, `Fees_Info`, `Book_Fine_Info`, and `Publisher`, using composite primary keys and foreign key constraints to model books, loans, and fines
- **Customer record management:** search customers by email, then read, update, and delete records
- **Safe deletes:** deleting a customer removes their related loan and fine records across 5 tables inside a single transaction, and rolls back if any step fails, so no orphaned records are left behind
- **Parameterized queries** for user-supplied input
- **Custom SQL window:** run your own queries against the database and view the results

## Tech Stack

- Python
- Tkinter (GUI)
- Oracle SQL via the `oracledb` driver

## Getting Started

### Prerequisites

- Python 3.x
- An Oracle Database instance (such as Oracle Database XE) running locally at `localhost:1521/xe`
- The `oracledb` package:

```bash
pip install oracledb
```

### Run

```bash
python Library_Database_System.py
```

Enter your Oracle username and password in the connection window. Then use the buttons to create the tables, populate them with sample data, and explore.

> Note: the connection string is currently hardcoded to `localhost:1521/xe`.


## Known Limitations and Future Improvements

- Add a borrow/return workflow that updates `Book_Loan` with validation (for example, preventing a book from being checked out twice)
- Add a form to create new customers (currently the data comes from the seed script)
- Make the database connection configurable instead of hardcoded
- Add indexes and benchmark query performance on a larger dataset







