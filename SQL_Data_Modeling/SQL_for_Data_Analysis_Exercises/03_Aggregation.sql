-- Aggregators only aggregate vertically - the values of a column. They are typically used in SELECT statements apart from GROUP BY.
-- To aggregate values across rows, you'll need to use arithmetic operators.
-- When identifying NULLs in a WHERE clause, we write IS NULL or IS NOT NULL. We don't use =, 
-- because NULL isn't considered a value in SQL. Rather, it is a property of the data.

-- ------------------------------------------------------------------------------------------------------------------
-- COUNT function. Similar to len() in python. Used to determine number of rows
-- ------------------------------------------------------------------------------------------------------------------
SELECT COUNT(accounts.id) FROM accounts;
-- Count the null rows in a table
SELECT COUNT(*) FROM accounts WHERE primary_poc IS NULL;


-- ------------------------------------------------------------------------------------------------------------------
-- SUM function. Sums rows but requires column names instead of wildcat "*"
-- ------------------------------------------------------------------------------------------------------------------
--  If an alias is not provided for each summed column in a multi-column sum query, only the last query is returned
SELECT  SUM(standard_qty) AS standard, 
        SUM(gloss_qty) AS gloss, 
        SUM(poster_qty) AS poster 
    FROM orders;
-- Find the total amount of poster_qty paper ordered in the orders table
SELECT SUM(poster_qty) AS poster FROM orders;
-- Find the total amount of standard_qty paper ordered in the orders table
SELECT SUM(standard_qty) AS standard FROM orders;
-- Find the total dollar amount of sales using the total_amt_usd in the orders table.
SELECT SUM(total_amt_usd) usd_amt FROM orders;
-- Find the total amount spent on standard_amt_usd and gloss_amt_usd paper for each individual order in the orders table. 
-- This should give a dollar amount for each order in the table.
SELECT standard_amt_usd + gloss_amt_usd AS total_standard_gloss FROM orders;
-- Find the standard_amt_usd per unit of standard_qty paper. Your solution should use both an aggregation and a mathematical operator.
SELECT SUM(standard_amt_usd)/SUM(standard_qty) per_unit FROM orders;

-- ------------------------------------------------------------------------------------------------------------------
-- MIN and MAX function.
-- ------------------------------------------------------------------------------------------------------------------
/* Functionally, MIN and MAX are similar to COUNT in that they can be used on non-numerical columns. Depending on the column type, 
MIN will return the lowest number, earliest date, or non-numerical value as early in the alphabet as possible. As you might suspect,
MAX does the opposite—it returns the highest number, the latest date,  or the non-numerical value closest alphabetically to “Z.” */
SELECT MIN(standard_qty) AS standard_min, MAX(standard_qty) AS standard_max FROM orders;

-- ------------------------------------------------------------------------------------------------------------------
-- AVG function. Returns arithmetic mean, and works only on numerical columns and ignores NULL values
-- ------------------------------------------------------------------------------------------------------------------
SELECT AVG(standard_qty) AS standard_avg FROM orders;
-- To include average of null values while representing them as zeros, use SUM()/COUNT()
-- This is probably not a good idea if the NULL values truly just represent unknown values for a cell
SELECT SUM(standard_qty)/COUNT(standard_qty) AS standard_avg FROM orders;

/* MEDIAN - Expert Tip
One quick note that a median might be a more appropriate measure of center for this data, but finding the median happens to be a 
pretty difficult thing to get using SQL alone — so difficult that finding a median is occasionally asked as an interview question. */

