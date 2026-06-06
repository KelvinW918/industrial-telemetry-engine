"""
Industrial Telemetry Dashboard - Visualización en tiempo real
Ejecutar: python -m streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
from supabase import create_client
import time

# ============================================
# CONFIGURACIÓN
# ============================================

SUPABASE_URL = "https://kbrcheplngrywgpceunt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImticmNoZXBsbmdyeXdncGNldW50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA3NjQ5OTAsImV4cCI6MjA5NjM0MDk5MH0.ZLy3zKWU_uDBHB2k_zaim8EI7U5WN80m15hLUIB3ynY"

# Configurar página
st.set_page_config(
    page_title="Industrial Telemetry Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1rem;
        border-radius: 1rem;
        border-left: 4px solid #38bdf8;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES
# ============================================

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data(hours=24):
    """Carga datos de las últimas N horas"""
    supabase = init_supabase()
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    
    response = supabase.table('sensor_data')\
        .select('*')\
        .gte('time', cutoff)\
        .order('time', desc=False)\
        .execute()
    
    return pd.DataFrame(response.data)

def get_latest_readings():
    """Obtiene las últimas lecturas de cada sensor"""
    supabase = init_supabase()
    
    response = supabase.table('sensor_data')\
        .select('sensor_id, sensor_type, value, unit, time, location')\
        .order('time', desc=True)\
        .limit(100)\
        .execute()
    
    df = pd.DataFrame(response.data)
    if not df.empty:
        df = df.drop_duplicates(subset=['sensor_id'], keep='first')
    return df

# ============================================
# HEADER
# ============================================

st.title("🏭 Industrial Telemetry Dashboard")
st.markdown("*Monitoreo en tiempo real de sensores industriales*")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    hours = st.slider("📅 Rango de tiempo", min_value=1, max_value=72, value=24, 
                      help="Últimas N horas")
    
    sensor_types = st.multiselect(
        "🔧 Tipos de sensor",
        options=['temperature', 'pressure', 'vibration', 'humidity', 'current'],
        default=['temperature', 'pressure', 'vibration']
    )
    
    st.markdown("---")
    st.markdown("### 📊 Estadísticas")
    
    if st.button("🔄 Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔗 Información")
    st.caption("Datos almacenados en Supabase PostgreSQL")
    st.caption(f"Conectado a: `{SUPABASE_URL.split('//')[1]}`")

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================

@st.cache_data(ttl=10)
def load_metrics():
    supabase = init_supabase()
    
    count_resp = supabase.table('sensor_data').select('*', count='exact').execute()
    total_readings = count_resp.count
    
    sensors_resp = supabase.table('sensor_data').select('sensor_id').execute()
    df_sensors = pd.DataFrame(sensors_resp.data)
    unique_sensors = df_sensors['sensor_id'].nunique() if not df_sensors.empty else 0
    
    last_resp = supabase.table('sensor_data').select('time').order('time', desc=True).limit(1).execute()
    last_update = last_resp.data[0]['time'] if last_resp.data else None
    
    return total_readings, unique_sensors, last_update

col1, col2, col3 = st.columns(3)

with col1:
    total_readings, unique_sensors, last_update = load_metrics()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_readings:,}</div>
        <div class="metric-label">📊 Total lecturas</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{unique_sensors}</div>
        <div class="metric-label">📡 Sensores activos</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if last_update:
        if last_update.endswith('Z'):
            last_update = last_update.replace('Z', '+00:00')
        last_dt = datetime.fromisoformat(last_update)
        now_aware = datetime.now(timezone.utc)
        delta = int((now_aware - last_dt).total_seconds())
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Hace {delta}s</div>
            <div class="metric-label">🕐 Última lectura</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">---</div>
            <div class="metric-label">🕐 Sin datos</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# GRÁFICOS
# ============================================

df = load_data(hours)

if not df.empty:
    df['time'] = pd.to_datetime(df['time'])
    df_filtered = df[df['sensor_type'].isin(sensor_types)]
    
    # Gráfico 1: Evolución temporal
    st.subheader("📈 Evolución de sensores")
    
    fig1 = px.line(df_filtered, 
                   x='time', 
                   y='value', 
                   color='sensor_type',
                   title=f"Valores de sensores - últimas {hours} horas",
                   labels={'value': 'Valor', 'time': 'Tiempo', 'sensor_type': 'Tipo'},
                   color_discrete_map={
                       'temperature': '#ef4444',
                       'pressure': '#3b82f6',
                       'vibration': '#f59e0b',
                       'humidity': '#10b981',
                       'current': '#8b5cf6'
                   })
    
    fig1.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Distribución de valores
    st.subheader("📊 Distribución de valores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.box(df_filtered, 
                      x='sensor_type', 
                      y='value',
                      color='sensor_type',
                      title="Distribución por tipo de sensor",
                      labels={'value': 'Valor', 'sensor_type': 'Tipo'})
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.histogram(df_filtered, 
                            x='value', 
                            color='sensor_type',
                            title="Frecuencia de valores",
                            labels={'value': 'Valor', 'count': 'Frecuencia'},
                            barmode='overlay',
                            opacity=0.7)
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Gráfico 3: Últimas lecturas por ubicación
    st.subheader("📍 Últimas lecturas por ubicación")
    
    latest = get_latest_readings()
    if not latest.empty:
        location_stats = latest.groupby(['location', 'sensor_type']).size().reset_index(name='count')
        
        fig4 = px.bar(location_stats, 
                      x='location', 
                      y='count', 
                      color='sensor_type',
                      title="Sensores activos por ubicación",
                      labels={'location': 'Ubicación', 'count': 'Cantidad', 'sensor_type': 'Tipo'})
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Tabla de últimos valores
    st.subheader("📋 Últimas lecturas por sensor")
    
    latest_display = latest.head(20)[['time', 'sensor_id', 'sensor_type', 'value', 'unit', 'location']]
    latest_display['time'] = pd.to_datetime(latest_display['time']).dt.strftime('%H:%M:%S')
    st.dataframe(latest_display, use_container_width=True)
    
else:
    st.warning("⚠️ No hay datos en el rango seleccionado. Genera datos con el simulador.")

# ============================================
# AUTO-REFRESH
# ============================================

st.markdown("---")
st.caption("🔄 Los datos se actualizan automáticamente cada 30 segundos")
time.sleep(30)
st.rerun()