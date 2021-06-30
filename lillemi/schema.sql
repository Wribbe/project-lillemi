CREATE TABLE visit (
  id INTEGER PRIMARY KEY
  ,datetime DATETIME DEFAULT current_timestamp
  ,ip INTEGER NOT NULL
);
