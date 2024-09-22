import csv
import time
import psycopg2
from datetime import datetime

# ฟังก์ชันเชื่อมต่อกับ CrateDB
def connect_to_cratedb():
    conn = psycopg2.connect(
    host="localhost",
    port="5432", 
    dbname="doc",
    user="crate",
    password=""
    )   
    return conn

# ฟังก์ชันสำหรับอัปโหลดข้อมูลไปยัง CrateDB
def upload_to_cratedb(cursor, timestamp, temperature, humidity, co2):
    query = """
    INSERT INTO raw_data (timestamp, datetime, device_id, datapoint, value)
    VALUES (%s, %s, %s, %s, %s)
    """
    # อัปโหลดค่า temperature
    cursor.execute(query, (timestamp, timestamp.isoformat(), 'sensor_01', 'temperature', temperature))
    # อัปโหลดค่า humidity
    cursor.execute(query, (timestamp, timestamp.isoformat(), 'sensor_01', 'humidity', humidity))
    # อัปโหลดค่า co2
    cursor.execute(query, (timestamp, timestamp.isoformat(), 'sensor_01', 'co2', co2))

# ฟังก์ชันจำลองการทำงานของอุปกรณ์ IoT
def simulate_iot_device(csv_file):
    conn = connect_to_cratedb()
    cursor = conn.cursor()

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # อ่านข้อมูลจาก CSV
            temperature = float(row['temperature'])
            humidity = float(row['humidity'])
            co2 = float(row['co2'])

            # ตรวจสอบช่วงข้อมูล
            if temperature < 22:
                temperature = 22
            elif temperature > 32:
                temperature = 32

            if humidity < 30:
                humidity = 30
            elif humidity > 70:
                humidity = 70

            if co2 < 400:
                co2 = 400
            elif co2 > 2000:
                co2 = 2000

            # ใช้ real-time timestamp
            timestamp = datetime.now()

            # อัปโหลดข้อมูลไปยัง CrateDB
            upload_to_cratedb(cursor, timestamp, temperature, humidity, co2)

            # Commit transaction ทุกครั้งหลังจากอัปโหลดข้อมูล
            conn.commit()

            # รอ 5 วินาทีก่อนอัปโหลดข้อมูลแถวถัดไป
            time.sleep(5)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    simulate_iot_device('./mock_iaq_data.csv') 
