# Dockerfile สำหรับ IoT Simulation
FROM python:3.9-slim

# ตั้งค่า Working Directory
WORKDIR /app

# คัดลอกไฟล์ที่จำเป็นทั้งหมดไปที่ Container
COPY Simulation_iot.py /app/
COPY mock_iaq_data.csv /app/
COPY requirements.txt /app/

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# รัน IoT Simulation Script
CMD ["python", "Simulation_iot.py"]
