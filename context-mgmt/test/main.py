import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
load_dotenv(override=True)
import logfire
from context_mgmt.sliding_window import SlidingWindow
from context_mgmt.compaction import Compaction
logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent(
    'ollama:qwen3.5:9b',
    capabilities=[
        # SlidingWindow(max_messages=10, keep_messages=4)
        Compaction(max_messages=4, keep_messages=2)
    ],
    instructions="You are a helpful assistant."
)

async def main():    
    print("Agent is ready! (Type 'exit' to quit)")
    history = []
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ("exit", "quit"):
            break
        result = await agent.run(user_input, message_history=history)
        history = result.all_messages()  
        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
