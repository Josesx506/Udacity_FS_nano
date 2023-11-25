-- This for performing joins over large datasets and performing efficient queries that run quickly. 
-- Many of the examples will be edge cases

-- ------------------------------------------------------------------------------------------------------------------
-- FULL OUTER JOIN statement. aka FULL JOIN
-- ------------------------------------------------------------------------------------------------------------------
-- Inner join recap
SELECT column_name(s) FROM Table_A
INNER JOIN Table_B ON Table_A.column_name = Table_B.column_name;
-- Left join recap
SELECT column_name(s) FROM Table_A
LEFT JOIN Table_B ON Table_A.column_name = Table_B.column_name;
-- Right join recap
SELECT column_name(s) FROM Table_A
RIGHT JOIN Table_B ON Table_A.column_name = Table_B.column_name;
-- FULL OUTER JOIN. A full outer join returns unmatched records in each table with null values for the columns that came from the opposite table.
-- A common application of this is when joining two tables on a timestamp.
SELECT column_name(s) FROM Table_A
FULL OUTER JOIN Table_B ON Table_A.column_name = Table_B.column_name;
-- If you wanted to return unmatched rows only, which is useful for some cases of data assessment, you can isolate them by adding the following line to the end of the query
SELECT column_name(s) FROM Table_A
FULL OUTER JOIN Table_B ON Table_A.column_name = Table_B.column_name
WHERE Table_A.column_name IS NULL OR Table_B.column_name IS NULL;


-- Say you're an analyst at Parch & Posey and you want to see:
-- each account who has a sales rep and each sales rep that has an account (all of the columns in these returned rows will be full)
-- This type of question is rare, but FULL OUTER JOIN is perfect for it. In the following SQL Explorer, write a query with FULL OUTER JOIN to fit the above described 
-- Parch & Posey scenario (selecting all of the columns in both of the relevant tables, accounts and sales_reps) then answer the subsequent multiple choice quiz.
SELECT ac.*, sr.* FROM accounts ac
FULL JOIN sales_reps sr ON ac.sales_rep_id = sr.id;

-- but also each account that does not have a sales rep and each sales rep that does not have an account (some of the columns in these returned rows will be empty)
SELECT ac.*, sr.* FROM accounts ac
FULL JOIN sales_reps sr ON ac.sales_rep_id = sr.id
WHERE ac.sales_rep_id IS NULL OR sr.id IS NULL;


-- ------------------------------------------------------------------------------------------------------------------
-- Inequality JOIN statements.
-- ------------------------------------------------------------------------------------------------------------------
-- Expert Tip
-- join clause is evaluated before the where clause -- filtering in the join clause will eliminate rows before they are joined, 
-- while filtering in the WHERE clause will leave those rows in and produce some nulls.

-- write a query that left joins the accounts table and the sales_reps tables on each sale rep's ID number and joins it using the < comparison operator on accounts.primary_poc 
-- and sales_reps.name like `accounts.primary_poc < sales_reps.name`. The query results should be a table with three columns: the account name, the primary contact name, and the 
-- sales representative's name.
SELECT ac.name ac_name, ac.primary_poc, sr.name 
FROM accounts ac
LEFT JOIN sales_reps sr 
ON ac.sales_rep_id = sr.id AND ac.primary_poc < sr.name;


-- ------------------------------------------------------------------------------------------------------------------
-- Self JOIN statements.
-- ------------------------------------------------------------------------------------------------------------------
-- This comes up pretty commonly in job interviews. Self JOIN logic can be pretty tricky
-- Used to find cases where two events both occurred one after another e.g. find simultaneous orders within the same month from the same customer
SELECT o1.id AS o1_id,
       o1.account_id AS o1_account_id,
       o1.occurred_at AS o1_occurred_at,
       o2.id AS o2_id,
       o2.account_id AS o2_account_id,
       o2.occurred_at AS o2_occurred_at
  FROM orders o1
 LEFT JOIN orders o2                                           -- Join the orders table on itself
   ON o1.account_id = o2.account_id
  AND o2.occurred_at > o1.occurred_at                          -- Find where the date of the order in the second table is > the first order date
  AND o2.occurred_at <= o1.occurred_at + INTERVAL '28 days'    -- Impose a clause to confirm the second order date is within a month's duration
ORDER BY o1.account_id, o1.occurred_at


-- Perform the same interval analysis on the web_events table but change the interval to 1 day to find those web events that occurred after, but not more than 1 day after, 
-- another web event. Add a column for the channel variable in both instances of the table in your query
SELECT  we1.id AS we1_id,
        we1.account_id AS we1_account_id,
        we1.channel AS we1_chan,
        we1.occurred_at AS we1_occurred_at,
        we2.id AS we2_id,
        we2.account_id AS we2_account_id,
        we2.channel AS we2_chan,
        we2.occurred_at AS we2_occurred_at
FROM web_events we1
LEFT JOIN web_events we2
    ON we1.account_id = we2.account_id
    AND we2.occurred_at > we1.occurred_at
    AND we2.occurred_at <= we1.occurred_at + INTERVAL '1 day'
ORDER BY we1.account_id, we1.occurred_at;


