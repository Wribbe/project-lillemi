from lillemi import db

def upgrade():
  db.executescript(f"""
    BEGIN TRANSACTION;
    CREATE TABLE role (
      id INTEGER PRIMARY KEY
      ,name TEXT NOT NULL UNIQUE
      ,description TEXT NOT NULL
    );
    CREATE TABLE role_assignment (
      id INTEGER PRIMARY KEY
      ,user INTEGER NOT NULL
      ,role INTEGER NOT NULL
      ,FOREIGN KEY(user) REFERENCES user(id)
      ,FOREIGN KEY(role) REFERENCES role(id)
    );
    INSERT INTO role (name, description) VALUES ('admin','Administrator');
    COMMIT;
  """)

def downgrade():
  db.executescript("""
    BEGIN TRANSACTION;
    DROP TABLE role;
    DROP TABLE role_assignment;
    COMMIT;
  """)
