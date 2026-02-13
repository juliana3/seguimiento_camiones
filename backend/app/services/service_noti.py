from sqlalchemy.orm import Session
from ..models import Notificacion


def crear_notificacion(
    db: Session,
    usuario_id: int,
    tipo: str,
    titulo: str | None,
    mensaje: str | None,
    canal: str = "in_app"
):
    notificacion = Notificacion(
        usuario_id=usuario_id,
        tipo=tipo,
        titulo=titulo,
        mensaje=mensaje,
        canal=canal
    )

    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)

    return notificacion


def listar_notificaciones_usuario(db: Session, usuario_id: int):
    return (
        db.query(Notificacion)
        .filter(Notificacion.usuario_id == usuario_id)
        .order_by(Notificacion.created_at.desc())
        .all()
    )


def marcar_como_leida(db: Session, notificacion_id: int, usuario_id: int):
    notificacion = (
        db.query(Notificacion)
        .filter(
            Notificacion.notificacion_id == notificacion_id,
            Notificacion.usuario_id == usuario_id
        )
        .first()
    )

    if not notificacion:
        return None

    notificacion.leida = True # type: ignore
    db.commit()
    db.refresh(notificacion)

    return notificacion
