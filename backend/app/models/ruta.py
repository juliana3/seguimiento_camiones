from sqlalchemy import Column, Integer, String, Text, DateTime, Index, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from ..db.base import Base

class Ruta(Base):
    __tablename__ = "rutas"
    __table_args__ = (
        Index(
            "idx_ruta_geometria",
            "geometria",
            postgresql_using="gist"
        ),

         {"schema": "public"}
    )


    ruta_id = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    direccion = Column(Text)
    geometria = Column(Geometry(geometry_type='LINESTRING', srid=4326), nullable=False)
    largo_metros = Column(Integer)
    duracion_estimada_minutos = Column(Integer)
    descripcion = Column(Text)

    #fk de la zona
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

    zona = relationship("Zona", back_populates="rutas")
    reportes = relationship("Reporte", back_populates="ruta")
