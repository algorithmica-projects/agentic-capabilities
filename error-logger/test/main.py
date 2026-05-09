import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
load_dotenv(override=True)
import logfire
from error_logger.logger import ErrorLogger

logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent(
    'ollama:qwen3.7.1:9b',
    capabilities=[ErrorLogger()],
    instructions="You are a helpful assistant."
)

async def main():    
    print("Agent is ready! (Type 'exit' to quit)")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ("exit", "quit"):
            break
        result = await agent.run(user_input)
        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())