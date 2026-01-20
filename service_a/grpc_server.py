import grpc
from concurrent import futures
import sys
import os

# Add the proto directory to sys.path to allow imports of generated code
current_dir = os.path.dirname(os.path.abspath(__file__))
proto_dir = os.path.join(current_dir, 'proto')
sys.path.append(proto_dir)

import user_pb2
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUserInfo(self, request, context):
        print(f"Service A: Received request for user ID {request.id}")
        return user_pb2.UserResponse(
            id=request.id,
            name=f"User {request.id}",
            email=f"user{request.id}@example.com"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    print("Service A (Server) started on port 50051...")
    server.start()
    server.wait_for_termination()
