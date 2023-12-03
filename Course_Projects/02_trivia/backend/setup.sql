DROP DATABASE IF EXISTS trivia;
DROP DATABASE IF EXISTS trivia_test;
CREATE DATABASE trivia;
CREATE DATABASE trivia_test;
GRANT ALL PRIVILEGES ON DATABASE trivia TO student;
GRANT ALL PRIVILEGES ON DATABASE trivia_test TO student;
ALTER USER student CREATEDB;
ALTER USER student WITH SUPERUSER;