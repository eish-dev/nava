import psycopg2
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from loguru import logger
from app.core.config import settings

class DatabaseRepository:
    def create_database(self, connection_string: str) -> bool:
        """Create a new database for the organization"""
        logger.debug(f"Attempting to create database with connection: {connection_string}")
        try:
            # Create database
            if not database_exists(connection_string):
                logger.debug("Database doesn't exist, creating...")
                create_database(connection_string)

            # Create engine for the new database
            engine = create_engine(connection_string)
            
            # Import here to avoid circular imports
            from app.db.base_class import Base
            from app.db.models import user, organization_user

            # Create all tables in the new database
            logger.debug("Creating database tables")
            Base.metadata.create_all(bind=engine)

            logger.info("Successfully created database and tables")
            return True
        except Exception as e:
            logger.error(f"Error creating database: {str(e)}")
            self.cleanup_failed_database(connection_string)
            raise Exception(f"Failed to create organization database: {str(e)}")

    def cleanup_failed_database(self, connection_string: str):
        """Clean up if database creation fails"""
        db_name = connection_string.split('/')[-1]
        logger.debug(f"Starting cleanup for database: {db_name}")
        try:
            conn = psycopg2.connect(
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                host=settings.DATABASE_HOST,
                port=settings.DATABASE_PORT,
                database='postgres'
            )
            conn.autocommit = True
            cur = conn.cursor()
            
            logger.debug("Terminating existing connections")
            cur.execute("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE datname = %s AND pid <> pg_backend_pid()
            """, (db_name,))
            
            logger.debug("Dropping database")
            cur.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            
            cur.close()
            conn.close()
            logger.info(f"Successfully cleaned up database: {db_name}")
        except Exception as e:
            logger.error(f"Error in cleanup: {str(e)}")