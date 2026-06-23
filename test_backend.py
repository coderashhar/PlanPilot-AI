import asyncio
from api.models.schemas import UserRequest
from api.index import chat_endpoint

async def run_test():
    req = UserRequest(query="We are 5 friends in Bhopal. Budget ₹2000. Suggest a dinner plan for tonight.")
    print("Testing Backend...")
    try:
        res = await chat_endpoint(req)
        print("Success! Response:")
        print(res.model_dump_json(indent=2))
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
