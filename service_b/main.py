from .grpc_client import get_user_info

if __name__ == "__main__":
    print("Service B (Client) starting...")
    user_id = 1
    user = get_user_info(user_id)
    if user:
        print(f"Service B: Received Response -> ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        print("Service B: Failed to get user info.")
