from typing import Any, AsyncIterable, Literal
from datetime import date
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from order_tools import get_order_status # Assuming order_tools.py is in the same directory

memory = MemorySaver()

class ResponseFormat(BaseModel):
    status: Literal["input_required", "completed", "error"]
    message: str

class OrderAgent:
    SYSTEM_INSTRUCTION = """
        You are an Order Management Assistant. Your task is to help customers with:
        - order status
        - tracking
        - order modifications or cancellations
        - return processing
        Use the appropriate tool (like get_order_status) based on the user's question.
        Always respond in a professional and helpful tone.
        If the user provides an invalid or missing order ID, prompt them to correct it.
        When providing order status, include all details returned by the get_order_status tool.
    """
    def __init__(self):
        self.model = ChatOllama(model="qwen3:1.7b", base_url="http://localhost:11434")
        self.tools = [get_order_status]
        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def invoke(self, query, context_id):
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        user_msg = f"{today_str}\n\nUser query: {query}"
        self.graph.invoke({"messages": [HumanMessage(content=user_msg)]}, config)
        return self.get_agent_response(config)

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        today_str = f"Today's date is {date.today():%Y-%m-%d}."
        inputs = {"messages": [HumanMessage(content=f"{today_str}\n\nUser query: {query}")]}
        config = {"configurable": {"thread_id": context_id}}

        last_tool_output = None # Store the last tool output

        async for item in self.graph.astream(inputs, config=config, stream_mode="values"):
            message = item["messages"][-1]
            if isinstance(message, AIMessage) and message.tool_calls:
                yield {"is_task_complete": False, "require_user_input": False, "content": "Fetching order details..."}
            elif isinstance(message, ToolMessage):
                # Capture the output of the tool call
                last_tool_output = message.content
                yield {"is_task_complete": False, "require_user_input": False, "content": "Processing..."}

        # After the stream, get the final state
        state = self.graph.get_state(config)
        structured = state.values.get("structured_response")

        final_message_content = "Sorry, something went wrong." # Default error message

        if structured and isinstance(structured, ResponseFormat):
            if structured.status == "completed":
                final_message_content = last_tool_output if last_tool_output else structured.message
            else:
                final_message_content = structured.message
        
        yield {
            "is_task_complete": structured.status == "completed" if structured else False,
            "require_user_input": structured.status == "input_required" if structured else True,
            "content": final_message_content,
        }

    async def get_agent_response(self, config):
        current_state = await self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")

        if structured_response and isinstance(structured_response, ResponseFormat):
            return {
                "is_task_complete": structured_response.status == "completed",
                "require_user_input": structured_response.status == "input_required",
                "content": structured_response.message, # This might still be the generic message
            }
        return {"is_task_complete": False, "require_user_input": True, "content": "Sorry, something went wrong."}