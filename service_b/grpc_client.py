import grpc
import sys
import os

# Add the proto directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
proto_dir = os.path.join(current_dir, 'proto')
sys.path.append(proto_dir)

import user_pb2
import user_pb2_grpc

def get_user_info(user_id):
    # Connect to the server running on localhost:50051
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        try:
            print(f"Service B: Requesting info for user ID {user_id}...")
            response = stub.GetUserInfo(user_pb2.UserRequest(id=user_id))
            return response
        except grpc.RpcError as e:
            print(f"Service B: RPC failed: {e}")
            return None
