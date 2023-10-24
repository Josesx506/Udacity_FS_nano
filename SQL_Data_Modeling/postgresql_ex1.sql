-- This exercise can be executed with http://sqlfiddle.com/#!17/a114f/109130
-- --------------------- Build the Schema ---------------------
-- Create the drivers table
create table drivers (
  id serial primary key,
  first_name varchar,
  last_name varchar
);
-- Create the vehicles table
create table vehicles (
  id serial primary key,
  make varchar,
  model varchar,
  driver_id integer references drivers(id)
);

-- --------------------- Perform some sample queries ---------------------
-- Create the driver table
INSERT INTO drivers (id,first_name, last_name) VALUES (1, 'Amy', 'Hua');
INSERT INTO drivers (id,first_name, last_name) VALUES (2,'Koshi', 'Kawasaki');
INSERT INTO drivers (id,first_name, last_name) VALUES (3,'Joel', 'Batoo');
INSERT INTO drivers (id,first_name, last_name) VALUES (4,'Sarah', 'Zelda');
-- Create the vehicles table
INSERT INTO vehicles (driver_id,make, model) VALUES (1,'Ford','Escape');
INSERT INTO vehicles (driver_id,make, model) VALUES (2,'Jeep','Wrangler');
INSERT INTO vehicles (driver_id,make, model) VALUES (3,'Toyota','Prius');
INSERT INTO vehicles (driver_id,make, model) VALUES (4,'Chevy','Bronco');
-- Select all driver records; select all vehicle records; select only 3 vehicle records (using LIMIT)
SELECT * from drivers;
SELECT * from vehicles;
SELECT * from vehicles LIMIT 3;
-- Driver with ID 2 no longer owns any vehicles. Update the database to reflect this.
DELETE FROM vehicles where vehicles.driver_id  = 2;
-- Driver with ID 1 now owns a new vehicle in addition to the previous one they owned. Update the database to reflect this.
INSERT INTO vehicles (driver_id,make, model) VALUES (1,'Subaru','Forester');


-- --------------------- Joins & Group Bys ---------------------
-- Select all vehicles owned by driver with ID 3.
SELECT vehicles.*
FROM vehicles, drivers
WHERE drivers.id = 3 and vehicles.driver_id = 3;
-- Select all vehicles owned by driver with name 'Sarah' (without knowing their ID).
SELECT vehicles.*
FROM vehicles, drivers
WHERE drivers.first_name = 'Sarah' and drivers.id = vehicles.driver_id;
-- Show a table of the number of vehicles owned per driver.
SELECT count(*)
FROM vehicles, drivers
WHERE drivers.id = vehicles.driver_id GROUP BY drivers.id;
-- Show the number of drivers that own a Toyota model.
SELECT count(*)
FROM vehicles, drivers
WHERE drivers.id =  vehicles.driver_id  and vehicles.make = 'Toyota';


-- --------------------- Structuring Data ---------------------
-- Add information about vehicle color.
ALTER TABLE vehicles
ADD color varchar;
-- Update all existing vehicle records to have a vehicle color.
update vehicles set color = 'red';
-- Add contact information (email, address) to the driver's table.
ALTER TABLE drivers
ADD email varchar;
ALTER TABLE drivers
ADD address varchar;

-- --------------------- Challenges ---------------------
-- Using Timestamps - https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-timestamp/
-- Update vehicles table to show the date of registration information. 
-- Hint:
-- timestamp: a timestamp without timezone one.
-- timestamptz: timestamp with a timezone.
ALTER TABLE vehicles
ADD reg_dt TIMESTAMP;
-- set the time zone of the database server to  America/Los_Angeles
SET timezone = 'America/Los_Angeles';
--  Add the timezone columns info
UPDATE vehicles
SET reg_dt = '2022-11-12 09:20:25-07' where make = 'Ford' and driver_id = 1;
UPDATE vehicles
SET reg_dt = '2022-12-23 16:14:21-07' where make = 'Subaru' and driver_id = 1;
UPDATE vehicles
SET reg_dt = '2023-01-02 09:26:23-07' where make = 'Toyota' and driver_id = 3;
UPDATE vehicles
SET reg_dt = '2023-05-28 12:38:45-07' where make = 'Chevy' and driver_id = 4;


-- Get the current time
SELECT NOW();
-- SELECT TIMEOFDAY(); -- Only works with timestampz that have specified timezones
-- SELECT CURRENT_TIMESTAMP; -- similar to now

/* The DMV is looking to notify all drivers with a vehicle that needs their 
registration renewed in the next month. If vehicles need to renew their 
vehicles once every year after their date of registration, then write a query 
to fetch all drivers with at least 1 vehicle that has an upcoming renewal in
the next month, fetching their contact information as well as information 
about which vehicles need renewals. The DMV would like to run this query 
every time they need to contact all drivers that have an upcoming renewal in 
the next month. */
ALTER TABLE vehicles
ADD elapsed_time interval;
update vehicles set elapsed_time = NOW() - vehicles.reg_dt;

-- Get the vehicles table
SELECT * from vehicles;