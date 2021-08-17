# PRP-Backend

Provides API to backend of the Private-Resource-Planning (PRP).

![GitHub](https://img.shields.io/github/license/manuelbieri/PRP-Backend?label=License) ![GitHub](https://img.shields.io/badge/Coverage-99%25-success) ![GitHub repo size](https://img.shields.io/github/repo-size/manuelbieri/PRP-Backend) ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/manuelbieri/PRP-Backend) ![GitHub last commit](https://img.shields.io/github/last-commit/manuelbieri/PRP-Backend) ![GitHub Release Date](https://img.shields.io/github/release-date/manuelbieri/PRP-Backend)

### Documentation
Read the wiki on GitHub.com ([PRP - Backend Wiki](https://github.com/manuelbieri/PRP-Backend/wiki)) for explanations about the use.

### Included Modules
Modules for functionality:
- [API](src/API) : Interface for the clients.
- [Database](src/database) :  Database access for the api.
- [Users](src/users) :  Manages access for different users.
- [CustomException](src/customExceptions) : Provides custom exception for the backend.

Modules for tests:
- [API - Test](test/APITest) : Tests the api.
- [Database - Test](test/databaseTest) : Tests the database access fort the api.
- [Users - Test](test/usersTest) : Tests the users - module.
- [Utilities for tests](test/testUtilities) : Utilities for tests, e.g. setup and clean up databases.
