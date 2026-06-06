# 🏭 Industrial Telemetry Engine
[![Tests](https://github.com/KelvinW918/industrial-telemetry-engine/actions/workflows/test.yml/badge.svg)](https://github.com/KelvinW918/industrial-telemetry-engine/actions/workflows/test.yml)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.24-3F4F75?style=for-the-badge&logo=plotly)
![Status](https://img.shields.io/badge/Status-Live-00ff88?style=for-the-badge)

**Sistema completo de telemetría industrial para monitoreo de sensores en tiempo real**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://industrial-telemetry-engine-kelvinw918.streamlit.app/)

</div>

---

## 🎯 ¿Qué es este proyecto?

Un **sistema de telemetría industrial** que simula 50+ sensores (temperatura, presión, vibración, humedad, corriente) enviando datos a una base de datos PostgreSQL en la nube (Supabase), con un **dashboard analítico en tiempo real**.

### Demo en vivo
👉 [industrial-telemetry-engine-kelvinw918.streamlit.app](https://industrial-telemetry-engine-kelvinw918.streamlit.app/)

---

## 🏗️ Arquitectura del sistema
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Simulador │────▶│ Supabase │────▶│ Dashboard │
│ (Python) │ │ (PostgreSQL) │ │ (Streamlit) │
│ │ │ │ │ │
│ • 50 sensores │ │ • Almacenamiento│ │ • Métricas │
│ • Datos cada 1s │ │ • Índices │ │ • Gráficos │
│ • 5 tipos │ │ • Time-series │ │ • Tablas │
└─────────────────┘ └─────────────────┘ └─────────────────┘

text

---

## 📊 Dashboard Features

| Feature | Descripción |
|---------|-------------|
| **📈 Evolución temporal** | Gráfico de líneas con valores por tipo de sensor |
| **📊 Distribución de valores** | Boxplot + histograma interactivo |
| **📍 Sensores por ubicación** | Barras con cantidad de sensores activos |
| **📋 Últimas lecturas** | Tabla actualizada con los últimos valores |
| **🔄 Auto-refresh** | Datos actualizados cada 30 segundos |

### Métricas en tiempo real

| Métrica | Descripción |
|---------|-------------|
| Total lecturas | Cantidad acumulada de registros |
| Sensores activos | Número de sensores únicos |
| Última lectura | Tiempo desde la última actualización |

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| **Base de datos** | Supabase (PostgreSQL) | Almacenamiento de series temporales |
| **Simulador** | Python + psycopg2 | Generación de datos IoT |
| **Dashboard** | Streamlit + Plotly | Visualización interactiva |
| **Despliegue** | Streamlit Cloud | Hosting gratuito |

---

## 🚀 Ejecutar localmente

### Requisitos previos
- Python 3.11+
- Cuenta gratuita en [Supabase](https://supabase.com)

### Paso a paso

```bash
# 1. Clonar repositorio
git clone https://github.com/KelvinW918/industrial-telemetry-engine.git
cd industrial-telemetry-engine

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (crear .env)
echo SUPABASE_URL=tu_url > .env
echo SUPABASE_KEY=tu_key >> .env

# 5. Ejecutar simulador (genera datos)
python generator/sensor_simulator.py

# 6. Ejecutar dashboard (en otra terminal)
streamlit run dashboard/app.py
📁 Estructura del proyecto
text
industrial-telemetry-engine/
├── dashboard/
│   └── app.py              # Dashboard Streamlit
├── generator/
│   └── sensor_simulator.py # Generador de datos IoT
├── requirements.txt        # Dependencias Python
├── runtime.txt             # Versión Python
├── .env                    # Variables de entorno (no se sube)
└── README.md               # Documentación
📊 Base de datos (Supabase)
Esquema de la tabla sensor_data
sql
CREATE TABLE sensor_data (
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    sensor_type VARCHAR(20) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    location VARCHAR(100)
);

-- Índices para consultas rápidas
CREATE INDEX idx_sensor_time ON sensor_data (sensor_id, time DESC);
CREATE INDEX idx_time ON sensor_data (time DESC);
Ejemplo de queries analíticas
sql
-- Promedio por tipo de sensor en la última hora
SELECT sensor_type, AVG(value) as avg_value
FROM sensor_data
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY sensor_type;

-- Últimas 10 lecturas de cada sensor
SELECT DISTINCT ON (sensor_id) 
    sensor_id, time, value
FROM sensor_data
ORDER BY sensor_id, time DESC;
📈 Datos simulados
Tipo de sensor	Rango	Unidad
🌡️ Temperatura	-10°C a 45°C	°C
🔧 Presión	950 a 1050	hPa
📳 Vibración	0 a 25	mm/s
💧 Humedad	20% a 90%	%
⚡ Corriente	0 a 150	A
🔮 Hoja de ruta
Conexión a TimescaleDB para series temporales optimizadas

Alertas en tiempo real (umbrales configurables)

Exportación de datos (CSV, JSON)

Autenticación de usuarios

Historial de eventos (logs de sensores)

👤 Autor
Kelvin W.
Systems Engineer · Product Architect

https://img.shields.io/badge/GitHub-KelvinW918-181717?style=flat-square&logo=github
https://img.shields.io/badge/LinkedIn-kelvin--williams-0A66C2?style=flat-square&logo=linkedin

📄 Licencia
MIT — Libre para uso, modificación y distribución.

<div align="center"> ⭐ Si este proyecto te es útil, dale una estrella ⭐ </div> ```