-- When was the earliest order ever placed? You only need to return the date.
SELECT MIN(occurred_at) AS earliest FROM orders;
-- Try performing the same query as in question 1 without using an aggregation function.
SELECT occurred_at FROM orders ORDER BY occurred_at LIMIT 1;
-- When did the most recent (latest) web_event occur?
SELECT MAX(occurred_at) AS latest FROM web_events;
-- Try to perform the result of the previous query without using an aggregation function.
SELECT occurred_at FROM web_events ORDER BY occurred_at DESC LIMIT 1;
-- Find the mean (AVERAGE) amount spent per order on each paper type, as well as the mean amount of each paper type purchased per order. 
-- Your final answer should have 6 values - one for each paper type for the average number of sales, as well as the average amount.
SELECT  AVG(standard_amt_usd) AS standard_amt_avg,
        AVG(gloss_amt_usd) AS gloss_amt_avg,
        AVG(poster_amt_usd) AS poster_amt_avg,
        AVG(standard_qty) AS standard_sales_avg,
        AVG(gloss_qty) AS gloss_sales_avg,
        AVG(poster_qty) AS poster_sales_avg
FROM orders;
-- Via the video, you might be interested in how to calculate the MEDIAN. Though this is more advanced than what we have covered so far try 
-- finding - what is the MEDIAN total_usd spent on all orders?
-- Udacity solution for median
SELECT *
FROM (SELECT total_amt_usd
         FROM orders
         ORDER BY total_amt_usd
         LIMIT 3457) AS Table1
ORDER BY total_amt_usd DESC
LIMIT 2;
-- My solution - Instead of hardcoding the 3457. It gives the same result as the Udacity solution above.
-- I couldn't get it to average out the two values to get the exact median.
SELECT *
FROM (SELECT total_amt_usd
         FROM orders
         ORDER BY total_amt_usd
         LIMIT (SELECT (COUNT(total_amt_usd)/2)+1 FROM orders)
     ) AS Table1
ORDER BY total_amt_usd DESC
LIMIT 2;


-- ------------------------------------------------------------------------------------------------------------------
-- GROUP BY function. Similar to pandas.groupby(). 
-- ------------------------------------------------------------------------------------------------------------------
-- Always goes between a WHERE clause and ORDER BY clause if they exist in a query.
-- GROUP BY can be used to aggregate data within subsets of the data. Any column in the SELECT statement that is not within an 
-- aggregator must be in the GROUP BY clause. It is worth noting that SQL evaluates the aggregations before the LIMIT clause.
-- Note: You can also group by the index values of the column names in a SELECT statement when the number of columns are numerous to list out
-- e.g., GROUP BY 1,2,3 ... 

-- Which account (by name) placed the earliest order? Your solution should have the account name and the date of the order.
SELECT ac.name, od.occurred_at FROM accounts ac
JOIN orders od ON ac.id = od.account_id 
ORDER BY od.occurred_at LIMIT 1;
-- Find the total sales in usd for each account. You should include two columns - the total sales for each company's orders 
-- in usd and the company name.
SELECT ac.name,SUM(od.total) AS tot_sales FROM accounts ac 
JOIN orders od ON ac.id = od.account_id 
GROUP BY ac.name ORDER BY ac.name;
-- Via what channel did the most recent (latest) web_event occur, which account was associated with this web_event? 
-- Your query should return only three values - the date, channel, and account name.
SELECT MAX(we.occurred_at) AS dates, we.channel, ac.name FROM web_events we
JOIN accounts ac ON we.account_id = ac.id
GROUP BY we.channel,ac.name 
ORDER BY dates DESC LIMIT 1;
-- Find the total number of times each type of channel from the web_events was used. Your final table should have two columns - 
-- the channel and the number of times the channel was used.
SELECT channel, COUNT(channel) FROM web_events GROUP BY channel;
-- Who was the primary contact associated with the earliest web_event?
SELECT ac.primary_poc, MIN(we.occurred_at) AS dates FROM accounts ac
JOIN web_events we ON ac.id = we.account_id
GROUP BY ac.primary_poc ORDER BY dates LIMIT 1;
-- What was the smallest order placed by each account in terms of total usd. Provide only two columns - 
-- the account name and the total usd. Order from smallest dollar amounts to largest.
SELECT ac.name, MIN(od.total_amt_usd) AS smallest_order FROM accounts ac
JOIN orders od ON ac.id = od.account_id
GROUP BY ac.name ORDER BY smallest_order;
-- Find the number of sales reps in each region. Your final table should have two columns - 
-- the region and the number of sales_reps. Order from fewest reps to most reps.
SELECT rg.name, COUNT(sr.name) AS num_sales_reps FROM region rg
JOIN sales_reps sr ON rg.id = sr.region_id
GROUP BY rg.name ORDER BY num_sales_reps;
-- For each account, determine the average amount of each type of paper they purchased across their orders. Your result should have 
-- four columns - one for the account name and one for the average quantity purchased for each of the paper types for each account.
SELECT  ac.name, 
        AVG(od.standard_qty) AS standard_qty_avg, 
        AVG(od.poster_qty) AS poster_qty_avg, 
        AVG(od.gloss_qty)  AS gloss_qty_avg
