import psycopg2

# Create a connection to the database
conn = psycopg2.connect('dbname=fyyur') 
# Cursor is used to queue up tasks
cur = conn.cursor()

## drop any existing table2 table
cur.execute("DROP TABLE IF EXISTS table2;")

# Create a table
cur.execute('''
    CREATE TABLE table2 (
               id INTEGER PRIMARY KEY,
               description VARCHAR NOT NULL,
               completed BOOLEAN NOT NULL DEFAULT FALSE
    );
''')

# You can also use string interpolation '%s' or f-strings f'{}' to fill the transactions with python variables
# Define a one or more transactions that will be performed on the table.
cur.execute("INSERT INTO table2 (id, description, completed) VALUES (1, 'This is row 1', True);")
cur.execute(f"INSERT INTO table2 (id, description, completed) VALUES ({2}, 'This is row 2', {False});")
cur.execute("INSERT INTO table2 (id, description, completed) VALUES (%s, %s, %s);",
               (3, 'This is row 3', True))

# Commit the changes to the database. A rollback can also be performed with cur.rollback()
conn.commit()

# Close the cursor and connection (This is not done automatically)
cur.close()
conn.close()