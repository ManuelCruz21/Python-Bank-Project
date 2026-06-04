import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ContaDB(Base):
    __tablename__ = "contas"
    numero = Column(String(50), primary_key=True)
    titular = Column(String(100), nullable=False)
    saldo = Column(Numeric(15, 2), default=0.00, nullable=False)

class MovimentoDB(Base):
    __tablename__ = "movimentos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conta_numero = Column(String(50), ForeignKey("contas.numero", ondelete="CASCADE"))
    tipo = Column(String(50), nullable=False)
    valor = Column(Numeric(15, 2), nullable=False)
    data = Column(DateTime, nullable=False)
    descricao = Column(String(255), default="")
    conta_destino = Column(String(50), nullable=True)