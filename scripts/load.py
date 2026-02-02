import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión desde el .env
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def load_to_sql():
    print("Cargando datos a PostgreSQL...")
    
    # Crear conexión
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    # Leer el CSV limpio
    df = pd.read_csv('data/river_cleaned.csv')
    
    # Cargar a la tabla (reemplaza si existe)
    df.to_sql('partidos_river', engine, if_exists='replace', index=False)
    
    print("¡Carga completada exitosamente!")

if __name__ == "__main__":
    load_to_sql()