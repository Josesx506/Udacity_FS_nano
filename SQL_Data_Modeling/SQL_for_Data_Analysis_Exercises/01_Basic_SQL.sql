-- create and populate the database using PostgreSQL
createdb parch
psql parch < parch_and_posey.sql

-- PS: Double quotes (" ") do not work for strings, and single quotes ('') are required

-- ------------------------------------------------------------------------------------------------------------------
-- SELECT command. Allows you to access multiple columns from tables
-- ------------------------------------------------------------------------------------------------------------------
-- SELECT <columns> FROM <table_name>;
-- "*" is used to select all the column names in a table
SELECT id, account_id FROM orders;
SELECT * FROM orders;

-- ------------------------------------------------------------------------------------------------------------------
-- LIMIT command. Each command ends with a ";"
-- ------------------------------------------------------------------------------------------------------------------
--  This is similar to a pandas .head() or .tail() command
SELECT occurred_at,account_id,channel 
FROM web_events 
LIMIT 15;

-- ------------------------------------------------------------------------------------------------------------------
-- ORDER BY command. Used to sort a query by a column or multiple columns.
-- ------------------------------------------------------------------------------------------------------------------
-- Equivalent to pandas sort_values.
-- Default is ascending order but "DESC" decorator can be used to sort in descending order
SELECT * FROM orders
ORDER BY occurred_at DESC
LIMIT 100;

-- Write a query to return the 10 earliest orders in the orders table
-- Include the id, occurred_at, and total_amt_usd.
SELECT id,occurred_at,total_amt_usd FROM orders
ORDER BY occurred_at LIMIT 10;

-- Write a query to return the top 5 orders in terms of largest total_amt_usd
-- Include the id, account_id, and total_amt_usd.
SELECT id,account_id,total_amt_usd FROM orders
ORDER BY total_amt_usd DESC LIMIT 5;

-- Write a query to return the lowest 20 orders in terms of smallest total_amt_usd. 
-- Include the id, account_id, and total_amt_usd.
SELECT id,account_id,total_amt_usd FROM orders
ORDER BY total_amt_usd LIMIT 20;

-- Write a query that displays the order ID, account ID, and total dollar amount for all the orders, 
-- sorted first by the account ID (in ascending order), and then by the total dollar amount (in descending order)
SELECT id,account_id,total_amt_usd FROM orders
ORDER BY account_id, total_amt_usd DESC;

-- Now write a query that again displays order ID, account ID, and total dollar amount for each order, but this 
-- time sorted first by total dollar amount (in descending order), and then by account ID (in ascending order)
SELECT id,account_id,total_amt_usd FROM orders
ORDER BY total_amt_usd DESC, account_id;

-- ------------------------------------------------------------------------------------------------------------------
-- WHERE command. Used to filter tables. Can work with numeric or non-numeric data.
-- ------------------------------------------------------------------------------------------------------------------
-- Equivalent to pandas/python "== or > or <" e.g df_orders_20 = df[(df.orders > 20)]
-- You will notice when using these WHERE statements, we do not need to ORDER BY unless we want to actually order our data. 
-- Our condition will work without having to do any sorting of the data.
-- Pull the first 5 rows and all columns from the orders table that have a dollar amount of gloss_amt_usd greater than or equal to 1000
SELECT * FROM orders WHERE gloss_amt_usd >= 1000 LIMIT 5;

-- Pull the first 10 rows and all columns from the orders table that have a total_amt_usd less than 500.
SELECT * FROM orders WHERE total_amt_usd < 500 LIMIT 10;

-- Commonly when we are using WHERE with non-numeric data fields, we use the LIKE, NOT, or IN operators.
-- Filter the accounts table to include the company name, website, and the primary point of contact (primary_poc) 
-- just for the Exxon Mobil company in the accounts table.
SELECT name,website,primary_poc FROM accounts
WHERE name = 'Exxon Mobil';


-- ------------------------------------------------------------------------------------------------------------------
-- Arithmetic Operators. "*, +, -, /"
-- ------------------------------------------------------------------------------------------------------------------
-- Creating a new column that is a combination of existing columns is known as a derived column (or "calculated" or "computed" column).
-- Usually you want to give a name, or "alias," to your new column using the AS keyword.

-- Create a column that divides the standard_amt_usd by the standard_qty to find the unit price for standard paper for each order. 
-- Limit the results to the first 10 orders, and include the id and account_id fields.
SELECT id, account_id, 
standard_amt_usd/standard_qty AS unit_price 
FROM orders LIMIT 10;

-- Write a query that finds the percentage of revenue that comes from poster paper for each order. You will need to use only the columns that end with _usd. 
-- (Try to do this without using the total column.) Display the id and account_id fields also.
-- An error will occur because at least one of the values in the data creates a division by zero in the formula.
SELECT id, account_id, 
poster_amt_usd / (standard_amt_usd+gloss_amt_usd+poster_amt_usd) AS post_per
FROM orders;


