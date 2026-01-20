# ใช้ Python base image
FROM python:3.9-slim

# กำหนด working directory
WORKDIR /app

# คัดลอก requirements และ install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# สร้างไฟล์ python จาก proto (เพื่อใช้เป็น client)
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/data.proto

# เปิด port สำหรับ FastAPI
EXPOSE 8000

# รัน main script
CMD ["python", "main.py"]
