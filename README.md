****Health Records Management System (SQLite + Jupyter Notebook)****

A simple but well structured health data management system built using SQLite inside a Jupyter Notebook.
This project demonstrates how to design, create, and manage a database using SQL while performing full CRUD operations, joins, aggregations, and common analytical queries used in healthcare data systems.

Project Overview
This project simulates a small health database that stores information about patients, doctors, and appointments.
It is built for beginners learning:

SQL basics
SQLite database design
CRUD operations
Joins & relational mapping
Data analysis using SQL
Writing documentation inside Jupyter Notebook

The project uses the %sql magic command inside Jupyter Notebook to execute SQL queries on a SQLite database.

Database Structure
The system contains three main tables:
1. Patients Table
   Stores patient information.
Fields:
   patient_id (Primary Key)
   first_name
   last_name
   age
   gender
   disease
   phone (Added later)

2. Doctors Table
   Stores doctor information.
Fields:
   doctor_id (Primary Key)
   name
   speciality

3. Appointments Table
   Links patients and doctors.
Fields:
   appointment_id (Primary Key)
   patient_id (Foreign Key → Patients)
   doctor_id (Foreign Key → Doctors)
   appointment_date
   status

Features / CRUD Operations
   Create
   Insert new patients
   Add new doctors
   Create appointment entries

Read
   Fetch all patients, doctors, appointments
   Filter by gender, disease, or status
   Join tables to create combined reports
   Generate analytics (count, group by, etc.)

Update
   Modify patient diseases or phone numbers
   Update appointment status
   Edit doctor specialities

Delete
   Remove patients
   Delete appointments
   Clean tables if needed

Analytical Queries Included
   Count patients by disease
   Count male vs. female patients
   List pending appointments
   Complete appointment summary (patients + doctors)
   Filter by specific conditions (disease, age, status)

Tools & Technologies Used
Tool	                      Purpose
Jupyter Notebook	          Documentation & execution environment
SQLite	                    Lightweight relational database
SQL Magic (%sql)	          Running SQL inside notebook
Python	                    Used to load and manage SQLite engine

Project Files
File	                      Description
health.db	                  SQLite database generated inside the notebook
Health_SQL_health.ipynb	    Main Jupyter Notebook with documentation + SQL code
README.md	                  Project documentation (this file)

How to Run This Project:
Install Jupyter Notebook or open Google Colab.
Run the following inside a code cell:
%load_ext sql
%sql sqlite:///health.db
