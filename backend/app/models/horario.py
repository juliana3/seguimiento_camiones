from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Time, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Horario(Base):
    __tablename__ = "horarios"
    __table_args__ = (
        CheckConstraint(
            "dia_semana BETWEEN 0 AND 6",
            name="cns_horarios_dia_semana"
        ),
        CheckConstraint(
            "tipo_residuo IN (1, 2)",
            name="cns_horarios_tipo_residuo"
        ),
        UniqueConstraint(
            "zona_id",
            "dia_semana",
            "tipo_residuo",
            name="unq_horarios_zona_dia_residuo"
        ),
        {"schema": "db"}
    )


    horario_id = Column(Integer, primary_key=True, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    dia_semana = Column(SmallInteger, nullable=False)  # 0=Domingo, 6=Sábado
    tipo_residuo = Column(SmallInteger, nullable=False) #1 humedo, 2 seco


    #fk
    zona_id = Column(Integer, ForeignKey("db.zonas.zona_id"), nullable=False)

    #auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    #relaciones
    zona = relationship("Zona", back_populates="horarios")

    
