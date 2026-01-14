from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from ..db.base import Base

class Zona(Base):
    __tablename__ = "zonas"
    __table_args__ = (
        Index(
            "idx_zona_geometria",
            "geometria",
            postgresql_using="gist"
        ),
         {"schema": "public"}
    )

    zona_id = Column(Integer, primary_key=True, nullable=False)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    geometria = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=False)

    color = Column(String(7), nullable=True, default="#FF5733")  


    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)


    #relaciones
    rutas = relationship("Ruta", back_populates="zona")
    camiones = relationship("Camion", back_populates="zona")
    horarios = relationship("Horario", back_populates="zona", cascade="all, delete-orphan")
    reportes = relationship("Reporte", back_populates="zona")


