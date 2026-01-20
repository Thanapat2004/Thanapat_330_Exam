# ใช้ Python base image
FROM python:3.9-slim

# กำหนด working directory
WORKDIR /app

# คัดลอก requirements และ install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# เปิด port สำหรับ FastAPI
EXPOSE 8000

# รัน main script
CMD ["python", "main.py"]
