from lillemi import db

def upgrade():
  db.executescript(f"""
    BEGIN TRANSACTION;
    CREATE TABLE user (
      id INTEGER PRIMARY KEY
      ,name TEXT NOT NULL UNIQUE
      ,secret TEXT NOT NULL UNIQUE
    );
    COMMIT;
  """)

def downgrade():
  db.executescript("""
    BEGIN TRANSACTION;
    DROP TABLE user;
    COMMIT;
  """)
