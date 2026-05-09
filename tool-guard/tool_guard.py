from typing import Any
from pydantic_ai import  RunContext, ToolDefinition
from pydantic_ai.capabilities import AbstractCapability
from dataclasses import dataclass

@dataclass
class ToolGuard(AbstractCapability[Any]):
    
    async def prepare_tools(self, ctx: RunContext, tool_defs: list[ToolDefinition]) -> list[ToolDefinition]:
        if ctx.deps.role == "user":
            return [tool_def for tool_def in tool_defs if tool_def.name == "get_temperature"]
        elif ctx.deps.role == "admin":
            return tool_defs
        else:
            return None