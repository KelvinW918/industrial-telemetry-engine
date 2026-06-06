"""
Industrial Telemetry Simulator - Supabase SDK (no necesita psycopg2)
"""

import random
import time
from datetime import datetime
from supabase import create_client

# ============================================
# CONFIGURACIÓN SUPABASE (CREDENCIALES REALES)
# ============================================

SUPABASE_URL = "https://kbrcheplngrywgpceunt.supabase.co"

# ANON KEY (pública - segura para usar en cliente)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImticmNoZXBsbmdyeXdncGNldW50Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA3NjQ5OTAsImV4cCI6MjA5NjM0MDk5MH0.ZLy3zKWU_uDBHB2k_zaim8EI7U5WN80m15hLUIB3ynY"

# ============================================
# TIPOS DE SENSORES
# ============================================

SENSOR_TYPES = {
    'temperature': {'min': -10, 'max': 45, 'unit': '°C'},
    'pressure': {'min': 950, 'max': 1050, 'unit': 'hPa'},
    'vibration': {'min': 0, 'max': 25, 'unit': 'mm/s'},
    'humidity': {'min': 20, 'max': 90, 'unit': '%'},
    'current': {'min': 0, 'max': 150, 'unit': 'A'}
}

LOCATIONS = ['North_Plant', 'South_Plant', 'East_Wing', 'West_Wing', 'Central_Control']

def main():
    print("=" * 60)
    print("🏭 INDUSTRIAL TELEMETRY SIMULATOR (Supabase SDK)")
    print("=" * 60)
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Probar conexión con una consulta simple
        supabase.table('sensor_data').select('*').limit(1).execute()
        print("✅ Conectado a Supabase\n")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    sensors = [f"S_{i+1:04d}" for i in range(50)]
    print(f"📡 Simulando {len(sensors)} sensores\n")
    
    count = 0
    try:
        while True:
            data = []
            for sensor in sensors:
                sensor_type = random.choice(list(SENSOR_TYPES.keys()))
                config = SENSOR_TYPES[sensor_type]
                value = round(random.uniform(config['min'], config['max']), 2)
                
                data.append({
                    'time': datetime.now().isoformat(),
                    'sensor_id': sensor,
                    'sensor_type': sensor_type,
                    'value': value,
                    'unit': config['unit'],
                    'location': random.choice(LOCATIONS)
                })
            
            supabase.table('sensor_data').insert(data).execute()
            count += len(sensors)
            print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] Insertadas {len(sensors)} lecturas | Total: {count}")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n✅ Simulación detenida. Total lecturas: {count}")

if __name__ == "__main__":
    main()