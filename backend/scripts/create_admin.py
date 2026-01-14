from app.db.session import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import get_password_hash

db = SessionLocal()

email = "admin@basurapp.com"

existe = db.query(Usuario).filter(Usuario.email == email).first()
if existe:
    print("El usuario ya existe")
    exit()

usuario = Usuario(
    email=email,
    password_hash=get_password_hash("admin123"),
    nombre_completo="Admin Sistema",
    rol="admin",
    esta_activo=True,
    notificaciones_activadas=True,
)

db.add(usuario)
db.commit()
db.refresh(usuario)

print("Usuario creado:", usuario.email)
