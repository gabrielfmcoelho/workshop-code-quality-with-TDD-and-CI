import sqlalchemy as sa
from sqlalchemy import text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException

from .settings import DatabaseSettings


class DatabaseInterface:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, only_base: bool = False):
        """
        Initialize the database connection
        """
        if not hasattr(self, 'initialized'):
            if only_base:
                self.declarative_base = declarative_base()
            else:
                self.create_instance()
            self.initialized = True
    
    def create_instance(self):
        """
        Create a new instance of the database connector
        """
        try:
            db_configs = DatabaseSettings() # type: ignore
            self.engine = sa.create_engine(db_configs.url, echo=True)
            self.declarative_base = declarative_base()
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.test_connection()
        except Exception as e:
            raise e

    def test_connection(self, raise_exception: bool = True):
        """
        Test the database connection
        """
        try:
            with self.engine.connect() as connection:
                return True
        except Exception as e:
            if raise_exception:
                raise HTTPException(status_code=500, detail='Database connection failed')
            return False

    def get_declarative_base(self):
        """
        Get the tables registry
        """
        return self.declarative_base
    
    def get_session(self):
        """
        Get a session object
        """
        try:
            with self.SessionLocal() as session:
                yield session
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to create session object')

    def create_tables(self):
        """
        Create tables in the database
        """
        try:
            self.declarative_base.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail='Failed to create tables')
        
    def get_metadata_tables(self):
        """
        Get metadata of the tables
        """
        return self.declarative_base.metadata.tables

    def get_existing_tables(self):
        """
        Get all existing tables in the database
        """
        return inspect(self.engine).get_table_names()

    def drop_tables(self):
        """
        Drop tables from the database
        """
        try:
            self.declarative_base.metadata.drop_all(self.engine, checkfirst=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Failed to drop tables: {e}')

    def reset_tables(self):
        """
        Reset tables in the database
        """
        self.drop_tables()
        self.create_tables()

    def query_data(self, model):
        """
        Query data from the database
        """
        try:
            session = self.get_session().__next__()
            return session.query(model).all()
        except Exception as e:
            return []
            
def get_database_interface() -> DatabaseInterface:
    """
    Get the database interface, specially for dependency injection
    """
    return DatabaseInterface()