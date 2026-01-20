from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI(title="Service 1 (Gateway)")

@app.get("/")
def read_root():
    return {"message": "Service 1 (Gateway) is running. Call /api/data/{id} to test the chain."}

@app.get("/api/data/{item_id}")
def get_data_chain(item_id: int):
    """
    Endpoint สำหรับให้ User เรียก
    Function นี้จะเรียกไปยัง Service 2 (Logic) ผ่าน REST API
    """
    # ชื่อ service ใน Docker Compose ของ Service 2 คือ 'service_2'
    # Service 2 รันอยู่ที่ port 8000 ภายใน network ของ docker
    service_2_url = f"http://service_2:8000/process/{item_id}"
    
    print(f"[Service 1] Forwarding request to Service 2: {service_2_url}")
    
    try:
        response = requests.get(service_2_url)
        if response.status_code == 200:
            return {
                "final_response": "Success from Service 1",
                "data_from_chain": response.json()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from Service 2")
            
    except requests.exceptions.RequestException as e:
        print(f"[Service 1] Connection Error: {e}")
        raise HTTPException(status_code=503, detail=f"Service 2 Unavailable: {e}")

if __name__ == "__main__":
    # Service 1 จะ expose ออกมาให้เราใช้
    uvicorn.run(app, host="0.0.0.0", port=8000)
