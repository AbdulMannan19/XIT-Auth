import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DRIVER = "ODBC Driver 18 for SQL Server"
ENCRYPT = "yes"
TRUST_SERVER_CERTIFICATE = "no"

class DatabasePool:
    def __init__(self):
        self.engines = {
            'dev': self._create_engine('DEV'),
            'qa': self._create_engine('QA')
        }
    
    def _create_engine(self, prefix):
        server = os.getenv(f'{prefix}_DB_SERVER')
        database = os.getenv(f'{prefix}_DB_NAME')
        username = os.getenv(f'{prefix}_DB_USER')
        password = os.getenv(f'{prefix}_DB_PASSWORD')
        timeout = os.getenv('DB_CONNECTION_TIMEOUT', '30')
        pool_size = int(os.getenv('DB_POOL_SIZE', '5'))
        max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '10'))
        
        conn_str = (
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt={ENCRYPT};"
            f"TrustServerCertificate={TRUST_SERVER_CERTIFICATE};"
            f"Connection Timeout={timeout};"
        )
        
        return create_engine(
            f"mssql+pyodbc:///?odbc_connect={conn_str}",
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True
        )
    
    def get_engine(self, db_name):
        return self.engines.get(db_name)

def list_tables(pool, db_name):
    engine = pool.get_engine(db_name)
    
    query = text("""
        SELECT TABLE_SCHEMA, TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        tables = result.fetchall()
        
        print(f"\n{db_name.upper()} - {len(tables)} tables:")
        for schema, table in tables:
            print(f"  {schema}.{table}")

if __name__ == "__main__":
    pool = DatabasePool()
    
    list_tables(pool, 'dev')
    list_tables(pool, 'qa')
