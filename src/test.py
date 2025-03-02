import sqlite3


if __name__ == "__main__":
    con = sqlite3.connect("mini_chat.db")
    con.execute("DROP TABLE new_account")