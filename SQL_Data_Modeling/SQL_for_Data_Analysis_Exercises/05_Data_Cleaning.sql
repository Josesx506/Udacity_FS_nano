-- ------------------------------------------------------------------------------------------------------------------
-- LEFT, RIGHT, and LENGTH functions. Used to filter values along rows like array index filters in numpy
-- ------------------------------------------------------------------------------------------------------------------
-- Together these 3 functions can be used to mimic str.split() in python but can only be used for ordered string values.
-- LEFT pulls a specified number of characters for each row in a specified column starting at the beginning (or from the left).
-- RIGHT pulls a specified number of characters for each row in a specified column starting at the end (or from the right).
-- LENGTH provides the number of characters for each row of a specified column.
-- NOTE: When nesting functions, the innermost function is nested first.

-- In the accounts table, there is a column holding the website for each company. The last three digits specify what type of web 
-- address they are using. A list of extensions (and pricing) is provided here. Pull these extensions and provide how many of each 
-- website type exist in the accounts table.
SELECT DISTINCT RIGHT(website,3) AS type_address FROM accounts; -- This lists out all the unique website suffixes
SELECT COUNT(DISTINCT RIGHT(website,3)) FROM accounts;          -- This counts all the unique suffixes to answer the question
-- Udacity solution merges both queries above
SELECT RIGHT(website, 3) AS domain, COUNT(*) num_companies
FROM accounts
GROUP BY 1
ORDER BY 2 DESC;

-- There is much debate about how much the name (or even the first letter of a company name) matters. Use the accounts table to pull 
-- the first letter of each company name to see the distribution of company names that begin with each letter (or number).
SELECT DISTINCT LEFT(name,1) AS first_letter 
FROM accounts
ORDER BY first_letter;
-- Udacity solution returns the number of companies for each unique start value
SELECT LEFT(UPPER(name), 1) AS first_letter, COUNT(*) num_companies
FROM accounts
GROUP BY 1
ORDER BY 2 DESC;

-- Use the accounts table and a CASE statement to create two groups: one group of company names that start with a number and a second 
-- group of those company names that start with a letter. What proportion of company names start with a letter?
SELECT CASE WHEN LEFT(name, 1) BETWEEN '0' AND '9' THEN 'numeric'
            ELSE 'alphabet' END AS name_group,
            COUNT(*) AS name_count
FROM accounts
GROUP BY name_group;

-- Consider vowels as a, e, i, o, and u. What proportion of company names start with a vowel, and what percent start with anything else?
-- Using UPPER allows you to include company names that start with lower case vowels.
-- LOWER & UPPER decorators allows you to force change the case of a string.
SELECT CASE WHEN LEFT(UPPER(name), 1) IN ('A','E','I','O','U') THEN 'vowel'
            ELSE 'consonant' END AS name_group,
            COUNT(*) AS name_count
FROM accounts
GROUP BY name_group;


-- ------------------------------------------------------------------------------------------------------------------
-- POSITION, STRPOS functions. 
-- ------------------------------------------------------------------------------------------------------------------
-- Continuation of str.split() in python that can handle wildcat values. The index of the first position is 1 in SQL.
-- POSITION takes a character and a column, and provides the index where that character is for each row. POSITION(',' IN city_state).
-- STRPOS provides the same result as POSITION, but the syntax for achieving those results is a bit different as shown here: STRPOS(city_state, ',')

-- Use the accounts table to create first and last name columns that hold the first and last names for the primary_poc.
-- Extract the index of the separation space (' ')
WITH split AS (SELECT id, 
                      STRPOS(primary_poc, ' ') idx 
               FROM accounts)
-- Split the strings using the new table
SELECT ac.primary_poc, 
       LEFT(ac.primary_poc,sp.idx-1) AS first_name, 
       RIGHT(ac.primary_poc, 
             LENGTH(ac.primary_poc)-sp.idx) AS last_name
FROM accounts ac
JOIN split sp ON ac.id = sp.id;

-- Udacity solution is more efficient
SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name, 
       RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name
FROM accounts;

-- Now see if you can do the same thing for every rep name in the sales_reps table. Again provide first and last name columns.
WITH split AS (SELECT id, 
                      STRPOS(name, ' ') idx 
               FROM sales_reps)
