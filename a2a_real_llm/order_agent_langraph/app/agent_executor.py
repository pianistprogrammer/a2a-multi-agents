import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from agent import OrderAgent

logger = logging.getLogger(__name__)

class OrderAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = OrderAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if not context.task_id or not context.context_id:
            raise ValueError("Missing task_id or context_id")
        if not context.message:
            raise ValueError("Message is required")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()
        await updater.start_work()

        query = context.get_user_input()
        try:
            async for item in self.agent.stream(query, context.context_id):
                part = [Part(root=TextPart(text=item["content"]))]
                logger.info(f"Processing part: {part}")
                if item["require_user_input"]:
                    await updater.update_status(TaskState.input_required, message=updater.new_agent_message(part))
                    break
                elif item["is_task_complete"]:
                    await updater.add_artifact(part, name="order_result")
                    await updater.complete()
                    break
                else:
                    await updater.update_status(TaskState.working, message=updater.new_agent_message(part))
        except Exception as e:
            logger.error(f"Error during execution: {e}")
            raise ServerError(error=InternalError()) from e

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise ServerError(error=UnsupportedOperationError())