FROM accounts ac
JOIN orders od ON ac.id = od.account_id GROUP BY ac.name ORDER BY ac.name;
-- For each account, determine the average amount spent per order on each paper type. Your result should have four columns - 
-- one for the account name and one for the average amount spent on each paper type.
SELECT  ac.name, 
        AVG(od.standard_amt_usd) AS standard_amt_avg, 
        AVG(od.poster_amt_usd) AS poster_amt_avg, 
        AVG(od.gloss_amt_usd) AS gloss_amt_avg 
FROM accounts ac
JOIN orders od ON ac.id = od.account_id 
GROUP BY ac.name ORDER BY ac.name;
-- Determine the number of times a particular channel was used in the web_events table for each sales rep. Your final table should have three 
-- columns - the name of the sales rep, the channel, and the number of occurrences. 
-- Order your table with the highest number of occurrences first.
SELECT sr.name, we.channel, COUNT(we.channel) AS num_used FROM sales_reps sr 
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN web_events we ON ac.id = we.account_id
GROUP BY sr.name,we.channel ORDER BY num_used DESC;
-- Determine the number of times a particular channel was used in the web_events table for each region. Your final table should have three 
-- columns - the region name, the channel, and the number of occurrences. Order your table with the highest number of occurrences first.
SELECT rg.name, we.channel, COUNT(we.channel) AS num_used FROM region rg
JOIN sales_reps sr ON rg.id = sr.region_id
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN web_events we ON ac.id = we.account_id
GROUP BY rg.name, we.channel ORDER BY num_used DESC;


-- ------------------------------------------------------------------------------------------------------------------
-- DISTINCT function. Similar to pandas.unique(). 
-- ------------------------------------------------------------------------------------------------------------------
-- Extracts unique values in a column that can be used to group rows and replace GROUP BY if all columns in a query should be grouped.
-- DISTINCT is always used in SELECT statements, and it provides the unique rows for all columns written in the SELECT statement. 
-- Therefore, you only use DISTINCT once in any particular SELECT statement.
-- e.g. SELECT DISTINCT column1, column2, column3 FROM table1; is a valid query.
-- SELECT DISTINCT column1, DISTINCT column2, DISTINCT column3 FROM table1; is an incorrect query.
-- The latter example return sthe unique (or DISTINCT) rows across all three columns.
-- It’s worth noting that using DISTINCT, particularly in aggregations, can SSSLLLOOOWWW your queries down quite a bit.

-- Use DISTINCT to test if there are any accounts associated with more than one region.
SELECT DISTINCT ac.name AS acct_name, rg.name AS reg_name FROM accounts ac
JOIN sales_reps sr ON ac.sales_rep_id = sr.id
JOIN region rg ON sr.region_id = rg.id;
-- Have any sales reps worked on more than one account?
SELECT DISTINCT sr.name AS sr_name, ac.name AS acct_name FROM sales_reps sr
JOIN accounts ac ON sr.id = ac.sales_rep_id;

-- Udacity solution
-- Use DISTINCT to test if there are any accounts associated with more than one region.
--  This shows that every account is associated with only one region.
SELECT  a.id as "account id", 
        r.id as "region id", 
        a.name as "account name", 
        r.name as "region name"
