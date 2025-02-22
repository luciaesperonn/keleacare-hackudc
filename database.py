from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Crear la base de datos SQLite
DATABASE_URL = "sqlite:///./diario_emocional.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de datos con SQLAlchemy
Base = declarative_base()

# Modelo para almacenar registros del diario emocional
class DiarioEmocional(Base):
    __tablename__ = "diario"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    texto = Column(String, nullable=False)
    emocion_detectada = Column(String, nullable=False)
    score_negativo = Column(Float)
    score_neutro = Column(Float)
    score_positivo = Column(Float)
    score_compuesto = Column(Float)

# Crear las tablas en la BD
Base.metadata.create_all(bind=engine)
