To perform an initial migration of data from your local database to a Supabase table, you can follow these steps:

# Step 1: Export Data from Local Database

 Depending on your local database (e.g., PostgreSQL, MySQL), you can use a command-line tool or a GUI tool to export your data. For PostgreSQL, you can use the pg_dump command:

pg_dump -U your_username -d your_database_name -t your_table_name --data-only --column-inserts > data.sql

This command will create a SQL file (data.sql) containing the data from the specified table.


# Step 2: Prepare the SQL File

Open the data.sql file and ensure that the insert statements are compatible with Supabase. You may need to adjust the table name if it differs in Supabase.

# Step 3: Connect to Supabase
Use a PostgreSQL client (like psql, DBeaver, or pgAdmin) to connect to your Supabase database. You can find the connection details (host, port, database name, username, and password) in the API section of your Supabase project settings.

# Step 4: Import Data to Supabase
Once connected to your Supabase database, you can execute the SQL file to insert the data. If you're using psql, you can run:

\i /path/to/data.sql

This command will execute the SQL commands in the data.sql file, inserting the data into your Supabase table.

# Step 5: Verify Data Migration
After the import, you can run a SELECT query in Supabase to verify that the data has been migrated successfully:

SELECT * FROM your_table_name;

