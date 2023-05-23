<h1 align="center">
<img src="cmms/static/icon.svg"/>
<br/>CMMS<br/>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<a href="/LICENSE"><img alt="License: BSD-3-Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-blue.svg"></a>
</h1>

**Computerized Maintenance Management System** or **CMMS** is a webapp created for Pertamina Hulu Energi, designed to provide a reliable scheduling, tracking, reporting tools for equipment and facilities maintenance.

## Setup

### Prerequisites
- Python 3.10 or Newer
- [Poetry](https://python-poetry.org/docs/#installation)
- Redis (for Session Management and Cache)

### Deploy
- Run `poetry install` to install all required dependencies in a virtualenv
- Run `poetry run manage tailwind build` to build the website's CSS
- Finally run `poetry run start` to start the server

### Environment Variables

|Name|Description|Example|
|----|-----------|-------|
|DATABASE\_URL|URL to your database. Check out [`dj-database-url`](https://github.com/jazzband/dj-database-url#url-schema) for more information|`postgres://user:p#ssword!@localhost/foobar`|
|REDIS\_URL|URL to your redis. Check out [`django-redis`](https://github.com/jazzband/django-redis#configure-as-cache-backend) for more information|`redis://127.0.0.1:6379/1`|
