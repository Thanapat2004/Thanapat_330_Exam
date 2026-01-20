Project: tanapat_boonphad_330
Student: Tanapat Boonphad (ID:330)

Directory Structure:
Midterm_Exam_DevOps/
├── docker-compose.yml
├── readme.txt
├── service_1/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── service_2/
│   ├── Dockerfile
│   ├── main.py
│   ├── proto/
│   │   └── data.proto
│   └── requirements.txt
└── service_3/
    ├── Dockerfile
    ├── main.py
    ├── proto/
    │   └── data.proto
    └── requirements.txt

คำอธิบายการทำงาน (How it works):
1. User ส่ง Request มาที่ Service 1 (Gateway) ผ่าน REST API
   - URL: http://localhost:8001/api/data/{id}
   
2. Service 1 รับ Request และส่งต่อให้ Service 2 (Logic) ผ่าน REST API (Internal)
   - Service 1 ทำหน้าที่เป็น Gateway เปิดประตูรับแขก

3. Service 2 รับ Request จาก Service 1 และแปลง request เพื่อเรียก Service 3 (Data) ผ่าน gRPC
   - Service 2 ทำหน้าที่เป็น Business Logic / Middleman

4. Service 3 รับ gRPC Call, ค้นหาข้อมูล (Mockup), และส่ง Response กลับ
   - Service 3 คือ Data Service ที่เก็บข้อมูลสำคัญ

Flow:
[User] --HTTP--> [Service 1] --HTTP--> [Service 2] --gRPC--> [Service 3]

วิธีการรัน (How to run):
1. เปิด Terminal ใน folder `Midterm_Exam_DevOps`
2. รันคำสั่ง:
   docker-compose up --build
3. รอจนกว่าทุก container จะ Start เสร็จ (เห็น log ขึ้นครบ)

ผลลัพธ์ที่ควรได้ (Expected Result):
- เมื่อเรียกผ่าน Browser หรือ Postman: http://localhost:8001/api/data/123
- จะได้ JSON Response:
{
    "final_response": "Success from Service 1",
    "data_from_chain": {
        "source": "Service 2 Proxy",
        "processed": true,
        "original_data": {
            "id": 123,
            "content": "Secret Data for Item 123",
            "author": "Tanapat Boonphad",
            "code": "330"
        }
    }
}
