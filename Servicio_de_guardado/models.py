from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Progreso(Base):
    __tablename__ = "progresos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(String, index=True)
    id_nivel = Column(String, index=True)
    estado = Column(JSON)
    fecha_guardado = Column(DateTime, default=datetime.utcnow)
