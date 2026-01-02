from sqlalchemy import Column, Integer, Text, Boolean, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from .base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint(
            "rol IN ('publico', 'registrado', 'admin', 'superadmin')",
            name="cns_usuario_rol"
        ),
        {"schema": "db"}
    )

    #identidad del usuraio
    usuario_id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)

    # Auth
    auth_provider = Column( 
        String(20),
        nullable=False,
        default="local"  # local | google
    )

    google_id = Column(
        Text,
        unique=True,
        nullable=True
    )

    password_hash = Column(
        Text,
        nullable=True
    )

    #info personal
    nombre_completo = Column(Text)
    direccion_guardada = Column(Text)
    ubicacion_guardada = Column(Geometry(geometry_type='POINT', srid=4326))

    #estado / permisos
    rol = Column(String(20), nullable=False, default="publico")
    esta_activo = Column(Boolean, default=True)
    notificaciones_activadas = Column(Boolean, default=True)

    #auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    #relaciones
    notificaciones = relationship("Notificacion", back_populates="usuario")
    reportes = relationship("Reporte", back_populates="usuario")