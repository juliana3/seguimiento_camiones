from sqlalchemy import Column, Integer, Numeric,  DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .base import Base

class PosicionGPS(Base):
    __tablename__ = "posiciones_gps"
    __table_args__ = (
            Index(
                "idx_posiciones_gps_geom",
                "ubicacion",
                postgresql_using="gist"
            ),
            Index(
                "idx_posiciones_gps_camion_fecha",
                "camion_id",
                "timestamp"
            ),
            {"schema": "db"}
    )

    gps_pos_id = Column(Integer, primary_key=True, nullable=False)

    ubicacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    velocidad = Column(Numeric) # km/h
    grados = Column(Numeric) #0 a 360
    exactitud = Column(Numeric) # metros

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    #fk
    camion_id = Column(Integer, ForeignKey("db.camiones.camion_id"), nullable=False)

    #auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


    #relaciones
    camion = relationship("Camion", back_populates="posiciones_gps")