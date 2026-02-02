# ⚪🔴 River Plate Analytics Dashboard ⚪🔴

Este proyecto es un dashboard de análisis de datos interactivo construido con Python (Streamlit), SQL y Docker, enfocado en seguir el rendimiento del Club Atlético River Plate durante la temporada 2026.

La aplicación web presenta datos detallados sobre los partidos, resultados, y estadísticas clave, proporcionando una visión completa del desempeño del equipo en las diferentes competiciones.

## ✨ Características Principales

- **Visualización de Calendario:** Muestra los próximos partidos y los ya jugados, organizados por competición (Liga Profesional, Copa Argentina, Amistosos, etc).
- **Resultados con Semáforo:** Utiliza un sistema de colores (verde para victoria, amarillo para empate, rojo para derrota) para una rápida identificación de los resultados.
- **Análisis Estadístico:**
  - **Puntos por Torneo:** Métricas que resumen los puntos obtenidos en cada competición.
  - **Distribución de Resultados:** Gráficos de torta y barras que muestran el porcentaje y la cantidad de victorias, empates y derrotas.
  - **KPIs de Rendimiento:** Métricas como el promedio de goles a favor y la cantidad de partidos con valla invicta.
- **ETL Integrado:** Un botón en la barra lateral permite ejecutar un proceso de **Extract, Transform, Load (ETL)** para actualizar los datos desde la fuente original mediante web scraping.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python
- **Dashboard:** Streamlit
- **Base de Datos:** PostgreSQL
- **Contenerización:** Docker & Docker Compose
- **Web Scraping:** BeautifulSoup y Requests
- **Análisis de Datos:** Pandas
- **Visualización de Datos:** Plotly Express

## 🚀 Cómo Empezar

Para ejecutar este proyecto en tu entorno local, necesitarás tener Docker instalado.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/river-plate-analytics.git
cd river-plate-analytics
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto, basándote en el archivo `.env.template` o usando la siguiente plantilla. Estos valores deben coincidir con los de `docker-compose.yml`.

```env
DB_HOST=db
DB_NAME=river_plate_db
DB_USER=postgres
DB_PASSWORD=admin123
DB_PORT=5432
```

### 3. Levantar los Contenedores

Desde la raíz del proyecto, ejecuta el siguiente comando para construir y levantar los servicios de la base de datos y el dashboard:

```bash
docker-compose up --build
```

- El servicio de la base de datos PostgreSQL estará disponible en el puerto `5432`.
- El dashboard de Streamlit será accesible desde tu navegador en **http://localhost:8501**.

##  Uso

1.  **Accede al Dashboard:** Abre tu navegador y ve a `http://localhost:8501`.
2.  **Actualiza los Datos:** Al ser la primera vez que ejecutas la aplicación, la base de datos estará vacía. Haz clic en el botón **🚀 Actualizar Datos (ETL)** en la barra lateral izquierda para iniciar el proceso de web scraping y poblar la base de datos.
3.  **Explora los Datos:** Una vez que los datos estén cargados, podrás navegar por las pestañas "📅 AGENDA POR COMPETICIÓN" y "📊 ANÁLISIS ESTADÍSTICO" para explorar el rendimiento del equipo.

## 📂 Estructura del Proyecto

```
/river-plate-analytics
├── .env                # Archivo para variables de entorno (no versionado)
├── .gitignore          # Archivos y carpetas ignorados por Git
├── Dockerfile          # Define la imagen de Docker para la app de Streamlit
├── README.md           # Documentación del proyecto
├── data/               # (Opcional) Almacenamiento de datos crudos o procesados
├── docker-compose.yml  # Orquesta los servicios de la base de datos y el dashboard
├── main.py             # Script principal de la aplicación Streamlit
├── requirements.txt    # Dependencias de Python
├── scripts/
│   ├── extract.py      # Módulo para extraer datos (web scraping)
│   ├── transform.py    # Módulo para transformar los datos extraídos
│   └── load.py         # Módulo para cargar los datos en la base de datos
└── sql/
    └── init_db.sql     # Script SQL para inicializar la estructura de la tabla
```
