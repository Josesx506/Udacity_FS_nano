/*
JOIN statements. Types include INNER, OUTER, LEFT, RIGHT.
Equivalent to pd.merge() in pandas.
LEFT and RIGHT joins are subsets of outer joins, and they are interchangeable. 
The table mentioned first in a join statement is always the 'left table' and the second table mentioned in a 'right table'.
Changing the order in which the tables are mentioned affects which one is left or right.
Typically left joins are mostly used and the Udacity course uses them for the rest of the course.
Discusses database (db) normalization, how dbs should be set up to reduce latency when queried etc.
Check out more on db normalization here - https://www.itprotoday.com/sql-server/sql-design-why-you-need-database-normalization
In the Entity Relationship Diagrams (ERD) for parch_and_posey db, PK is primary key, FK is foreign key.
For filtering purposes, using AND within the ON statement can reduce processing time for a join search instead of 
using WHERE after the join statement has been executed.
*/

-- ------------------------------------------------------------------------------------------------------------------
-- INNER JOIN statements. 
-- ------------------------------------------------------------------------------------------------------------------
SELECT orders.*, accounts.* FROM orders JOIN accounts 
ON orders.account_id = accounts.id;

-- Try pulling all the data from the accounts table, and all the data from the orders table.
SELECT accounts.*,orders.* FROM orders JOIN accounts
ON orders.account_id = accounts.id;

-- Try pulling standard_qty, gloss_qty, and poster_qty from the orders table, and the website and the primary_poc from the accounts table.
SELECT orders.standard_qty,orders.gloss_qty,orders.poster_qty,
accounts.website,accounts.primary_poc
FROM orders JOIN accounts
ON orders.account_id = accounts.id;


-- ALIAS. Can be used to shorten table names for queries for efficiency. 
-- It isn't explicitly written but can be represented with AS. Typically just leave a ' ' and the alias name to implement
-- ----------------------------------------------------------------------------------------------
-- Similar to renaming columns from arithmetic operations exercise with AS. e.g. FROM tablename AS t1 JOIN tablename2 AS t2
-- It's recommended to represent renamed table names with small-case alphabets
SELECT t1.column1 aliasname, t2.column2 aliasname2
FROM tablename AS t1 JOIN tablename2 AS t2 ON t1.id = t2.account_id;

-- Provide a table for all web_events associated with account name of Walmart. There should be three columns. 
-- Be sure to include the primary_poc, time of the event, and the channel for each event. Additionally, 
-- you might choose to add a fourth column to assure only Walmart events were chosen.
SELECT we.occurred_at,we.channel,ac.primary_poc,ac.name
FROM web_events we
JOIN accounts ac
ON we.account_id = ac.id
WHERE ac.name = 'Walmart';;

-- Provide a table that provides the region for each sales_rep along with their associated accounts. 
-- Your final table should include three columns: the region name, the sales rep name, and the account name. 
-- Sort the accounts alphabetically (A-Z) according to account name.
SELECT rg.name AS rg_name,sr.name AS sr_name, ac.name AS ac_name
FROM region rg
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac   ON sr.id = ac.sales_rep_id
ORDER BY ac.name;

-- Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) 
-- for the order. Your final table should have 3 columns: region name, account name, and unit price. A few accounts have 0 for total, 
-- so I divided by (total + 0.01) to assure not dividing by zero.
SELECT rg.name AS rg_name,ac.name AS ac_name, (od.total_amt_usd/(od.total+0.01)) AS unit_price
FROM region rg
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac   ON sr.id = ac.sales_rep_id
JOIN orders od     ON ac.id = od.account_id;


-- ------------------------------------------------------------------------------------------------------------------
-- LEFT JOIN statements. LEFT OUTER JOIN is equivalent to LEFT JOIN synthax.
-- ------------------------------------------------------------------------------------------------------------------
-- This allows you to include rows that have no data in a particular table within the query

-- Provide a table that provides the region for each sales_rep along with their associated accounts. This time only for the Midwest region. 
-- Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts 
-- alphabetically (A-Z) according to account name.
SELECT rg.name AS r_name, sr.name AS s_name, ac.name AS a_name 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id AND rg.name = 'Midwest'
JOIN accounts ac   ON sr.id = ac.sales_rep_id
ORDER BY ac.name;

-- Provide a table that provides the region for each sales_rep along with their associated accounts. 
-- This time only for accounts where the sales rep has a first name starting with S and in the Midwest region. 
-- Your final table should include three columns: the region name, the sales rep name, and the account name. 
-- Sort the accounts alphabetically (A-Z) according to account name.
SELECT rg.name AS r_name, sr.name AS s_name, ac.name AS a_name 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id AND rg.name = 'Midwest' AND sr.name LIKE 'S%'
JOIN accounts ac   ON sr.id = ac.sales_rep_id
ORDER BY ac.name;

-- Provide a table that provides the region for each sales_rep along with their associated accounts. 
-- This time only for accounts where the sales rep has a last name starting with K and in the Midwest region. 
-- Your final table should include three columns: the region name, the sales rep name, and the account name. 
-- Sort the accounts alphabetically (A-Z) according to account name.
SELECT rg.name AS r_name, sr.name AS s_name, ac.name AS a_name 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id AND rg.name = 'Midwest' AND sr.name LIKE '% K%'
JOIN accounts ac   ON sr.id = ac.sales_rep_id
ORDER BY ac.name;

-- Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. 
-- However, you should only provide the results if the standard order quantity exceeds 100. Your final table should have 3 columns: region name, 
-- account name, and unit price. In order to avoid a division by zero error, adding .01 to the denominator here is helpful total_amt_usd/(total+0.01)
SELECT rg.name AS r_name, ac.name AS a_name, od.total_amt_usd/(od.total+0.01) AS unit_price 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac   ON sr.id = ac.sales_rep_id
JOIN orders od     ON ac.id = od.account_id AND od.standard_qty > 100;

-- Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. 
-- However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. 
-- Your final table should have 3 columns: region name, account name, and unit price. Sort for the smallest unit price first. 
-- In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
SELECT rg.name AS r_name, ac.name AS a_name, od.total_amt_usd/(od.total+0.01) AS unit_price 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac   ON sr.id = ac.sales_rep_id
JOIN orders od     ON ac.id = od.account_id AND od.standard_qty > 100 AND od.poster_qty > 50
ORDER BY unit_price;

-- Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. 
-- However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. 
-- Your final table should have 3 columns: region name, account name, and unit price. Sort for the largest unit price first. 
-- In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
SELECT rg.name AS r_name, ac.name AS a_name, od.total_amt_usd/(od.total+0.01) AS unit_price 
FROM region rg 
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac   ON sr.id = ac.sales_rep_id
JOIN orders od     ON ac.id = od.account_id AND od.standard_qty > 100 AND od.poster_qty > 50
ORDER BY unit_price DESC;

-- What are the different channels used by account id 1001? 
-- Your final table should have only 2 columns: account name and the different channels. 
-- You can try SELECT DISTINCT to narrow down the results to only the unique values.
-- SELECT DISTINCT is the equivalent of pandas .unique()
SELECT DISTINCT ac.name, we.channel
FROM accounts ac
JOIN web_events we
ON ac.id = we.account_id AND ac.id = '1001';

-- Find all the orders that occurred in 2015. Your final table should have 4 columns: occurred_at, 
-- account name, order total, and order total_amt_usd.
SELECT od.occurred_at, ac.name, od.total, od.total_amt_usd
FROM orders od
JOIN accounts ac ON od.account_id = ac.id 
AND od.occurred_at >= '2015-01-01' AND od.occurred_at < '2016-01-01';