-- Split the strings using the new table
SELECT sr.name, 
       LEFT(sr.name,sp.idx-1) AS first_name, 
       RIGHT(sr.name, 
             LENGTH(sr.name)-sp.idx) AS last_name
FROM sales_reps sr
JOIN split sp ON sr.id = sp.id;

-- Udacity solution is more efficient
SELECT LEFT(name, STRPOS(name, ' ') -1 ) first_name, 
       RIGHT(name, LENGTH(name) - STRPOS(name, ' ')) last_name
FROM sales_reps;


-- ------------------------------------------------------------------------------------------------------------------
-- CONCAT or Piping `||` functions. Can be used to merge strings from multiple columns
-- ------------------------------------------------------------------------------------------------------------------
-- e.g. CONCAT(first_name, ' ', last_name) or with 
--      piping as: first_name || ' ' || last_name

-- Each company in the accounts table wants to create an email address for each primary_poc. The email address should be the first 
-- name of the primary_poc . last name primary_poc @ company name .com.
SELECT CONCAT(LEFT(primary_poc, STRPOS(primary_poc, ' ') - 1),
              '.',
              RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')),
              '@',
              LOWER(name),
              '.com') email_address
FROM accounts;
-- Udacity solution included the names and emails
WITH t1 AS (SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name,  
                   RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name, 
                   name
            FROM accounts)
SELECT first_name, last_name, CONCAT(first_name, '.', last_name, '@', name, '.com')
FROM t1;

-- You may have noticed that in the previous solution some of the company names include spaces, which will certainly not work in an email 
-- address. See if you can create an email address that will work by removing all of the spaces in the account name, but otherwise your 
-- solution should be just as in question 1. Some helpful documentation is here.
SELECT CONCAT(LEFT(primary_poc, STRPOS(primary_poc, ' ') - 1),
              '.',
              RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')),
              '@',
              REPLACE(LOWER(name),' ','_'),
              '.com') email_address
FROM accounts;
-- Udacity solution. They used the replace function too
WITH t1 AS (SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name,  
                   RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name, 
                   name
            FROM accounts)
SELECT first_name, last_name, CONCAT(first_name, '.', last_name, '@', REPLACE(name, ' ', ''), '.com')
FROM  t1;

-- We would also like to create an initial password, which they will change after their first log in. The first password will be the first 
-- letter of the primary_poc's first name (lowercase), then the last letter of their first name (lowercase), the first letter of their last 
-- name (lowercase), the last letter of their last name (lowercase), the number of letters in their first name, the number of letters in 
-- their last name, and then the name of the company they are working with, all capitalized with no spaces.
SELECT CONCAT(LOWER(LEFT(primary_poc,1)),
              LOWER(RIGHT(LEFT(primary_poc, 
                               STRPOS(primary_poc, ' ') - 1),1)),
              LOWER(SUBSTRING(RIGHT(primary_poc, 
                                    LENGTH(primary_poc) - STRPOS(primary_poc, ' ')),1,1)),
              SUBSTRING(primary_poc,LENGTH(primary_poc),LENGTH(primary_poc)),
              LENGTH(LEFT(primary_poc, 
                          STRPOS(primary_poc, ' ') - 1)),
              LENGTH(RIGHT(primary_poc, 
                           LENGTH(primary_poc) - STRPOS(primary_poc, ' '))),
              REPLACE(UPPER(name),' ','')) passwords
FROM accounts;
-- Udacity solution created a subquery table which made the final query easier. They also included an email column and used piping for the password
WITH t1 AS (SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name,  
                   RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name, 
                   name
            FROM accounts)
SELECT  first_name, 
        last_name, 
        CONCAT(first_name, '.', last_name, '@', name, '.com') emails, 
        LEFT(LOWER(first_name), 1) || RIGHT(LOWER(first_name), 1) || LEFT(LOWER(last_name), 1) || RIGHT(LOWER(last_name), 1) || LENGTH(first_name) || LENGTH(last_name) || REPLACE(UPPER(name), ' ', '') AS passwords
FROM t1;


