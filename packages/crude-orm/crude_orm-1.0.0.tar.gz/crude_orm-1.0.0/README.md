# Krude: A Descriptive ORM for Python
Krude is a simple, lightweight ORM for Python which owes its ease-of-use to the
fact that it is a _descriptive_ ORM rather than a _prescriptive_ one. What does
that mean? It means you can connect to your existing database, and Crude will
automatically generate an API in which you can interact with your data in an
object-oriented manner:

```python
from krude import connect

table_builder = connect("./mydatabase.db")          # Your SQLite Database
MyTable = table_builder.create("mytable")           # A table in your database
my_record = Mytable.load(myPrimaryKeyColumn=1)      # Load using primary key(s)  
value = my_record.myTextColumn                      # Read from DB
my_record.myTextColumn = "Hello, world"             # Write to DB
```

Krude currently supports all CRUD operations on Sqlite databases. Further
operations and database engines will be supported soon.

# Download and Install
The latest stable version of Krude can be installed using `pip install krude`.
You may also download all releases from the official GitHub repository.

# Homepage and Documentation
The official Krude homepage, as well as the latest API documentation, can be
found at https://krude.net