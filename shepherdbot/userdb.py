import sqlite3
import os
from dataclasses import dataclass


@dataclass
class DiscordUser:
    """ 
    Simplified discord user model with toyhou.se account attribute
    
    Parameters
    -----------
    user_name - username as shown on discord app
    user_id - user id assigned to discord user
    th_account - name of toyhou.se user account, defaults to None
    """
    user_id: int = None
    user_name: str = None
    th_account: str = None

    def __repr__(self):
        return f"DiscordUser: {str(self.__dict__)}"


class UserDBService:
    """ 
    SQL wrapper class to simplify DB interaction 

    
    Code injection through arguments not likely through discord bot 
    but... good habits; so we have qmark style instead of f-strings. 
    """
    def __init__(self):
        self.db = "users.db"
        self._initialize_db()
        self._connect()

    def _initialize_db(self):
        """ 
        Initializes a new SQLite DB if not already found and automatically inserts user table 
        """
        if not os.path.isfile("users.db"):
            print("No SQL User DB found, creating DB...")
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("""CREATE TABLE users (
                      user_id integer,
                      user_name text,
                      th_account text
                     )""")
            conn.commit()
            conn.close()
    
    def _connect(self):
        """ Connects instance to user.db and creates a cursor """
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        print(f"Connected to DB: {self.db}")

    def _commit(self):
        """ Commit all changes to the db """
        self.conn.commit()

    def close(self):
        """ Closes connection to db """
        self.conn.close()
        
    def insert(self, user_id: int, user_name: str, th_account: str):
        """ 
        Inserts user information into user db 
        """
        print(user_id, user_name, th_account)
        print(type(user_id), type(user_name), type(th_account))
        self.c.execute("""insert into users values (?, ?, ?)""", (user_id, user_name, th_account))
        self._commit()
        
    def query_username(self, user_name: str) -> DiscordUser or None:
        """ Query the DB for a specific username """
        self.c.execute(f"SELECT user_id, user_name, th_account FROM users WHERE user_name = :user", {"user": user_name})
        results = self.c.fetchone()
        if results:
            user_dict = {
                "user_id": results[0],
                "user_name": results[1],
                "th_account": results[2]
            }
            return self.build_user(user_dict)
        return

    def query_id(self, user_id: int) -> DiscordUser or None:
        """ Query the DB for a specific user_id """
        self.c.execute(f"SELECT user_id, user_name, th_account FROM users WHERE user_id = :id", {"id": user_id})
        results = self.c.fetchone()
        if results:
            user_dict = {
                "user_id": results[0],
                "user_name": results[1],
                "th_account": results[2]
            }
            return self.build_user(user_dict)
        return

    def query_toyhouse(self, th_account: str) -> DiscordUser or None:
        """ Query the DB for a specific toyhou.se account """
        self.c.execute(f"SELECT user_id, user_name, th_account FROM users WHERE th_account = :th", {"th": th_account})
        results = self.c.fetchone()
        if results:
            user_dict = {
                "user_id": results[0],
                "user_name": results[1],
                "th_account": results[2]
            }
            return self.build_user(user_dict)
        return

    def update_th_account(self, user_id: int, th_account: str):
        """ Update an existing record in the Users table """
        self.c.execute(f"UPDATE users SET th_account = :th WHERE user_id = :id", {"th": th_account, "id": user_id})

    @staticmethod
    def build_user(user_dict) -> DiscordUser:
        """ Constructs a Discorduser object from dict """
        du = DiscordUser()
        for k, v in user_dict.items():
            setattr(du, k, v)
        return du

