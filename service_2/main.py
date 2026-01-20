from fastapi import FastAPI, HTTPException
import grpc
import sys
import os
import uvicorn

# เพิ่ม path เพื่อให้ import generated code ได้
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

try:
    import data_pb2
    import data_pb2_grpc
except ImportError:
    pass

app = FastAPI(title="Service 2 (Logic)")

@app.get("/")
def read_root():
    return {"message": "Service 2 (Logic Service) is running. Connects to Service 3 via gRPC."}

@app.get("/process/{item_id}")
def process_data(item_id: int):
    """
    รับ REST API request แล้วส่งต่อไปยัง Service 3 ผ่าน gRPC
    """
    # ที่อยู่ของ Service 3 (ชื่อ service ใน docker-compose คือ 'service_3')
    target = 'service_3:50051'
    
    print(f"[Service 2] Connecting to gRPC server at {target}...")
    
    try:
        # เปิด Channel เชื่อมต่อไปยัง gRPC server
        with grpc.insecure_channel(target) as channel:
            stub = data_pb2_grpc.DataServiceStub(channel)
            
            # เรียก Remote Procedure Call 'GetData'
            print(f"[Service 2] Calling GetData for ID: {item_id}")
            response = stub.GetData(data_pb2.DataRequest(id=item_id))
            
            # ประมวลผลผลลัพธ์เล็กน้อย (Logic)
            result = {
                "source": "Service 2 Proxy",
                "processed": True,
                "original_data": {
                    "id": response.id,
                    "content": response.content,
                    "author": response.author_name,
                    "code": response.author_id
                }
            }
            return result
    except grpc.RpcError as e:
        print(f"[Service 2] gRPC Error: {e}")
        raise HTTPException(status_code=500, detail=f"gRPC Communication Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
