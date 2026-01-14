from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Index
from geoalchemy2 import Geometry
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base import Base

class Reporte(Base):
    __tablename__ = "reportes"
    __table_args__ = (
        Index(
            "idx_reportes_fecha",
            "fecha_reporte"
        ),  
        Index(
            "idx_reportes_geom",
            "ubicacion",
            postgresql_using="gist"
        ),
        Index(
            "idx_reportes_zona_fecha",
            "zona_id",
            "fecha_reporte"
        ),


         {"schema": "public"}
    )

    reporte_id = Column(Integer, primary_key=True, nullable=False)
    ubicacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    direccion = Column(Text)
    fecha_reporte = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    #fk
    usuario_id = Column(Integer, ForeignKey("public.usuarios.usuario_id"), nullable=False)
    camion_id = Column(Integer, ForeignKey("public.camiones.camion_id"), nullable=True)
    ruta_id = Column(Integer, ForeignKey("public.rutas.ruta_id"), nullable=True)
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
    usuario = relationship("Usuario", back_populates="reportes")
    camion = relationship("Camion", back_populates="reportes")
    ruta = relationship("Ruta", back_populates="reportes")
    zona = relationship("Zona", back_populates="reportes")