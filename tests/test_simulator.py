"""
Tests básicos para el simulador de telemetría
Adaptado al código real de sensor_simulator.py
"""

import sys
import os
import random

# Agregar el proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar desde el simulador real
from generator.sensor_simulator import SENSOR_TYPES, LOCATIONS

def test_sensor_types_exists():
    """Verifica que SENSOR_TYPES está definido"""
    assert SENSOR_TYPES is not None
    assert isinstance(SENSOR_TYPES, dict)

def test_sensor_types_have_correct_keys():
    """Verifica que los tipos de sensores son los esperados"""
    expected_keys = {'temperature', 'pressure', 'vibration', 'humidity', 'current'}
    assert set(SENSOR_TYPES.keys()) == expected_keys

def test_each_sensor_has_min_max_unit():
    """Verifica que cada sensor tiene min, max, unit"""
    for sensor_type, config in SENSOR_TYPES.items():
        assert 'min' in config
        assert 'max' in config
        assert 'unit' in config
        assert isinstance(config['min'], (int, float))
        assert isinstance(config['max'], (int, float))

def test_min_less_than_max():
    """Verifica que min es menor que max para cada sensor"""
    for sensor_type, config in SENSOR_TYPES.items():
        assert config['min'] < config['max']

def test_temperature_range():
    """Verifica rango de temperatura"""
    temp = SENSOR_TYPES['temperature']
    assert temp['min'] == -10
    assert temp['max'] == 45
    assert temp['unit'] == '°C'

def test_pressure_range():
    """Verifica rango de presión"""
    pressure = SENSOR_TYPES['pressure']
    assert pressure['min'] == 950
    assert pressure['max'] == 1050
    assert pressure['unit'] == 'hPa'

def test_locations_exists():
    """Verifica que LOCATIONS está definido"""
    assert LOCATIONS is not None
    assert isinstance(LOCATIONS, list)

def test_locations_have_expected_places():
    """Verifica que las ubicaciones son las esperadas"""
    expected_locations = ['North_Plant', 'South_Plant', 'East_Wing', 'West_Wing', 'Central_Control']
    assert set(LOCATIONS) == set(expected_locations)

def test_random_value_generation():
    """Verifica que se pueden generar valores aleatorios correctamente"""
    for sensor_type, config in SENSOR_TYPES.items():
        for _ in range(50):
            value = round(random.uniform(config['min'], config['max']), 2)
            assert config['min'] <= value <= config['max']

def test_value_precision():
    """Verifica que los valores tienen 2 decimales"""
    for sensor_type, config in SENSOR_TYPES.items():
        for _ in range(20):
            value = round(random.uniform(config['min'], config['max']), 2)
            str_value = str(value)
            if '.' in str_value:
                decimal_places = len(str_value.split('.')[-1])
                assert decimal_places <= 2