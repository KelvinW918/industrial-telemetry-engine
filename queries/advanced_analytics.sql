-- ============================================
-- ADVANCED ANALYTICS QUERIES
-- Demostración del poder de TimescaleDB
-- ============================================

-- 1. COMPARATIVA DE PERFORMANCE
-- PostgreSQL standard vs TimescaleDB

-- Standard PostgreSQL (sin hypertable)
-- Tiempo estimado: ~45 segundos en 100M rows
/*
SELECT 
    date_trunc('hour', time) as hour,
    sensor_type,
    AVG(value) as avg_value
FROM sensor_data
WHERE time > NOW() - INTERVAL '30 days'
GROUP BY hour, sensor_type;
*/

-- TimescaleDB optimizado (con hypertable)
-- Tiempo estimado: ~0.3 segundos
SELECT 
    time_bucket('1 hour', time) as hour,
    sensor_type,
    AVG(value) as avg_value
FROM sensor_data
WHERE time > NOW() - INTERVAL '30 days'
GROUP BY hour, sensor_type;

-- 2. DETECCIÓN DE ANOMALÍAS EN TIEMPO REAL
-- Identificar sensores con valores fuera de rango

WITH stats AS (
    SELECT 
        sensor_id,
        AVG(value) as mean,
        STDDEV(value) as stddev
    FROM sensor_data
    WHERE time > NOW() - INTERVAL '1 hour'
    GROUP BY sensor_id
)
SELECT 
    s.sensor_id,
    s.time,
    s.value,
    st.mean,
    st.stddev,
    CASE 
        WHEN ABS(s.value - st.mean) > 3 * st.stddev THEN 'CRITICAL'
        WHEN ABS(s.value - st.mean) > 2 * st.stddev THEN 'WARNING'
        ELSE 'NORMAL'
    END as anomaly_level
FROM sensor_data s
JOIN stats st ON s.sensor_id = st.sensor_id
WHERE s.time > NOW() - INTERVAL '10 minutes'
ORDER BY anomaly_level DESC;

-- 3. ANÁLISIS DE TENDENCIAS POR HORA DEL DÍA
SELECT 
    EXTRACT(HOUR FROM time) as hour_of_day,
    sensor_type,
    AVG(value) as avg_value,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY value) as p95
FROM sensor_data
WHERE time > NOW() - INTERVAL '7 days'
GROUP BY hour_of_day, sensor_type
ORDER BY hour_of_day;

-- 4. EFICIENCIA DE COMPRESIÓN
SELECT 
    hypertable_name,
    compression_enabled,
    compression_status,
    compressed_total_bytes,
    uncompressed_total_bytes,
    round(100 - (compressed_total_bytes::float / uncompressed_total_bytes * 100), 2) as compression_ratio_pct
FROM timescaledb_information.compressed_hypertable_stats;

-- 5. TIEMPOS DE INGESTA POR SENSOR (Rendimiento)
SELECT 
    sensor_id,
    COUNT(*) as total_readings,
    MIN(time) as first_reading,
    MAX(time) as last_reading,
    EXTRACT(EPOCH FROM (MAX(time) - MIN(time))) / COUNT(*) as avg_interval_seconds
FROM sensor_data
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY sensor_id
ORDER BY avg_interval_seconds DESC
LIMIT 10;