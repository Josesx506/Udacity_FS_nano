import psycopg2

# Create a connection to the database
conn = psycopg2.connect('dbname=fyyur') 
# Cursor is used to queue up tasks
cur = conn.cursor()

# Retrieve rows from table 2
cur.execute('SELECT * FROM table2;')

# Assign the sql query to a python variable. cur.fetchone() and cur.fetchmany() can also be used
# Note: cur.fectchall() grabs all the data from the SElECT statement above, and leaves nothing for 
#       subsequent fetch results except a new query is executed below it.
result = cur.fetchall()
print('\n', result, '\n')

# Commit the changes to the database
conn.commit()

# Close the cursor and connection (This is not done automatically)
cur.close()
conn.close()