FROM accounts a
JOIN sales_reps s ON s.id = a.sales_rep_id
JOIN region r ON r.id = s.region_id;
-- AND
SELECT DISTINCT id, name FROM accounts;
-- Have any sales reps worked on more than one account?
-- All of the sales reps have worked on more than one account. The fewest number of accounts any sales rep works on is 3.
-- Using DISTINCT in the second query assures that all of the sales reps are accounted for in the first query.
SELECT s.id, s.name, COUNT(*) num_accounts FROM accounts a
JOIN sales_reps s ON s.id = a.sales_rep_id
GROUP BY s.id, s.name ORDER BY num_accounts;
-- AND
SELECT DISTINCT id, name FROM sales_reps;


-- ------------------------------------------------------------------------------------------------------------------
-- HAVING function. Useful when grouping by one or more columns.
-- ------------------------------------------------------------------------------------------------------------------
-- HAVING is the “clean” way to filter a query that has been aggregated, but this is also commonly done using a subquery. 
-- Essentially, any time you want to perform a WHERE on an element of your query that was created by an aggregate, 
-- you need to use HAVING instead.
-- HAVING appears after the GROUP BY clause, but before the ORDER BY clause whereas, 
-- WHERE comes before the GROUP BY and ORDER BY clauses.
-- The aggregation functions must be used in HAVING clause and an alias column name/index cannot be used.

-- How many of the sales reps have more than 5 accounts that they manage?
SELECT sr.name, COUNT(ac.name) AS num_accts FROM sales_reps sr
JOIN accounts ac ON sr.id = ac.sales_rep_id
GROUP BY sr.name HAVING COUNT(ac.name) > 5 ORDER BY num_accts;
-- How many accounts have more than 20 orders?
SELECT account_id, COUNT(id) AS num_orders FROM orders
GROUP BY account_id HAVING COUNT(id) > 20 
ORDER BY num_orders;
-- Which account has the most orders?
SELECT account_id, COUNT(id) AS num_orders FROM orders
GROUP BY account_id ORDER BY num_orders DESC LIMIT 1;
-- Which accounts spent more than 30,000 usd total across all orders?
SELECT account_id, SUM(total_amt_usd) AS amount FROM orders
GROUP BY account_id HAVING SUM(total_amt_usd) > 30000
ORDER BY amount; 
-- Which accounts spent less than 1,000 usd total across all orders?
SELECT account_id, SUM(total_amt_usd) AS amount FROM orders
GROUP BY account_id HAVING SUM(total_amt_usd) < 1000
ORDER BY amount;
-- Which account has spent the most with us?
SELECT account_id, SUM(total_amt_usd) AS amount FROM orders
GROUP BY account_id ORDER BY amount DESC LIMIT 1; 
-- Which account has spent the least with us?
SELECT account_id, SUM(total_amt_usd) AS amount FROM orders
GROUP BY account_id ORDER BY amount LIMIT 1; 
-- Which accounts used facebook as a channel to contact customers more than 6 times?
SELECT ac.id, we.channel, COUNT(we.channel) as num_used FROM accounts ac
JOIN web_events we ON ac.id = we.account_id
GROUP BY ac.id, we.channel
HAVING COUNT(we.channel) > 6 AND we.channel IN ('facebook')
ORDER BY num_used;
-- Which account used facebook most as a channel?
SELECT ac.id, we.channel, COUNT(we.channel) as num_used FROM accounts ac
JOIN web_events we ON ac.id = we.account_id
GROUP BY ac.id, we.channel
HAVING COUNT(we.channel) > 6 AND we.channel IN ('facebook')
ORDER BY num_used DESC LIMIT 1;
-- Which channel was most frequently used by most accounts? The udacity solution looked at the top 10 instead of 1 that I used initially.
SELECT ac.id, we.channel, COUNT(we.channel) as num_used FROM accounts ac
JOIN web_events we ON ac.id = we.account_id
GROUP BY ac.id, we.channel
ORDER BY num_used DESC LIMIT 10;


