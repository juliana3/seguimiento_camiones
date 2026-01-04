from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Definimos los metadatos especificando el esquema "db"
metadata = MetaData(schema="db")

# Pasamos esos metadatos a la clase base
Base = declarative_base(metadata=metadata)
