from lillemi import db

def upgrade():
  db.executescript(f"""
    CREATE TABLE visit (
      id INTEGER PRIMARY KEY
      ,datetime DATETIME DEFAULT current_timestamp
      ,ip INTEGER NOT NULL
    );
    """)

def downgrade():
  db.executescript("DROP TABLE visit;")
