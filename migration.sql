/* 
  In order to run the migration:
  $ sqlite3 <db_file> < migration.sql

  e.g. using the testdata.db
  $ sqlite3 testdata.db < migration.sql

  If you don't have sqlite3 installed, you can enter the docker container of paxray-api and run the command from there
  $ docker compose up -d
  $ docker exec -it paxray-api bash
  $ sqlite3 testdata.db < migration.sql


  Problem: 
  `processlog` table contains a redundant column `process`,
  If a type of process is to be renamed, then all dependant columns
  must also be updated, which is inefficient as it requires a lot of row updates.

  Solution:
  We can extract the column `process` to an independent table.
  Such that, when a process' name must be updated, then it's enough to just update a single row on the table `process`.
  The relationship between `processlog` and `process` will be N:1 or Many:1.


  > Steps:
  (1) We can create a new table called `process`, with the following columns:
  | id      | name  |
  | INTEGER | TEXT  |
*/
CREATE TABLE IF NOT EXISTS process (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL,
  UNIQUE(name)
);

-- (2) We can populate the `process` table by gathering the distinct / unique process values from the original table `processlog`.
INSERT OR IGNORE INTO process (name)
SELECT DISTINCT process FROM processlog;

-- (3) Alter the original table `processlog`, and add a new column called `processid` with type of integer and act as a FK (Foreign Key) to table `process`.
ALTER TABLE processlog ADD COLUMN processid INTEGER REFERENCES process(id);

-- (4) In the table `processlog`, map the value of `process` to `processid` through lookup at the `name` column in `process`.
UPDATE processlog 
SET processid = (
  SELECT process.id FROM process WHERE process.name = processlog.process
);

-- (5) Drop the column `process` at table `processlog`.
ALTER TABLE processlog DROP COLUMN process;
