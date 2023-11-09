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
-- Appending Data via UNION operator.
-- ------------------------------------------------------------------------------------------------------------------
-- The UNION operator is used to combine the result sets of 2 or more SELECT statements. It removes duplicate rows between the various SELECT statements
-- Each SELECT statement within the UNION must have the same number of fields in the result sets with similar data types.
-- Typically, the use case for leveraging the UNION command in SQL is when a user wants to pull together distinct values of specified columns that are spread across multiple tables. 
For example, a chef wants to pull together the ingredients and respective aisle across three separate meals that are maintained in different tables.