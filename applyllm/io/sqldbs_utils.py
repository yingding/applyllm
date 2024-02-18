from dataclasses import dataclass
import sqlalchemy, os

# import psycopg


class SqlDBConfig:
    def __init__(
        self,
        host: str = "localhost",
        user: str = "postgres",
        password: str = "postgres",
        dbname: str = "postgres",
        schema: str = "public",
        port: int = 5432,
    ):
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_USER_PW = password
        self.DB_NAME = dbname
        self.DB_SCHEMA = schema
        self.DB_PORT = port

    @classmethod
    def load_env(clz, key: str, default=""):
        return os.environ.get(key, default)

    def __repr__(self) -> str:
        """for program and developer obj representation also used by jupyter notebook cell"""
        return f"{self.DB_HOST}\n{self.DB_USER}\n{self.DB_USER_PW}\n{self.DB_NAME}\n{self.DB_SCHEMA}\n{self.DB_PORT}"

    def __str__(self):
        """for user print() function"""
        return self.__repr__()

    def to_psycopg_dic(self) -> dict:
        return {
            "dbname": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_USER_PW,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
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


class SqlDBHelperFactory:
    """Factory class for creating sqlalchemy engine"""

    @staticmethod
    def get_sync_engine(
        db_config: SqlDBConfig, verbose: bool = False
    ) -> sqlalchemy.engine.base.Engine:
        # create sync engine https://docs.sqlalchemy.org/en/20/core/engines.html
        return sqlalchemy.create_engine(db_config.to_sqlalchemy_url(), echo=verbose)

    @staticmethod
    def get_db_config_from_env(
        host_key: str = "SCIVIAS_DB_HOST",
        user_key: str = "SCIVIAS_DB_USERNAME",
        password_key: str = "SCIVIAS_DB_PASSWORD",
        db_key: str = "SCIVIAS_DB_NAME",
        schema_key: str = "SCIVIAS_DB_SCHEMA",
        port_key: str = "SCIVIAS_DB_PORT",
    ) -> SqlDBConfig:
        return SqlDBConfig(
            host=SqlDBConfig.load_env(host_key),
            user=SqlDBConfig.load_env(user_key),
            password=SqlDBConfig.load_env(password_key),
            dbname=SqlDBConfig.load_env(db_key),
            schema=SqlDBConfig.load_env(schema_key),
            port=int(SqlDBConfig.load_env(port_key, "5432")),
        )
