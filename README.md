# Period and Schedule Management API

This repository contains a Flask-based API for managing periods and their associated schedules. The API allows you to create, read, update, and delete periods and schedules, as well as perform various other operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Migrations](#database-migrations)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/tungBKDN/life-assistance-server.git
    cd life-assistance-server
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    flask db upgrade
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. The API will be available at `http://127.0.0.1:5000/api`.

## API Endpoints

### Periods

- **GET /api/periods**: Retrieve all periods.
- **GET /api/periods/<int:id>**: Retrieve a specific period by ID.
- **POST /api/periods**: Create a new period.
- **PUT /api/periods/<int:id>**: Update an existing period by ID.
- **DELETE /api/periods/<int:id>**: Delete a specific period by ID.
- **DELETE /api/periods/**: Delete all periods.
- **DELETE /api/periods/unactive**: Delete all inactive periods.
- **GET /api/periods/agenda**: Retrieve the agenda for the current day.


## Database Migrations

This project uses Flask-Migrate for handling database migrations. To create a new migration, run:
```sh
flask db migrate -m "Migration message"
