from src.db.engine import execute_in_session
from datetime import datetime

# query = """
# CREATE TABLE IF NOT EXISTS test (
#     id ROWID PRIMARY KEY,
#     title TEXT,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );
# """

# query = """
# INSERT INTO test VALUES ($1,$2,$3);
# """

query = """
SELECT * FROM test;
"""

if __name__ == "__main__":
    print(execute_in_session(query))
