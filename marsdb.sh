#!/bin/bash

# This script assumes that postgresql is downloaded on the machine
# and there is a postgres role named 'myprojectuser' with CREATE priveleges.


psql <<EOF
DROP DATABASE IF EXISTS myproject;
CREATE DATABASE myproject OWNER myprojectuser;
EOF

psql myproject myprojectuser <<EOF
CREATE SCHEMA minerals;
CREATE TABLE mars_sample (
ID CHAR(15),
DATA_ID CHAR(10) PRIMARY KEY NOT NULL,
SAMPLE_ID VARCHAR(20) NOT NULL,
DATE_ACCESSED TIMESTAMP,
ORIGIN VARCHAR(50),
LOCALITY VARCHAR(50),
NAME VARCHAR(25) NOT NULL,
SAMPLE_DESC VARCHAR(100),
SAMPLE_TYPE VARCHAR(25),
SAMPLE_CLASS VARCHAR(25),
SUB_CLASS VARCHAR(25),
GRAIN_SIZE VARCHAR(10),
VIEW_GEOM integer ARRAY[2],
RESOLUTION integer ARRAY[2],
REFL_RANGE integer ARRAY[2],
FORMULA VARCHAR(20),
COMPOSITION VARCHAR(100),
WAVE_LENGTH JSON,
REFLECTANCE JSON
);
