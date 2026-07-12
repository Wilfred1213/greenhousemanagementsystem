# SCL Greenhouse Production & Inventory Management System

## Overview

The **SCL Greenhouse Production & Inventory Management System** is a web-based application developed using Django to help greenhouse managers efficiently plan, monitor, and manage greenhouse production activities. The system integrates nursery management, production cycles, harvesting, operations, inventory control, supplier management, and reporting into a single platform.

This project was developed as an academic and practical greenhouse management solution.

---

## Features

### Dashboard

* Overview of greenhouse activities
* Production statistics
* Harvest summaries
* Inventory summary
* Quick navigation

### Greenhouse Management

* Register greenhouses
* Manage bays
* Manage beds
* View greenhouse performance

### Nursery Management

* Record nursery batches
* Track sowing dates
* Monitor germination
* Monitor transplant readiness

### Production Cycle Management

* Create production cycles
* Assign nursery batches
* Allocate beds
* Track production progress

### Harvest Management

* Record harvests
* Harvest grading
* Harvest history
* Harvest summaries

### Operations Management

* Record greenhouse operations
* Apply operations to selected beds, bays, or entire greenhouses
* Record labour costs
* Record product usage
* Track operational history

### Inventory Management

* Manage products
* Stock receipts
* Supplier management
* Inventory tracking

### Performance Monitoring

* Greenhouse performance
* Bed performance
* Production cycle performance
* Operation details

### Reports

* Harvest reports
* Production reports
* Inventory reports

---

## Technologies Used

* Python 3
* Django 5
* MySQL
* Bootstrap 5
* HTML5
* CSS3
* JavaScript
* HTMX

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project directory:

```bash
cd greenhouse_sql_project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

---

## Project Structure

* Dashboard
* Farmers
* Greenhouses
* Bays
* Beds
* Nursery
* Production Cycles
* Harvests
* Operations
* Inventory
* Suppliers
* Reports

---

## Future Improvements

* PDF report generation
* Excel exports
* QR code support for greenhouse assets
* Email notifications
* Offline data capture
* Mobile-friendly interface
* Advanced analytics dashboard

---

## Developer

**Wilfred Mathias**

Designed and developed as part of an agricultural management solution using Django and MySQL.

---

## License

This project is intended for educational and demonstration purposes.
