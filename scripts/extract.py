import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

def extract_river_scraping():
    print("🚀 Iniciando scraping de Resultados-Futbol...")
    url = "https://www.resultados-futbol.com/equipo/partidos/ca-river-plate/2026"
    
    # User-Agent para evitar que la web nos bloquee
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        partidos = []
        # Buscamos cada bloque de competición (Apertura, Copa Argentina, etc.)
        bloques_liga = soup.select('div.liga')

        for bloque in bloques_liga:
            # Extraer nombre de la competición desde el título del bloque
            titulo_tag = bloque.select_one('div.title a')
            if not titulo_tag:
                continue
            nombre_competicion = titulo_tag.get_text(strip=True)

            # Buscamos todas las filas de partidos dentro de este bloque
            filas = bloque.select('table.tablemarcador tbody tr')

            for fila in filas:
                try:
                    # 1. Extraer Fecha (ej: "24 Ene 26")
                    fecha_raw = fila.select_one('td.time').get_text(strip=True)
                    
                    # 2. Extraer Equipos
                    local = fila.select_one('td.team-home').get_text(strip=True)
                    visitante = fila.select_one('td.team-away').get_text(strip=True)
                    
                    # 3. Extraer Marcador / Resultado
                    marcador_tag = fila.select_one('div.marker_box')
                    if not marcador_tag:
                        continue
                    marcador_raw = marcador_tag.get_text(strip=True)

                    g_river = None
                    g_rival = None
                    horario = "00:00" # Por defecto
                    resultado = "Pendiente"

                    # Si el marcador tiene un guion, es un resultado final (ej: "1-0")
                    if '-' in marcador_raw:
                        goles = marcador_raw.split('-')
                        g1 = goles[0].strip()
                        g2 = goles[1].strip()
                        
                        if "River Plate" in local:
                            g_river, g_rival = g1, g2
                        else:
                            g_rival, g_river = g1, g2
                        
                        # Determinar si ganó, perdió o empató
                        if g_river.isdigit() and g_rival.isdigit():
                            if int(g_river) > int(g_rival): 
                                resultado = "Ganó"
                            elif int(g_river) < int(g_rival): 
                                resultado = "Perdió"
                            else: 
                                resultado = "Empató"
                    else:
                        # Si no hay guion, el marcador suele ser la hora (ej: "21:00")
                        if ':' in marcador_raw:
                            horario = marcador_raw.strip()
                    partidos.append({
                        "fecha": fecha_raw,
                        "competicion": nombre_competicion,
                        "local": local,
                        "visitante": visitante,
                        "g_river": g_river,
                        "g_rival": g_rival,
                        "resultado_final": resultado,
                        "horario": horario  # <--- ESTA LÍNEA ES CLAVE
                    })
                except Exception:
                    continue

        # Crear DataFrame
        df_final = pd.DataFrame(partidos)
        
        # --- PASO CRUCIAL PARA EL TRANSFORM ---
        # Guardamos el archivo JSON que el script de transform.py va a buscar
        os.makedirs('data', exist_ok=True)
        df_final.to_json('data/river_raw_data.json', orient='records', force_ascii=False)
        
        print(f"✅ Scraping finalizado. {len(df_final)} partidos guardados en JSON.")
        return df_final

    except Exception as e:
        print(f"❌ Error en el scraping: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    extract_river_scraping()