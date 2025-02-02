-- Here I moved the process column into its own table so that I could create a one2many relationship between caseids and processes.
-- Hence, we can now change process name from a single row in the process table and reassign a case to a different process by changing one row from the process_case table.
BEGIN TRANSACTION;
CREATE TABLE process (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);
CREATE TABLE process_case (
	caseid INTEGER PRIMARY KEY,
	processid BIGINT
);

INSERT INTO process (name)
SELECT DISTINCT(process) AS name
	FROM processlog
;

INSERT INTO process_case(
	processid, caseid
)
SELECT DISTINCT p.id AS processid, plog.caseid AS caseid  
	FROM processlog plog JOIN process p ON plog.process = p.name;

ALTER TABLE processlog DROP COLUMN process;
COMMIT TRANSACTION;
