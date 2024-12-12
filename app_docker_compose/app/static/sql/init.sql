-- database and table names are acquired from env variables
CREATE DATABASE IF NOT EXISTS `default`;
USE `default`;

-- create PERSON table
CREATE TABLE IF NOT EXISTS person (
    ID INT NOT NULL,

    name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    country VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    org VARCHAR(255) NOT NULL,

    PRIMARY KEY (ID)
);

-- create ATTENDANCE table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT NOT NULL,  -- unique ID for each attendance record
    person_id INT NOT NULL,                     -- references the person table
    date DATE NOT NULL,                         -- date of attendance
    time TIME NOT NULL,                         -- time of attendance
    status VARCHAR(50) NOT NULL,                -- e.g., 'present', 'absent', 'late', etc.
    PRIMARY KEY (attendance_id),
    FOREIGN KEY (person_id) REFERENCES person(ID) -- ensures person exists in person table
);
