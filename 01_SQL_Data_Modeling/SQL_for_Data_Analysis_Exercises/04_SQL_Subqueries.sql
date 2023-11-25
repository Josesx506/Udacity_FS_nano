/* This module focuses on 
1. Subqueries - SQL queries with nested subqueries
2. Table Expressions
3. Persistent Derived Tables */


-- ------------------------------------------------------------------------------------------------------------------
-- Subqueries module. Each subquery tabe must be assigned an alias
-- ------------------------------------------------------------------------------------------------------------------
-- Use the udacity test environment to find the number of events that occur for each day for each channel
SELECT DATE_TRUNC('day', occurred_at) AS day,
       channel,
       COUNT(*) as event_count
FROM web_events
GROUP BY 1,2 ORDER BY 3 DESC;

--  Create a subquery that simply provides all the data from your first query
SELECT * 
FROM (SELECT DATE_TRUNC('day', occurred_at) AS day,
             channel,
             COUNT(*) as event_count
     FROM web_events
     GROUP BY 1,2) AS subquery;

-- Find the average number of events for each channel. Since it has been separated at daily intervals, this is 
-- giving an average value per day across channels
SELECT channel, 
       AVG(event_count) AS avg_event_count 
FROM (SELECT DATE_TRUNC('day', occurred_at) AS day,
             channel,
             COUNT(*) as event_count
     FROM web_events
     GROUP BY 1,2) AS subquery
GROUP BY 1 ORDER BY 2 DESC;

-- Logical statements like WHERE can be used with subqueries that return only one result. 
-- IN is the only statement that works when the subqueries contain multiple results.
-- Note that you should not include an alias when you write a subquery in a conditional statement. 
-- This is because the subquery is treated as an individual value (or set of values in the IN case) rather than as a table.

-- Use DATE_TRUNC to pull `month` level information about the first order ever placed in the orders table
SELECT DATE_TRUNC('month', MIN(occurred_at)) FROM orders

-- Use the result from the previous query to find only orders that took place in the same month and year as the first order,
-- and then pull the average for each type of paper qty in this month
SELECT AVG(standard_qty) AS standard_avg,
       AVG(poster_qty) AS poster_qty_avg,
       AVG(gloss_qty) AS gloss_avg,
       SUM(total_amt_usd) as tot_amt,
       DATE_TRUNC('month', occurred_at)
FROM orders 
WHERE DATE_TRUNC('month', occurred_at) = (SELECT DATE_TRUNC('month', MIN(occurred_at)) 
                                          FROM orders)
GROUP BY 5; 


-- Provide the name of the sales_rep in each region with the largest amount of total_amt_usd sales.
-- ----------------------------------------------------------------------------------------------
--  Create the first table with sum values for total_amt_usd
SELECT sr.name as sr_name, 
       rg.name as rg_name, 
       SUM(od.total_amt_usd) tot_usd
FROM sales_reps sr
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN region rg ON sr.region_id = rg.id
JOIN orders od ON ac.id = od.account_id
GROUP BY 1,2 ORDER BY 3 DESC;

-- Create a second table which gets the max of the values by region for the first table
SELECT rg_name, MAX(tot_usd) AS max_reg_usd
FROM (SELECT sr.name as sr_name, 
             rg.name as rg_name, 
             SUM(od.total_amt_usd) tot_usd
      FROM sales_reps sr
      JOIN accounts ac ON sr.id = ac.sales_rep_id
      JOIN region rg ON sr.region_id = rg.id
      JOIN orders od ON ac.id = od.account_id
      GROUP BY 1,2) AS table1
GROUP BY rg_name ORDER BY 2;

-- Create a third table that joins the data from table 1 and 2
SELECT table1.sr_name, table1.rg_name, table1.tot_usd
FROM (SELECT sr.name as sr_name, 
             rg.name as rg_name, 
             SUM(od.total_amt_usd) tot_usd
     FROM sales_reps sr
     JOIN accounts ac ON sr.id = ac.sales_rep_id
     JOIN region rg ON sr.region_id = rg.id
     JOIN orders od ON ac.id = od.account_id
     GROUP BY 1,2) AS table1

