<h1 align="center"><code>CMMS</code></h1>

<h3 align="center"> A reliable scheduling, tracking, reporting tools for equipment and facilities maintenance.</h3>

## About
CMMS (Computerized Maintenance Management System) is a software designed to store maintenance data on a computer, whether it's a work order for a breakdown or a daily inspection. This software simplifies the maintenance management by giving users insight into the state of maintenance needs with comprehensive work order schedules, accurate inventory of spare parts, and access to very important reports. This information makes it easier for maintenance workers to do their jobs more effectively. CMMS is designed to be used in the medical field, but it can also be used in other industry.

![Work Orders](images/Feat_1.png)
![Work Orders](images/Feat_2.png)

## Usage

> **Note**
>
> For user usage, please read [USAGE.md](USAGE.md) instead!

### Prerequisites
- [NodeJS v15 or later](https://nodejs.org/en/)
- SQL-based Database ([MariaDB](https://mariadb.com) is recommended)
  - You can use [Ampps](https://www.ampps.com/downloads) if you're in a hurry
- A bit of SQL and JavaScript knowledge

### Setup

1. Create new database for CMMS, for this example we name it `cmms`.

2. Open the folder of the project using your IDE.

3. Copy `config.json-example` and paste it as `config.json`, then change `dbUrl` with your database connection url (e.g. `mysql://root:mysql@localhost:3306/cmms`)

4. Open terminal (or command prompt) and run `npm install`

5. After all the packages are installed you run the server by running `npm start` or `node server.js`.

6. You can access the CMMS by opening **localhost:5000** in your browser.

7. You will find the home of the CMMS. To see the rest of the CMMS you have to log in.

> **Note**: **email**: admin@gmail.com, **password**: 0000

8. Now you can see all the content of our website and edit it.

> **Note**: There is an uploaded SQL file for CMMS in [`.sql-dumps`](.sql-dumps/) if you need a sample data

<!-- I don't even know why you need this in the first place?
## CMMS Database Relation
![Work Orders](images/RM.png)
-->

## License
This software is licensed under [New BSD License](./LICENSE).
