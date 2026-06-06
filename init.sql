-- ============================================
-- INDUSTRIAL TELEMETRY ENGINE
-- TimescaleDB Schema & Hypertables
-- ============================================

-- Extensión necesaria
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ============================================
-- TABLA PRINCIPAL: sensor_data
-- ============================================

CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    sensor_type VARCHAR(20) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    location VARCHAR(100),
    metadata JSONB
);

-- Convertir a hypertable (particionamiento por tiempo)
SELECT create_hypertable('sensor_data', 'time', chunk_time_interval => INTERVAL '1 day');

-- ============================================
-- ÍNDICES OPTIMIZADOS
-- ============================================

-- Índice para búsquedas por sensor y tiempo
CREATE INDEX idx_sensor_time ON sensor_data (sensor_id, time DESC);

-- Índice para búsquedas por tipo de sensor
CREATE INDEX idx_sensor_type ON sensor_data (sensor_type, time DESC);

-- ============================================
-- CONTINUOUS AGGREGATES (Materialized Views)
-- ============================================

-- Agregación por minuto
CREATE MATERIALIZED VIEW sensor_data_1min
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 minute', time) AS bucket,
    sensor_id,
    sensor_type,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    COUNT(*) AS sample_count
FROM sensor_data
GROUP BY bucket, sensor_id, sensor_type;

-- Agregación por hora
CREATE MATERIALIZED VIEW sensor_data_1hour
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    sensor_type,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY value) AS p95_value
FROM sensor_data
GROUP BY bucket, sensor_id, sensor_type;

-- ============================================
-- POLÍTICAS DE REFRESH AUTOMÁTICO
-- ============================================

-- Refresh cada minuto para la vista de 1 minuto
SELECT add_continuous_aggregate_policy('sensor_data_1min',
    start_offset => INTERVAL '5 minutes',
    end_offset => INTERVAL '1 minute',
    schedule_interval => INTERVAL '1 minute');

-- Refresh cada hora para la vista de 1 hora
SELECT add_continuous_aggregate_policy('sensor_data_1hour',
    start_offset => INTERVAL '2 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');

-- ============================================
-- COMPRESIÓN (ahorra ~90% de espacio)
-- ============================================

ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id',
    timescaledb.compress_orderby = 'time DESC'
);

-- Comprimir datos con más de 7 días
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');

-- ============================================
-- POLÍTICA DE RETENCIÓN (borrar datos viejos)
-- ============================================

-- Eliminar datos de más de 1 año
SELECT add_retention_policy('sensor_data', INTERVAL '365 days');

-- ============================================
-- QUERIES DE EJEMPLO
-- ============================================

-- 1. Últimas lecturas por sensor
-- SELECT DISTINCT ON (sensor_id) 
--     sensor_id, time, value
-- FROM sensor_data 
-- ORDER BY sensor_id, time DESC;

-- 2. Promedio diario por tipo de sensor en la última semana
-- SELECT 
--     time_bucket('1 day', time) AS day,
--     sensor_type,
--     AVG(value) as avg_value
-- FROM sensor_data
-- WHERE time > NOW() - INTERVAL '7 days'
-- GROUP BY day, sensor_type
-- ORDER BY day DESC;

-- 3. Sensores con anomalías (valor > 2 desviaciones)
-- SELECT sensor_id, time, value
-- FROM sensor_data
-- WHERE value > (
--     SELECT AVG(value) + 2 * STDDEV(value)
--     FROM sensor_data
--     WHERE sensor_type = 'temperature'
-- );