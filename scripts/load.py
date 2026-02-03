import pandas as pd
from sqlalchemy import create_engine
from config import get_db_url

def load_to_sql():
    print("Cargando datos a PostgreSQL...")
    
    # Crear conexión usando la URL centralizada
    engine = create_engine(get_db_url())
    
    # Leer el CSV limpio
    df = pd.read_csv('data/river_cleaned.csv')
    
    # Cargar a la tabla (reemplaza si existe)
    df.to_sql('partidos_river', engine, if_exists='replace', index=False)
    
    print("¡Carga completada exitosamente!")

if __name__ == "__main__":
    load_to_sql()