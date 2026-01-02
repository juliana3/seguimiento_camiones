#app princilal 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# IMPORTAR TODOS LOS MODELOS
#from app.models import user, truck, zone, route, gps_position, report, notification, schedule





app = FastAPI(title="API sistema de seguimiento de camiones recolectores de basura", version="0.1.0")

#configuracion CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #ahora permite todos los origenes pero en prod restringir a la url del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    db_info = settings.DATABASE_URL.split("@")[-1]  # Obtener la parte después de '@'
    return {"status": "todo ok", "db_info": db_info}