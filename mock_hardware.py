import time
import requests
import pandas as pd
import json

CSV_FILE = "ml-data/edgeguard_training_data.csv"
API_URL = "http://127.0.0.1:8000/readings"

def main():
    print(f"Loading data from {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    
    # We will pick a subset of sensors to simulate
    sensors = {
        "engine_temp": "C",
        "oil_pressure": "bar",
        "vibration_x": "g",
        "hydraulic_pressure": "bar",
        "battery_voltage": "V",
        "rpm": "rpm"
    }

    print("Starting simulation...")
    for index, row in df.iterrows():
        truck_id = str(row["truck_id"])
        device_ts = str(int(time.time() * 1000))
        
        for sensor, unit in sensors.items():
            if sensor in row:
                payload = {
                    "truck_id": truck_id,
                    "sensor_type": sensor,
                    "value": float(row[sensor]),
                    "unit": unit,
                    "device_ts": device_ts
                }
                try:
                    requests.post(API_URL, json=payload, timeout=2.0)
                except Exception as e:
                    print(f"Error posting data: {e}")
        
        print(f"Pushed cycle {row.get('cycle_id')} for {truck_id}")
        time.sleep(1) # Mimic live streaming (1 row per second)

if __name__ == "__main__":
    main()