JOIN (SELECT rg_name, MAX(tot_usd) AS max_reg_usd
      FROM (SELECT sr.name as sr_name, 
                rg.name as rg_name, 
                SUM(od.total_amt_usd) tot_usd
            FROM sales_reps sr
            JOIN accounts ac ON sr.id = ac.sales_rep_id
            JOIN region rg ON sr.region_id = rg.id
            JOIN orders od ON ac.id = od.account_id
            GROUP BY 1,2) AS table2
      GROUP BY rg_name) AS table3
ON table1.rg_name = table3.rg_name AND table1.tot_usd = table3.max_reg_usd;

-- For the region with the largest sales total_amt_usd, how many total orders were placed?
-- ----------------------------------------------------------------------------------------------
SELECT r.name, COUNT(o.total) total_orders
FROM sales_reps s
JOIN accounts a ON a.sales_rep_id = s.id
JOIN orders o ON o.account_id = a.id
JOIN region r ON r.id = s.region_id
GROUP BY r.name
HAVING SUM(o.total_amt_usd) = (SELECT MAX(total_amt)
                               FROM (SELECT r.name region_name, SUM(o.total_amt_usd) total_amt
                                     FROM sales_reps s
                                     JOIN accounts a ON a.sales_rep_id = s.id
                                     JOIN orders o ON o.account_id = a.id
                                     JOIN region r ON r.id = s.region_id
                                     GROUP BY r.name) AS sub);

-- How many accounts had more total purchases than the account name which has bought the most 
-- standard_qty paper throughout their lifetime as a customer?
-- ----------------------------------------------------------------------------------------------
SELECT COUNT(*)
FROM (SELECT a.name
      FROM orders o
      JOIN accounts a ON a.id = o.account_id
      GROUP BY 1
      HAVING SUM(o.total) > (SELECT total 
                             FROM (SELECT a.name act_name, SUM(o.standard_qty) tot_std, SUM(o.total) total
                                   FROM accounts a
                                   JOIN orders o ON o.account_id = a.id
                                   GROUP BY 1
                                   ORDER BY 2 DESC
                                   LIMIT 1) inner_tab)
                ) counter_tab;

-- For the customer that spent the most (in total over their lifetime as a customer) total_amt_usd, 
-- how many web_events did they have for each channel?
-- ----------------------------------------------------------------------------------------------
SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND a.id =  (SELECT id
                                    FROM (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
                                          FROM orders o
                                          JOIN accounts a ON a.id = o.account_id
                                          GROUP BY a.id, a.name
                                          ORDER BY 3 DESC
                                          LIMIT 1) inner_table)
GROUP BY 1, 2
ORDER BY 3 DESC;

-- What is the lifetime average amount spent in terms of total_amt_usd for the top 10 total spending accounts?
-- ----------------------------------------------------------------------------------------------
SELECT AVG(tot_spent)
FROM (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
      FROM orders o
      JOIN accounts a ON a.id = o.account_id
      GROUP BY a.id, a.name
      ORDER BY 3 DESC
      LIMIT 10) temp;

--  What is the lifetime average amount spent in terms of total_amt_usd, including only the companies that spent more per order, 
-- on average, than the average of all orders.
-- ----------------------------------------------------------------------------------------------
SELECT AVG(avg_amt) 
FROM (SELECT o.account_id, AVG(o.total_amt_usd) avg_amt 
      FROM orders o 
      GROUP BY 1 
      HAVING AVG(o.total_amt_usd) > (SELECT AVG(o.total_amt_usd) avg_all 
                                     FROM orders o)) temp_table;


-- ------------------------------------------------------------------------------------------------------------------
-- WITH statement. Allows you to create a subset table with an alias name
-- ------------------------------------------------------------------------------------------------------------------
-- WITH statement is often called a Common Table Expression or CTE
-- Unlike subqueries, the alias in a WITH statement is called before the AS expression
-- Two WITH statements cannot be used simultaneously. Instead use one WITH statement, and separate the table names with comma `,`.
WITH events AS (SELECT DATE_TRUNC('day', occurred_at) AS day,
                       channel,
                       COUNT(*) AS event_count
                FROM web_events
                GROUP 1,2)