-- ------------------------------------------------------------------------------------------------------------------
-- Logical Operators. "LIKE, IN, NOT, AND & BETWEEN, OR"
-- ------------------------------------------------------------------------------------------------------------------

-- LIKE operator
-- ----------------------------------------------------------------------------------------------
-- Uses wildcats with '%' operator. This is like the equivalent of '*' in terminal
-- e.g. '%g' is for ends with 'g'. 'a%' is for starts with 'a'. '%abc%' is for contains 'abc'

-- Use the accounts table to find
-- All the companies whose names start with 'C'.
SELECT * FROM accounts WHERE name LIKE 'C%';
-- All companies whose names contain the string 'one' somewhere in the name.
SELECT * FROM accounts WHERE name LIKE '%one%';
-- All companies whose names end with 's'.
SELECT * FROM accounts WHERE name LIKE '%s';

-- IN operator. Equivalent to pandas column.isin()
-- ----------------------------------------------------------------------------------------------
-- list of values are inserted in brackets e.g.(2,5,10) instead of square brackets like python lists
SELECT * FROM orders WHERE account_id UN (1001, 1021);

-- Use the accounts table to find the account name, primary_poc, and sales_rep_id for Walmart, Target, and Nordstrom.
SELECT name,primary_poc,sales_rep_id FROM accounts 
WHERE name IN ('Walmart', 'Target', 'Nordstrom');

-- Use the web_events table to find all information regarding individuals who were contacted via the channel of organic or adwords.
SELECT * FROM web_events WHERE channel IN ('organic', 'adwords');

-- NOT operator. Opposite of 'IN' or 'LIKE'. Equivalent to '~' in pandas
-- ----------------------------------------------------------------------------------------------
-- Use the accounts table to find the account name, primary poc, and sales rep id for all stores except Walmart, Target, and Nordstrom.
SELECT name,primary_poc,sales_rep_id FROM accounts 
WHERE name NOT IN ('Walmart', 'Target', 'Nordstrom');

-- Use the web_events table to find all information regarding individuals who were contacted via any method except using organic or adwords methods.
SELECT name,primary_poc,sales_rep_id FROM accounts 
SELECT * FROM web_events WHERE channel NOT IN ('organic', 'adwords');

-- Use the accounts table to find: 
-- All the companies whose names do not start with 'C'.
SELECT * FROM accounts WHERE name NOT LIKE 'C%';
-- All companies whose names do not contain the string 'one' somewhere in the name.
SELECT * FROM accounts WHERE name NOT LIKE '%one%';
-- All companies whose names do not end with 's'.
SELECT * FROM accounts WHERE name NOT LIKE '%s';

-- AND & BETWEEN operators. Can be used to find items within a range or items that satisfy multiple criteria. All conditions must be met.
-- ----------------------------------------------------------------------------------------------
-- Write a query that returns all the orders where the standard_qty is over 1000, the poster_qty is 0, and the gloss_qty is 0
SELECT * FROM orders where standard_qty > 1000 AND poster_qty = 0 AND gloss_qty = 0;
-- Using the accounts table, find all the companies whose names do not start with 'C' and end with 's'.
SELECT * FROM accounts WHERE name NOT LIKE 'C%' AND name LIKE '%s';
-- Write a query that displays the order date and gloss_qty data for all orders where gloss_qty is between 24 and 29.
-- Unlike numpy or pandas, the range in sql includes the values of your endpoint.
SELECT occurred_at,gloss_qty FROM orders WHERE gloss_qty BETWEEN 24 AND 29;
-- Use the web_events table to find all information regarding individuals who were contacted via the organic or adwords channels, 
-- and started their account at any point in 2016, sorted from newest to oldest.
-- Because SQL assumes the time is at 00:00:00 (i.e. midnight) for dates. The right-side endpoint is set to '2017-01-01'
SELECT * FROM web_events WHERE channel IN ('organic', 'adwords') 
AND occurred_at BETWEEN '2016-01-01' AND '2017-01-01' 
ORDER BY occurred_at DESC;

-- OR operator. Can be used to find rows that satisfy two or more conditions, where either condition can be met.
-- ----------------------------------------------------------------------------------------------
-- Parenthesis can be used to separate multiple logical operators 
-- Find list of orders ids where either gloss_qty or poster_qty is greater than 4000. Only include the id field in the resulting table.
SELECT id FROM orders WHERE gloss_qty > 4000 OR poster_qty > 4000;
-- Write a query that returns a list of orders where the standard_qty is zero and either the gloss_qty or poster_qty is over 1000.
SELECT * FROM orders WHERE standard_qty = 0 
AND (gloss_qty>1000 OR poster_qty>1000);
-- Find all the company names that start with a 'C' or 'W', and the primary contact contains 'ana' or 'Ana', but it doesn't contain 'eana'.
SELECT * FROM accounts WHERE (name LIKE 'C%' OR name LIKE 'W%') 
AND (primary_poc LIKE '%ana%' OR primary_poc LIKE '%Ana%') AND (primary_poc NOT LIKE '%eana%');