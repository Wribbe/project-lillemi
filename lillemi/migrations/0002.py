from lillemi import db

def upgrade():
  db.executescript(f"""
    BEGIN TRANSACTION;
    ALTER TABLE visit ADD COLUMN endpoint TEXT;
    COMMIT;
  """)

def downgrade():
  db.executescript("""
    BEGIN TRANSACTION;
    ALTER TABLE visit RENAME TO visit_old;
    CREATE TABLE visit (
      id INTEGER PRIMARY KEY
      ,datetime DATETIME DEFAULT current_timestamp
      ,ip INTEGER NOT NULL
    );
    INSERT INTO visit (datetime, ip) SELECT datetime, ip FROM visit_old;
    DROP TABLE visit_old;
    COMMIT;
  """)
