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
-- Makes the query easier to read
SELECT id,
       account_id,
       standard_qty,
       DATE_TRUNC('month', occurred_at) AS month,
       DENSE_RANK() OVER account_year_window AS dense_rank,
       SUM(standard_qty) OVER account_year_window AS sum_std_qty,
       COUNT(standard_qty) OVER account_year_window AS count_std_qty,
       AVG(standard_qty) OVER account_year_window AS avg_std_qty,
       MIN(standard_qty) OVER account_year_window AS min_std_qty,
       MAX(standard_qty) OVER account_year_window AS max_std_qty
FROM orders
WINDOW account_year_window AS (PARTITION BY account_id ORDER BY DATE_TRUNC('month',occurred_at))


-- ------------------------------------------------------------------------------------------------------------------
-- LAG and LEAD functions. Used for row comparison, similar to pandas df.rolling().
-- ------------------------------------------------------------------------------------------------------------------
-- LAG returns the value from a previous row to the current row in the table.
-- LEAD returns the value from the row following the current row in the table.
-- You can use LAG and LEAD functions whenever you are trying to compare the values in adjacent rows or rows that are offset by a certain number.
-- Example 1: You have a sales dataset with the following data and need to compare how the market segments fare against each other on profits earned.
WITH sub AS (SELECT account_id,
                    SUM(standard_qty) AS standard_sum
                    FROM orders 
                    GROUP BY 1)
SELECT account_id,
       standard_sum,
       LEAD(standard_sum) OVER (ORDER BY standard_sum) AS lead,
       LEAD(standard_sum) OVER (ORDER BY standard_sum) - standard_sum AS lead_difference
FROM sub

-- Imagine you're an analyst at Parch & Posey and you want to determine how the current order's total revenue ("total" meaning from sales of all 
-- types of paper) compares to the next order's total revenue. You'll need to use occurred_at and total_amt_usd in the orders table along with LEAD to do so. 
-- In your query results, there should be four columns: occurred_at, total_amt_usd, lead, and lead_difference.
-- A subquery is used to sum the values at similar timestamps
SELECT occurred_at,
       total_amt_usd,
       LEAD(total_amt_usd) OVER (ORDER BY occurred_at) AS lead,
       LEAD(total_amt_usd) OVER (ORDER BY occurred_at) - total_amt_usd AS lead_difference
FROM (SELECT occurred_at,
             SUM(total_amt_usd) AS total_amt_usd
      FROM orders 
      GROUP BY 1) AS sub;


-- ------------------------------------------------------------------------------------------------------------------
-- NTILE function. Used to identify what percentile (or quartile, or any other subdivision) a given row falls into
-- ------------------------------------------------------------------------------------------------------------------
-- This function is used with a window function.
-- Note NTILE(4) divides the rows into 4 groups where each group will be aproximately 25% of the data.
-- NTILE(100) will give the regular percentiles of a rows value as expected from a numpy array
-- In cases with relatively few rows in a window, the NTILE function doesn’t calculate exactly as you might expect. For example, If you only had two records and 
-- you were measuring percentiles, you’d expect one record to define the 1st percentile, and the other record to define the 100th percentile. Using the NTILE function, 
-- what you’d actually see is one record in the 1st percentile, and one in the 2nd percentile.

-- Use the NTILE functionality to divide the accounts into 4 levels in terms of the amount of standard_qty for their orders. Your resulting table should have the account_id, 
-- the occurred_at time for each order, the total amount of standard_qty paper purchased, and one of four levels in a standard_quartile column.
SELECT account_id,
       occurred_at,
       standard_qty,
       NTILE(4) OVER (PARTITION BY account_id ORDER BY standard_qty) 
FROM orders ORDER BY account_id DESC;

-- Use the NTILE functionality to divide the accounts into two levels in terms of the amount of gloss_qty for their orders. Your resulting table should have the account_id, 
-- the occurred_at time for each order, the total amount of gloss_qty paper purchased, and one of two levels in a gloss_half column.
SELECT account_id, occurred_at, NTILE(2) OVER (PARTITION BY account_id ORDER BY gloss_qty) 
FROM orders ORDER BY account_id DESC;

-- Use the NTILE functionality to divide the orders for each account into 100 levels in terms of the amount of total_amt_usd for their orders. Your resulting table should have 
-- the account_id, the occurred_at time for each order, the total amount of total_amt_usd paper purchased, and one of 100 levels in a total_percentile column.
SELECT account_id, occurred_at, total_amt_usd, NTILE(100) OVER (PARTITION BY account_id ORDER BY total_amt_usd) 
FROM orders ORDER BY account_id DESC;