-- ------------------------------------------------------------------------------------------------------------------
-- DATE function. It is hard to group by dates in SQL because datetime values are unique down to milliseconds.
-- ------------------------------------------------------------------------------------------------------------------
-- The DATE_TRUNC() function can be used to truncate date values prior to grouping.
-- e.g. DATE_TRUNC('day', 2017-04-01 12:15:01). second, minute, hour, day, month, and year are other intervals that can be used to 
-- set truncation levels. Check https://mode.com/blog/date-trunc-sql-timestamp-function-count-on/ for additional details
-- DATE_PART() can be used to determine further granularity like day of the week, day of the month or month of the year
-- e.g. DATE_PART('day', 2017-04-01 12:15:01). `dow`-day of week, `day`-day of month, `month`-month of year
--  Additional description of datetime functions can be found https://www.postgresql.org/docs/9.1/functions-datetime.html.

-- Find the sales in terms of total dollars for all orders in each year, ordered from greatest to least. 
-- Do you notice any trends in the yearly sales totals?
-- If we look further at the monthly data, we see that for 2013 and 2017 there is only one month of sales for each of these years 
-- (12 for 2013 and 1 for 2017). Therefore, neither of these are evenly represented. Sales have been increasing year over year, 
-- with 2016 being the largest sales to date. At this rate, we might expect 2017 to have the largest sales.
SELECT DATE_PART('year', occurred_at), SUM(total_amt_usd) FROM orders
GROUP BY 1 ORDER BY 2 DESC;
-- Which month did Parch & Posey have the greatest sales in terms of total dollars? Are all months evenly represented by the dataset?
-- In order for this to be 'fair', we should remove the sales from 2013 and 2017. For the same reasons as discussed above.
SELECT DATE_PART('month', occurred_at), SUM(total_amt_usd) FROM orders
WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
GROUP BY 1 ORDER BY 2 DESC LIMIT 1;
-- Which year did Parch & Posey have the greatest sales in terms of total number of orders? Are all years evenly represented by the dataset?
SELECT DATE_PART('year', occurred_at), SUM(total) FROM orders
GROUP BY 1 ORDER BY 2 DESC LIMIT 1;
-- Which month did Parch & Posey have the greatest sales in terms of total number of orders? Are all months evenly represented by the dataset?
SELECT DATE_PART('month', occurred_at), SUM(total) FROM orders
WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
GROUP BY 1 ORDER BY 2 DESC LIMIT 1;
-- In which month of which year did Walmart spend the most on gloss paper in terms of dollars
SELECT ac.name, DATE_TRUNC('month', od.occurred_at), SUM(od.gloss_amt_usd) FROM accounts ac
JOIN orders od ON ac.id = od.account_id
WHERE ac.name='Walmart' 
GROUP BY 1, 2
ORDER BY 3 DESC 
LIMIT 1;


-- ------------------------------------------------------------------------------------------------------------------
-- CASE statements. This is a way to handle if-then logic in sql. It can also be combined with aggregating functions
-- ------------------------------------------------------------------------------------------------------------------
-- It can assign a value to rows that agree to a conditional statement into a new aliased column name.
-- Unlike WHERE statements, it can assign values to a new columnn based on multiple stipulated conditions.
-- The CASE statement always goes in the SELECT clause.
-- CASE must include the following components: WHEN, THEN, and END. ELSE is an optional component to catch cases that
-- didn’t meet any of the other previous CASE conditions.
SELECT CASE WHEN total > 500 THEN 'Over 500' 
            ELSE '500 or under' END AS total_group
       COUNT(*) AS order_count
FROM orders GROUP BY 1;
-- There are some advantages to separating data into separate columns like this depending on what you want to do, but often this level of 
-- separation might be easier to do in another programming language - rather than with SQL.

