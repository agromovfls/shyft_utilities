DROP TABLE IF EXISTS unittest_status;
CREATE TABLE unittest_status (
  step VARCHAR(30),
  title VARCHAR(30),
  value INT,
  comment VARCHAR(250)
);