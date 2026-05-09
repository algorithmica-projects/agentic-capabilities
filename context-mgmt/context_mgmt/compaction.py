from typing import Any
from pydantic_ai import ModelMessage, ModelRequest, RunContext, ModelRequestContext, SystemPromptPart
from pydantic_ai.capabilities import AbstractCapability
from dataclasses import dataclass
from utils import _find_safe_cutoff, _find_first_user_message, _format_messages, _extract_system_prompts, _extract_previous_summary, _SUMMARY_PREFIX

@dataclass
class Compaction(AbstractCapability[Any]):
    max_messages: int = 100
    keep_messages: int = 40
    preserve_first_user_message: bool = True
    summary_prompt = """\
        You are a context summarization assistant.  Extract the most important \
        information from the conversation below.

        The conversation history will be replaced with your summary, so include all \
        facts, decisions, and outcomes that are necessary for continuing the task.  \
        Do NOT repeat completed actions — focus on results and open questions.

        Respond ONLY with the summary.  No preamble, no markdown fences.

        <messages>
        {messages}
        </messages>\
    """

    async def _summarize(
        self,
        messages: list[ModelMessage],
        *,
        previous_summary: str | None = None,
    ) -> str:
        """Generate a summary for the given messages using the configured model."""
        from pydantic_ai import Agent

        formatted = _format_messages(messages)
        prompt = self.summary_prompt.format(messages=formatted)

        if previous_summary is not None:
            prompt = f'{prompt}\n\n<previous_summary>\n{previous_summary}\n</previous_summary>'

        agent: Agent[None, str] = Agent(
            self.model,
            instructions='You are a context summarization assistant. Extract the most important information from conversations.',
        )
        result = await agent.run(prompt)
        return result.output.strip()

    async def before_model_request(
        self,
        ctx: RunContext[Any],
        request_context: ModelRequestContext,
    ) -> ModelRequestContext:
        """Trim the message list if it exceeds the configured threshold."""

        messages: list[ModelMessage] = list(request_context.messages)
        if len(messages) <= self.max_messages:
            return request_context

        cutoff = _find_safe_cutoff(messages, self.keep_messages)

        if cutoff <= 0:
            return request_context

        system_parts = _extract_system_prompts(messages)
        to_summarize = messages[:cutoff]
        preserved = messages[cutoff:]

        previous_summary = _extract_previous_summary(messages) if self.incremental else None
        summary = await self._summarize(to_summarize, previous_summary=previous_summary)

        summary_part = SystemPromptPart(content=f'{_SUMMARY_PREFIX}{summary}')
        summary_message = ModelRequest(parts=[*system_parts, summary_part])

        first_user: list[ModelMessage] = []
        if self.preserve_first_user_message:
            first_user_msg = _find_first_user_message(messages)
            if first_user_msg is not None:
                idx = messages.index(first_user_msg)
                if idx < cutoff and first_user_msg not in preserved:
                    first_user = [first_user_msg]

        request_context.messages = [summary_message, *first_user, *preserved]
        return request_context