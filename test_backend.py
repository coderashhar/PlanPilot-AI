import asyncio
from api.models.schemas import UserRequest
from api.index import chat_endpoint

async def chat_loop():
    print("PlanPilot AI CLI | Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.strip():
                continue
            
            req = UserRequest(query=user_input)
            print("\nPlanPilot AI is thinking...\n")
            res = await chat_endpoint(req)
            
            print(f"Summary: {res.summary}\n")
            print("--- Recommendations ---")
            for rec in res.recommendations:
                print(f"- {rec.name} (Score: {rec.score})")
                print(f"  Reason: {rec.reason}")
            
            if res.weather:
                print(f"\n--- Weather ---")
                print(f"{res.weather.condition.title()}, {res.weather.temperature}°C")
            
            if res.events:
                print(f"\n--- Events ---")
                for event in res.events:
                    print(f"- {event.name}")
                    print(f"  Link: {event.location}")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(chat_loop())
