from typing import Any
from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent, FunctionToolset, RunContext, ToolDefinition
from pydantic_ai.capabilities import PrepareTools
from dataclasses import dataclass
from tool_guard import ToolGuard

load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

weather_toolset = FunctionToolset()

@weather_toolset.instructions
def instructions(ctx: RunContext[str]) -> str:
    return 'Use these tools for current temperature and wind forecasts.'


@weather_toolset.tool
def get_temperature(ctx:RunContext[Any],city: str) -> str:
    """Get the current temperature for a city."""
    return f"The temperature in {city} is 22°C."

@weather_toolset.tool
def get_wind_speed(ctx:RunContext[Any], city: str) -> str:
    """Get the current wind speed for a city in km/h."""
    return f"The wind speed in {city} is 15 km/h."

@dataclass
class Deps:
    role: str

agent = Agent(
    'ollama:qwen3.5:9b',
    toolsets=[weather_toolset],
    capabilities=[ToolGuard()],
    instructions="You are a helpful assistant."
)

async def main():
    deps = Deps(role="user")
    result = await agent.run("What's the temperature in london?", deps=deps)
    print(f"Output: {result.output}")
    result = await agent.run("What's the wind speed in london?", deps=deps)
    print(f"Output: {result.output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())