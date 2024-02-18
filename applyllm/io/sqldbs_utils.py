from dataclasses import dataclass
import sqlalchemy, os
# import psycopg

class DBConfig:
    def __init__(self,
                 host: str="localhost",
                 user: str="postgres",
                 password: str="postgres",
                 dbname: str="postgres",
                 schema: str="public",
                 port: int = 5432,
                 use_env: bool=False,
                 **kwargs):
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_USER_PW = password
        self.DB_NAME = dbname
        self.DB_SCHEMA = schema
        if use_env:
            self.DB_HOST = self._load_env("SCIVIAS_DB_HOST")
            self.DB_USER = self._load_env("SCIVIAS_DB_USERNAME")
            self.DB_USER_PW = self._load_env("SCIVIAS_DB_PASSWORD")
            self.DB_NAME = self._load_env("SCIVIAS_DB_NAME")
            self.DB_SCHEMA = self._load_env("SCIVIAS_DB_SCHEMA")
        self.DB_PORT = port
    
    
    @classmethod
    def _load_env(clz, key: str, default = ""):
        return os.environ.get(key, default)
    
    
    def __repr__(self) -> str:
        """for program and developer obj representation also used by jupyter notebook cell"""
        return f"{self.DB_HOST}\n{self.DB_USER}\n{self.DB_USER_PW}\n{self.DB_NAME}\n{self.DB_SCHEMA}\n{self.DB_PORT}"
        
    def __str__(self):
        """for user print() function"""
        return self.__repr__()
    
    
    def to_psycopg_dic(self) -> dict:
        return {
            "dbname":  self.DB_NAME,
            "user":    self.DB_USER,
            "password": self.DB_USER_PW,
            "host":     self.DB_HOST,
            "port":  self.DB_PORT,   
        }
    
    
    def to_sqlalchemy_url(self) -> sqlalchemy.engine.url.URL:
        return sqlalchemy.URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_USER_PW,  # plain (unescaped) text
            host=self.DB_HOST,
            database=self.DB_NAME,
            port=self.DB_PORT,
        )
    

class SqlalchemyFactory:
    """Factory class for creating sqlalchemy engine
    """
    @staticmethod
    def get_sync_engine(db_config: DBConfig, DEBUG: bool=False):
        # create sync engine https://docs.sqlalchemy.org/en/20/core/engines.html
        return sqlalchemy.create_engine(db_config.to_sqlalchemy_url(), echo=DEBUG)
        
 