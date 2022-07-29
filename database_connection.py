import sqlite3
from sqlite3 import Connection, Error

class DatabaseConnection(object):
    """Singleton Class to manage connection to sqlite database."""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.instance

    def connect(self, database_url: str)-> Connection:
        """Create connection with database url.
        Args:
            database_url (str) : Database url
        Returns:
            Connection / None
                Return the database connection, None if error when trying to connect
        """
        self.__connection = None
        try:
            self.__connection = sqlite3.connect(database_url)
        except Error as e:
            print(e)
        finally:
            return self.__connection
    
    def disconnect(self)-> None:
        """Close connection to database."""
        if self.__connection:
            self.__connection.close()