-- `events` is the new table alias created using a WITH statement
SELECT channel, AVG(event_count) AS avg_event_count
FROM events
GROUP BY 1
ORDER BY 2 DESC;

-- When creating multiple tables using WITH, you add a comma after every table leading to your final query
WITH table1 AS (SELECT * FROM web_events),
     table2 AS (SELECT * FROM accounts)

SELECT * FROM table1
JOIN table2 ON table1.account_id = table2.id;

-- Provide the name of the sales_rep in each region with the largest amount of total_amt_usd sales.
WITH table1 AS (SELECT sr.name as sr_name, 
                       rg.name as rg_name, 
                       SUM(od.total_amt_usd) tot_usd
                FROM sales_reps sr
                JOIN accounts ac ON sr.id = ac.sales_rep_id
                JOIN region rg ON sr.region_id = rg.id
                JOIN orders od ON ac.id = od.account_id
                GROUP BY 1,2 ORDER BY 3 DESC),
    -- Create table 2
     table2 AS (SELECT rg_name, MAX(tot_usd) AS max_reg_usd
                FROM table1
                GROUP BY rg_name ORDER BY 2)

SELECT table1.sr_name, table1.rg_name, table1.tot_usd
FROM table1
JOIN table2
ON table1.rg_name = table2.rg_name AND table1.tot_usd = table2.max_reg_usd;

-- For the region with the largest sales total_amt_usd, how many total orders were placed?
WITH table1 AS (SELECT rg.name as rg_name, 
                       SUM(od.total_amt_usd) tot_usd
                FROM sales_reps sr
                JOIN accounts ac ON sr.id = ac.sales_rep_id
                JOIN region rg ON sr.region_id = rg.id
                JOIN orders od ON ac.id = od.account_id
                GROUP BY rg_name)

SELECT rg.name, COUNT(od.total) total_orders
FROM region rg
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN orders od ON ac.id = od.account_id
GROUP BY rg.name
HAVING SUM(od.total_amt_usd) = (SELECT MAX(tot_usd) FROM table1);

-- For the account that purchased the most (in total over their lifetime as a customer) standard_qty paper, 
-- how many accounts still had more in total purchases?
WITH t1 AS (SELECT a.name account_name, SUM(o.standard_qty) total_std, SUM(o.total) total
            FROM accounts a
            JOIN orders o ON o.account_id = a.id
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 1), 
     t2 AS (SELECT a.name
            FROM orders o
            JOIN accounts a ON a.id = o.account_id
            GROUP BY 1
            HAVING SUM(o.total) > (SELECT total FROM t1))

SELECT COUNT(*) FROM t2;

-- For the customer that spent the most (in total over their lifetime as a customer) total_amt_usd, 
-- how many web_events did they have for each channel?
WITH t1 AS (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
            FROM orders o
            JOIN accounts a ON a.id = o.account_id
            GROUP BY a.id, a.name
            ORDER BY 3 DESC
            LIMIT 1)

SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w ON a.id = w.account_id AND a.id =  (SELECT id FROM t1)
GROUP BY 1, 2
ORDER BY 3 DESC;

-- What is the lifetime average amount spent in terms of total_amt_usd for the top 10 total spending accounts?
WITH t1 AS (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
            FROM orders o
            JOIN accounts a ON a.id = o.account_id
            GROUP BY a.id, a.name
            ORDER BY 3 DESC
            LIMIT 10)

SELECT AVG(tot_spent) FROM t1;

-- What is the lifetime average amount spent in terms of total_amt_usd, including only the companies that spent
-- more per order, on average, than the average of all orders.
WITH t1 AS (SELECT AVG(o.total_amt_usd) avg_all 
            FROM orders o 
            JOIN accounts a ON a.id = o.account_id), 
    t2 AS  (SELECT o.account_id, AVG(o.total_amt_usd) avg_amt 
            FROM orders o 
            GROUP BY 1 
            HAVING AVG(o.total_amt_usd) > (SELECT * FROM t1)) 

SELECT AVG(avg_amt) FROM t2; 