-- Write a query to display for each order, the account ID, total amount of the order, and the level of the order - 
-- ‘Large’ or ’Small’ - depending on if the order is $3000 or more, or smaller than $3000.
SELECT id, total_amt_usd, CASE WHEN total_amt_usd >= 3000 THEN 'Large' ELSE 'Small' END AS order_level
FROM orders;
-- Write a query to display the number of orders in each of three categories, based on the total number of items in each order. 
-- The three categories are: 'At Least 2000', 'Between 1000 and 2000' and 'Less than 1000'.
SELECT CASE WHEN total >= 2000 THEN 'At Least 2000'
            WHEN total >= 1000 AND total < 2000 THEN 'Between 1000 and 2000'
            ELSE 'Less than 1000' END AS categories,
       COUNT(*) 
FROM orders GROUP BY 1;
-- We would like to understand 3 different levels of customers based on the amount associated with their purchases. 
-- The top level includes anyone with a Lifetime Value (total sales of all orders) greater than 200,000 usd. 
-- The second level is between 200,000 and 100,000 usd. The lowest level is anyone under 100,000 usd. 
-- Provide a table that includes the level associated with each account. You should provide the account name, 
-- the total sales of all orders for the customer, and the level. Order with the top spending customers listed first.
SELECT ac.name, SUM(od.total_amt_usd), CASE WHEN SUM(od.total_amt_usd) > 200000 THEN 'top'
                                            WHEN SUM(od.total_amt_usd) >= 100000 AND SUM(od.total_amt_usd) < 200000 THEN 'middle'
                                            ELSE 'low' END AS levels
FROM accounts ac JOIN orders od ON ac.id = od.account_id
GROUP BY 1 ORDER BY 2 DESC;
-- We would now like to perform a similar calculation to the first, but we want to obtain the total amount spent by customers only in 2016 and 2017.
-- Keep the same levels as in the previous question. Order with the top spending customers listed first.
SELECT ac.name, SUM(od.total_amt_usd), CASE WHEN SUM(od.total_amt_usd) > 200000 THEN 'top'
                                            WHEN SUM(od.total_amt_usd) >= 100000 AND SUM(od.total_amt_usd) < 200000 THEN 'middle'
                                            ELSE 'low' END AS levels
FROM accounts ac JOIN orders od ON ac.id = od.account_id
WHERE od.occurred_at BETWEEN '2016-01-01' AND '2018-01-01'
GROUP BY 1 ORDER BY 2 DESC;
-- We would like to identify top performing sales reps, which are sales reps associated with more than 200 orders. Create a table with the sales rep name, 
-- the total number of orders, and a column with top or not depending on if they have more than 200 orders. Place the top sales people first in your final table.
SELECT sr.name, COUNT(*), CASE WHEN COUNT(*) > 200 THEN 'top' ELSE 'bottom' END AS performance
FROM sales_reps sr 
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN orders od ON ac.id = od.account_id
GROUP BY 1 ORDER BY 2 DESC;
-- The previous didn't account for the middle, nor the dollar amount associated with the sales. Management decides they want to see these characteristics represented 
-- as well. We would like to identify top performing sales reps, which are sales reps associated with more than 200 orders or more than 750000 in total sales. The 
-- middle group has any rep with more than 150 orders or 500000 in sales. Create a table with the sales rep name, the total number of orders, total sales across all orders, 
-- and a column with top, middle, or low depending on this criteria. Place the top sales people based on dollar amount of sales first in your final table. 
-- You might see a few upset sales people by this criteria!
SELECT  sr.name, 
        COUNT(*) AS num_sales, 
        SUM(od.total_amt_usd) AS amt_sales, 
        CASE WHEN COUNT(*) > 200 OR SUM(od.total_amt_usd) > 750000 THEN 'top' 
             WHEN COUNT(*) >= 150 AND COUNT(*) < 200 OR SUM(od.total_amt_usd) > 500000 THEN 'middle'
             ELSE 'low' END AS performance
FROM sales_reps sr 
JOIN accounts ac ON sr.id = ac.sales_rep_id
JOIN orders od ON ac.id = od.account_id
GROUP BY 1 ORDER BY 3 DESC;