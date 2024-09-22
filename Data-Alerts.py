import psycopg2
from datetime import datetime, timedelta
import requests
import time

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

# ฟังก์ชันสำหรับส่งแจ้งเตือนผ่าน Line Notify
def send_line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    token = 'wo1sgtT7u2JC7Z26GkWwjEFbfcBQtdKIvgQjZE'  
    headers = {
        'Authorization': 'Bearer ' + token
    }
    data = {'message': message}
    requests.post(url, headers=headers, data=data)

# ฟังก์ชันสำหรับตรวจสอบค่า IAQ
def check_comfort_conditions():
    conn = connect_to_cratedb()
    cursor = conn.cursor()

    # ดึงข้อมูล 5 นาทีล่าสุด
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=5)

    query = """
    SELECT datapoint, AVG(value) as avg_value 
    FROM raw_data 
    WHERE timestamp >= %s 
    GROUP BY datapoint;
    """
    cursor.execute(query, (five_minutes_ago,))
    results = cursor.fetchall()

    # กำหนดช่วงความสบายสำหรับ temperature, humidity, และ co2
    messages = []
    for row in results:
        datapoint, avg_value = row
        if datapoint == 'temperature' and (avg_value < 23 or avg_value > 26):
            messages.append(f"Temperature out of range: {avg_value:.2f}°C")
        elif datapoint == 'humidity' and (avg_value < 40 or avg_value > 50):
            messages.append(f"Humidity out of range: {avg_value:.2f}%")
        elif datapoint == 'co2' and avg_value >= 1000:
            messages.append(f"CO2 out of range: {avg_value:.2f} ppm")

    # ส่งข้อความแจ้งเตือนหากมีค่าที่ผิดปกติ
    if messages:
        for message in messages:
            send_line_notify(message)

    cursor.close()
    conn.close()

# ฟังก์ชันสำหรับรันทุก 1 นาที
def monitor_room_conditions():
    while True:
        print(f"Checking comfort conditions at {datetime.now()}")
        check_comfort_conditions()
        time.sleep(60)  # รอ 1 นาที ก่อนตรวจสอบครั้งถัดไป

if __name__ == "__main__":
    monitor_room_conditions()
