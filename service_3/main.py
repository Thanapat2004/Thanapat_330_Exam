import asyncio
import grpc
from concurrent import futures
import uvicorn
from fastapi import FastAPI
import sys
import os

# เพิ่ม path เพื่อให้ import generated code ได้สะดวก
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

# Import ไฟล์ที่ generate มาจาก proto
try:
    import data_pb2
    import data_pb2_grpc
except ImportError:
    # เผื่อกรณีรัน local ก่อน generate
    pass

# ==========================================
# ส่วนของ gRPC Server Definition
# ==========================================
class DataService(data_pb2_grpc.DataServiceServicer):
    """
    คลาสนี้ implement logic ของ gRPC Service
    รับ request เป็น id, ส่งคืนข้อมูล mock up พร้อมรหัส 330
    """
    def GetData(self, request, context):
        print(f"[Service 3] gRPC Request received for ID: {request.id}")
        # สร้าง response พร้อมใส่ชื่อและรหัสของคุณตามโจทย์
        return data_pb2.DataResponse(
            id=request.id,
            content=f"Secret Data for Item {request.id}",
            author_name="Tanapat Boonphad",
            author_id="330"
        )

async def serve_grpc():
    """
    ฟังก์ชันสำหรับรัน gRPC Server แบบ Async
    """
    server = grpc.aio.server()
    data_pb2_grpc.add_DataServiceServicer_to_server(DataService(), server)
    server.add_insecure_port('[::]:50051')
    print("[Service 3] gRPC Server starting on port 50051...")
    await server.start()
    await server.wait_for_termination()

# ==========================================
# ส่วนของ FastAPI Application
# ==========================================
app = FastAPI(title="Service 3 (Data)")

@app.get("/")
def read_root():
    return {"message": "Service 3 (Data Service) is running. gRPC port: 50051"}

# ==========================================
# Main Entry Point
# ==========================================
if __name__ == "__main__":
    # เราจะรันทั้ง FastAPI (Uvicorn) และ gRPC server ใน process เดียวกัน
    # โดยใช้ asyncio loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # สร้าง task สำหรับ gRPC
    grpc_task = loop.create_task(serve_grpc())
    
    # รัน FastAPI ด้วย Uvicorn (blocking call จึงต้องรันแยกหรือ config แบบนี้ก็ได้)
    # แต่เพื่อให้ง่าย เราจะให้ uvicorn รันเป็น main และ gRPC เป็น background task หรือกลับกัน
    # วิธีที่ง่ายสำหรับ demo คือ run uvicorn บน port 8000 และ gRPC บน background
    
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop=loop)
    server = uvicorn.Server(config)
    
    # รันทั้งคู่พร้อมกัน
    loop.run_until_complete(asyncio.gather(server.serve(), grpc_task))
