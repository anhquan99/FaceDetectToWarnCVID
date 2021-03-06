CREATE DATABASE PREDICT_COVID
USE PREDICT_COVID
CREATE TABLE PEOPLE(
	NAME VARCHAR(250) PRIMARY KEY,
	PHOTO VARCHAR(250) NOT NULL
)
CREATE TABLE PREDICTION(
	REF VARCHAR(250) NOT NULL,
	OTHER VARCHAR(250) NOT NULL,
	PREDICT_PER FLOAT NOT NULL,
	AT_TIME DATETIME NOT NULL
)
ALTER TABLE PREDICTION ADD PRIMARY KEY(REF, OTHER, AT_TIME)
ALTER TABLE PREDICTION ADD CONSTRAINT PRE_PE_REF FOREIGN KEY (REF) REFERENCES PEOPLE(NAME)
ALTER TABLE PREDICTION ADD CONSTRAINT PRE_PE_OTHER FOREIGN KEY (OTHER) REFERENCES PEOPLE(NAME)
CREATE TABLE ANALYZED_PREDICTION(
	NAME VARCHAR(250) NOT NULL,
	AT_TIME DATETIME NOT NULL,
	PERDICT_PER FLOAT NOT NULL,
	STATUS BIT NOT NULL
)	
ALTER TABLE ANALYZED_PREDICTION ADD PRIMARY KEY (NAME, AT_TIME)
ALTER TABLE ANALYZED_PREDICTION ADD CONSTRAINT AN_PE_NAME FOREIGN KEY (NAME) REFERENCES PEOPLE(NAME)
CREATE PROCEDURE findNotEffected
as
	begin 
		select Name from PEOPLE where NAME not in (select NAME from ANALYZED_PREDICTION where STATUS = 1)
	end