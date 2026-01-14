from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base import Base

class Camion(Base):
    __tablename__ = "camiones"
    __table_args__ = (
         {"schema": "public"}
    )

    camion_id = Column(Integer, primary_key=True, nullable=False)
    patente = Column(String(20), unique=True, nullable=False)
    esta_activo = Column(Boolean, default=True) 

    #fk 
    zona_id = Column(Integer, ForeignKey("public.zonas.zona_id"), nullable=False)

    #auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    #relaciones
    zona = relationship("Zona", back_populates="camiones")
    posiciones_gps = relationship("PosicionGPS", back_populates="camion", cascade="all, delete-orphan")
    reportes = relationship("Reporte", back_populates="camion")