-- ------------------------------------------------------------------------------------------------------------------
-- TO_DATE, CAST, DATE_PART, TRIM functions. 
-- ------------------------------------------------------------------------------------------------------------------
-- TO_DATE is used to convert str_date to numbers e.g January to 1
-- CAST is used to convert formatted strings into datetime objects similar to pythons' string parser strptime().
-- CASTing can also be done by append `::` as a suffix to the query
-- DATE_PART returns a specified part of a date e.g. SELECT DATEPART(year, '2017/08/25') AS DatePartInt; where year is column name
-- TRIM removes leading and trailing spaces from a string. Similar to python strip()
-- ------------------------------------------------------------------------------------------------------------------
-- SUBSTRING function. Used to select parts of a string by index
-- ------------------------------------------------------------------------------------------------------------------
-- e.g. SUBSTRING(date,7,4) will select from the 7th to the 10th index. The 4 is to select four values ahead of 7 that include 7.

-- LEFT, RIGHT, and TRIM are all used to select only certain elements of strings, but using them to select elements of a number 
-- or date will treat them as strings for the purpose of the function

-- Write a query to look at the top 10 rows to understand the columns and the raw data in the dataset called sf_crime_data
SELECT * FROM sf_crime_data LIMIT 10;
-- The format of the original date column is mm/dd/yyyy with times that are not correct also at the end of the date.
-- Convert it to sql date time
SELECT date,(SUBSTRING(date,7,4) || '-' || SUBSTRING(date,1,2) || '-' || SUBSTRING(date,4,2) || ' ' || SUBSTRING(date,12,8))::DATE AS new_date;


-- ------------------------------------------------------------------------------------------------------------------
-- COALESCEfunction. Returns the first non-NULL value passed for each row. 
-- ------------------------------------------------------------------------------------------------------------------
-- I didn't initially understand the explanation so it was mainly udacity solutions
-- SImilar to pandas.fillna(), it can be used to replace null values in one column with a string or values from another column

-- Run the query below
SELECT *
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

-- Use COALESCE to fill in the accounts.id column where the account.id for the NULL value for the the table in 1
SELECT COALESCE(o.id, a.id) filled_id, a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, o.*
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

-- Use COALESCE to fill in the oders.account_id column with the account.id for the NULL value for the the table in 1
SELECT COALESCE(o.id, a.id) filled_id, 
       a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, 
       COALESCE(o.account_id, a.id) account_id, 
       o.occurred_at, o.standard_qty, o.gloss_qty, o.poster_qty, o.total, o.standard_amt_usd, 
       o.gloss_amt_usd, o.poster_amt_usd, o.total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

-- Use COALESCE to fill in each of the qty and usd columns with 0 for the table in 1
SELECT COALESCE(o.id, a.id) filled_id, 
       a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, 
       COALESCE(o.account_id, a.id) account_id, 
       o.occurred_at, 
       COALESCE(o.standard_qty, 0) standard_qty, 
       COALESCE(o.gloss_qty,0) gloss_qty, 
       COALESCE(o.poster_qty,0) poster_qty, 
       COALESCE(o.total,0) total, 
       COALESCE(o.standard_amt_usd,0) standard_amt_usd, 
       COALESCE(o.gloss_amt_usd,0) gloss_amt_usd, 
       COALESCE(o.poster_amt_usd,0) poster_amt_usd, 
       COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

-- Run the query in 1 with the WHERE removed and COUNT the number of ids.
SELECT COUNT(*)
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;

-- Run the query in 5 but with the COALESCE function used in question 2 through 4
SELECT COALESCE(o.id, a.id) filled_id, 
       a.name, a.website, a.lat, a.long, a.primary_poc, a.sales_rep_id, 
       COALESCE(o.account_id, a.id) account_id, 
       o.occurred_at, 
       COALESCE(o.standard_qty, 0) standard_qty, 
       COALESCE(o.gloss_qty,0) gloss_qty, 
       COALESCE(o.poster_qty,0) poster_qty, 
       COALESCE(o.total,0) total, 
       COALESCE(o.standard_amt_usd,0) standard_amt_usd, 
       COALESCE(o.gloss_amt_usd,0) gloss_amt_usd, 
       COALESCE(o.poster_amt_usd,0) poster_amt_usd, 
       COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;