-- ------------------------------------------------------------------------------------------------------------------
-- Appending Data via UNION operator. Equivalent to pd.concat()
-- ------------------------------------------------------------------------------------------------------------------
-- The UNION operator is used to combine the result sets of 2 or more SELECT statements. It removes duplicate rows between the various SELECT statements
-- Each SELECT statement within the UNION must have the same number of fields in the result sets with similar data types.
-- Typically, the use case for leveraging the UNION command in SQL is when a user wants to pull together distinct values of specified columns that are spread across multiple tables. 
-- For example, a chef wants to pull together the ingredients and respective aisle across three separate meals that are maintained in different tables.

-- Expert tip
-- UNION removes duplicate rows and retains only distinct rows.
-- UNION ALL does not remove duplicate rows and can be used to merge rows with repeated data

-- A common misconception is that column names have to be the same. Column names, in fact, don't need to be the same to append two tables but you will find that they typically are.

-- Write a query that uses UNION ALL on two instances (and selecting all columns) of the accounts table.
SELECT * FROM accounts ac1
UNION ALL
SELECT * FROM accounts ac2

-- Add a WHERE clause to each of the tables that you unioned in the query above, filtering the first table where name equals Walmart and filtering the second table where name equals Disney.
SELECT * FROM accounts ac1 WHERE name = 'Walmart'
UNION ALL
SELECT * FROM accounts ac2 WHERE name = 'Disney'
-- Another way to write the function is 
SELECT * FROM accounts WHERE name = 'Walmart' OR name='Disney'

-- Perform the union in your first query (under the Appending Data via UNION header) in a common table expression and name it double_accounts. 
-- Then do a COUNT the number of times a name appears in the double_accounts table. If you do this correctly, your query results should have a count of 2 for each name.
WITH accts AS  (SELECT * FROM accounts ac1
                UNION ALL
                SELECT * FROM accounts ac2)
SELECT name, COUNT(*) AS name_count 
FROM accts
GROUP BY 1;


-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- PERFROMANCE TUNING. Accuracy is more important than runspeed.
-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/* One way to make a query run faster is to reduce the number of calculations that need to be performed. 
Some of the high-level things that will affect the number of calculations a given query will make include:
 - Table size
 - Joins
 - Aggregations
Query runtime is also dependent on some things that you can’t really control related to the database itself:
 - Other users running queries concurrently on the database
 - Database software and optimization (e.g., Postgres is optimized differently than Redshift)*/

-- 1. You can perform the query on a small dataset by using WHERE to reduce the number of rows before extending to entire dataset

-- 2. Using smaller limits of rows doesn't improve aggregation speed because the aggregation is performed before the LIMIT/WHERE statement is implemented.
-- To limit the size of the dataset for testing an aggregation function, use a subquery to create a table with a smaller number of rows
WITH sub AS (SELECT * FROM orders LIMIT 100)
-- The perform the aggregation tests on the smaller table.

-- 3. Make your JOIN statements less complicated by reducing the number of rows using pre-aggregation
-- e.g. if two unequally sized tables are to be joined and a COUNT function should be performed.
--      COUNT can be originally applied to the table with more rows to reduce it's size prior to joining the smaller table. example
SELECT a.name, sub.web_events 
FROM (SELECT account_id, COUNT(*) AS web_events
      FROM web_events
      GROUP BY 1) AS sub
JOIN accounts a ON a.id = sub.account_id
ORDER BY 2 DESC;

-- 4. The EXPLAIN function can be used like python timeit to estimate the runtime of a query and it also provides the steps breakdown
EXPLAIN
SELECT * FROM web_event LIMIT 100;
-- YOu can use EXPLAIN to revise queries and reduce the cost to be lower and efficient

-- 5. JOINing Subqueries to Improve Performance. We'll reduce the number of rows from 74000 to 1120 and improve efficiency.
-- e.g. Consider this long query which uses COUNT(DISTINCT) that takes a while to implement
SELECT o.occurred_at AS date,
       a.sales_rep_id,
       o.id AS order_id,
       we.id AS web_event_id
FROM   accounts a
JOIN   orders o
ON     o.account_id = a.id
JOIN   web_events we
ON     DATE_TRUNC('day', we.occurred_at) = DATE_TRUNC('day', o.occurred_at)
ORDER BY 1 DESC
-- Subquery 1
SELECT  DATE_TRUNC('day', o.occurred_at) AS date,
        COUNT(a.sales_rep_id) AS active_sales_reps,
        COUNT(o.id) AS orders
FROM accounts a
JOIN orders o ON a.id = o.account_id
GROUP BY 1
-- Subquery 2
SELECT  DATE_TRUNC('day', we.occurred_at) AS date,
        COUNT(we.id) AS web_visits
FROM web_events we
GROUP BY 1
-- Replace null date values with COALESCE and use a full join from both subqueries
SELECT  COALESCE(orders.date, web_events.date) AS date,
        orders.active_sales_reps,
        orders.orders,
        web_events.web_visits
FROM (SELECT  DATE_TRUNC('day', o.occurred_at) AS date,
              COUNT(a.sales_rep_id) AS active_sales_reps,
              COUNT(o.id) AS orders
      FROM accounts a
      JOIN orders o ON a.id = o.account_id
      GROUP BY 1) AS orders
FULL JOIN (SELECT  DATE_TRUNC('day', we.occurred_at) AS date,
                   COUNT(we.id) AS web_visits
           FROM web_events we
           GROUP BY 1) AS web_events
ON orders.date = web_events.date
ORDER BY 1;

