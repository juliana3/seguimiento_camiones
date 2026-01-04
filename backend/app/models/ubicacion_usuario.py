from sqlalchemy import (
    Column, Integer, Text, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from .base import Base


class UbicacionUsuario(Base):
    __tablename__ = "ubicaciones_usuario"
    __table_args__ = (
        Index(
            "idx_ubicaciones_usuario_geom",
            "ubicacion",
            postgresql_using="gist"
        ),
        Index(
            "idx_ubicaciones_usuario_usuario",
            "usuario_id"
        ),
        {"schema": "db"}
    )

    ubicacion_usuario_id = Column(Integer, primary_key=True)

    nombre = Column(
        Text,
        nullable=False  # "Casa", "Trabajo"
    )

    direccion_texto = Column(Text)

    ubicacion = Column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False
    )

    es_principal = Column(Boolean, default=False)

    # FK
    usuario_id = Column(
        Integer,
        ForeignKey("db.usuarios.usuario_id"),
        nullable=False
    )

    zona_id = Column(
        Integer,
        ForeignKey("db.zonas.zona_id"),
        nullable=False
    )

    # auditoría
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # relaciones
    usuario = relationship("Usuario", back_populates="ubicaciones")
    zona = relationship("Zona")
