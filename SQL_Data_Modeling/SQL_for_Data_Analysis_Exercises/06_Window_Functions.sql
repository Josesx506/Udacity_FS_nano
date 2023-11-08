-- ------------------------------------------------------------------------------------------------------------------
-- OVER statement. This allows you to implement window functions without using GROUP BY
-- ------------------------------------------------------------------------------------------------------------------
-- A window function performs a calculation across a set of table rows that are somehow related to the current row
-- You can get the average values of a quantity for each month without using GROUP BY. 
-- Also the query retains the original number of rows and replicates row values in the new column for rows that are aggregated
-- Note: You can’t use window functions and standard aggregations in the same query. More specifically, you can’t include window 
-- functions in a GROUP BY clause
-- https://www.postgresql.org/docs/9.1/tutorial-window.html

-- Using Derek's previous video as an example, create another running total. This time, create a running total of standard_amt_usd 
-- (in the orders table) over order time with no date truncation. Your final table should have two columns: one with the amount being 
-- added for each new row, and a second with the running total. The ORDER BY defines the grouping column.
SELECT standard_amt_usd, SUM(standard_amt_usd) OVER (ORDER BY occurred_at) AS running_total
FROM orders;

-- Now, modify your query from the previous quiz to include partitions. Still create a running total of standard_amt_usd (in the orders table) 
-- over order time, but this time, date truncate occurred_at by year and partition by that same year-truncated occurred_at variable. Your final 
-- table should have three columns: One with the amount being added for each row, one for the truncated date, and a final column with the 
-- running total within each year.
SELECT standard_amt_usd, 
       DATE_TRUNC('year', occurred_at), 
       SUM(standard_amt_usd) OVER (PARTITION BY DATE_TRUNC('year', occurred_at) 
                                   ORDER BY occurred_at) AS running_total
FROM orders;


-- ------------------------------------------------------------------------------------------------------------------
-- ROW_NUMBER & RANK & DENSE_RANK functions. These functions don't require input
-- ------------------------------------------------------------------------------------------------------------------
-- Select the id, account_id, and total variable from the orders table, then create a column called total_rank that ranks this total amount of 
-- paper ordered (from highest to lowest) for each account using a partition. Your final table should have these four columns.
SELECT  id, 
        account_id, 
        total, 
        RANK() OVER (PARTITION BY account_id ORDER BY total DESC) AS total_rank 
FROM orders;


-- Aggregate functions can be used in window functions
-- ----------------------------------------------------------------------------------------------
-- Deciding when or not to include ORDER By in a window function
-- The easiest way to think about this - leaving the ORDER BY out is equivalent to "ordering" in a way that all rows in the partition are "equal" to each other. 
-- Indeed, you can get the same effect by explicitly adding the ORDER BY clause like this: ORDER BY 0 (or "order by" any constant expression), or even, 
-- more emphatically, ORDER BY NULL.

-- Query from the video 
SELECT id,
       account_id,
       standard_qty,
       DATE_TRUNC('month', occurred_at) AS month,
       DENSE_RANK() OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS dense_rank,
       SUM(standard_qty) OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS sum_std_qty,
       COUNT(standard_qty) OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS count_std_qty,
       AVG(standard_qty) OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS avg_std_qty,
       MIN(standard_qty) OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS min_std_qty,
       MAX(standard_qty) OVER (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at)) AS max_std_qty
FROM orders


-- ------------------------------------------------------------------------------------------------------------------
-- WINDOW statement. Can be used to alias the order and partition of a window function when it's being called multiple times.
-- ------------------------------------------------------------------------------------------------------------------

SELECT id,
       account_id,
       standard_qty,
       DATE_TRUNC('month', occurred_at) AS month,
       DENSE_RANK() OVER main_window AS dense_rank,
       SUM(standard_qty) OVER main_window AS sum_std_qty,
       COUNT(standard_qty) OVER main_window AS count_std_qty,
       AVG(standard_qty) OVER main_window AS avg_std_qty,
       MIN(standard_qty) OVER main_window AS min_std_qty,
       MAX(standard_qty) OVER main_window AS max_std_qty
FROM orders
WINDOW main_window AS (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at))
