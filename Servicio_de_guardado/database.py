from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de PostgreSQL
DATABASE_URL = "postgresql://user:password@postgresdb/db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
