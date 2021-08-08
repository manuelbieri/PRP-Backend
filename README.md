# PRP-Backend

Provides API to backend of the Private-Resource-Planning (PRP).

### ToDo - API
`\items\index` : returns all items on the todo - list.

`\items?key=col_name&value=col_value` : returns all items meeting the arguments on the todo - list.

`\item?key=col_name&value=col_value` : returns an items meeting the arguments on the todo - list.


### Included Modules
Modules for functionality:
- [API](src/API) : Interface for the clients.
- [Database](src/database) :  Database access for the api.

Modules for tests:
- [API - Test](test/APITest) : Tests the api.
- [Database - Test](test/databaseTest) : Tests the database access fort the api.
- [Utilities for tests](test/testUtilities) : Utilities for tests, e.g. setup and clean up databases.
