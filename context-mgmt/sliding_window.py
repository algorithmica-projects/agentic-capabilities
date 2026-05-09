from typing import Any
from pydantic_ai import ModelMessage, RunContext, ModelRequestContext
from pydantic_ai.capabilities import AbstractCapability
from dataclasses import dataclass
from utils import _find_safe_cutoff, _prepend_first_user_message

@dataclass
class SlidingWindow(AbstractCapability[Any]):
    max_messages: int = 100
    keep_messages: int = 40
    preserve_first_user_message: bool = True

    async def before_model_request(
        self,
        ctx: RunContext[Any],
        request_context: ModelRequestContext,
    ) -> ModelRequestContext:
        """Trim the message list if it exceeds the configured threshold."""

        messages: list[ModelMessage] = list(request_context.messages)
        print(len(messages))
        if len(messages) <= self.max_messages:
            return request_context
        print(len(messages))
        cutoff = _find_safe_cutoff(messages, self.keep_messages)

        if cutoff > 0:
            trimmed = messages[cutoff:]
            if self.preserve_first_user_message:
                trimmed = _prepend_first_user_message(messages, cutoff, trimmed)
            request_context.messages = trimmed

        return request_context