from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"
    __table_args__ = (
         {"schema": "public"}
    )

    notificacion_id = Column(Integer, primary_key=True, nullable=False)
    tipo = Column(String(50), nullable=False)
    titulo = Column(Text)
    mensaje = Column(Text)

    #verificaciones
    canal = Column(String(20), nullable=False)  # push | in_app
    leida = Column(Boolean, default=False)


    #fk
    usuario_id = Column(Integer, ForeignKey("public.usuarios.usuario_id"), nullable=False)

    #auditoria

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    #relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")