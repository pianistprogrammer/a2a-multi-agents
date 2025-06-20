import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, AsyncIterable, List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import httpx
import nest_asyncio
from dotenv import load_dotenv

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    MessageSendParams, SendMessageRequest,
    SendMessageResponse, SendMessageSuccessResponse, Task,
)
from google.adk import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from dummy_data import COMBINED_DATA

import logging
# Assuming this is a module with user data
load_dotenv()
nest_asyncio.apply()


class RemoteAgentConnections:
    def __init__(self, agent_card: AgentCard, agent_url: str):
        self.card = agent_card
        self._httpx = httpx.AsyncClient(timeout=30)
        self.agent_client = A2AClient(self._httpx, agent_card, url=agent_url)

    async def send_message(self, message_request: SendMessageRequest) -> SendMessageResponse:
        return await self.agent_client.send_message(message_request)


class HostAgent:
    def __init__(self):
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        self.agents: str = ""
        self._agent = self.create_agent()
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        self._user_id = "host_agent"

    async def _async_init_components(self, addresses: List[str]):
        async with httpx.AsyncClient(timeout=30) as client:
            for url in addresses:
                try:
                    card = await A2ACardResolver(client, url).get_agent_card()
                    conn = RemoteAgentConnections(card, url)
                    self.remote_agent_connections[card.name] = conn
                    self.cards[card.name] = card
                except Exception as e:
                    print(f"❗Error connecting to {url}: {e}")

        self.agents = "\n".join(
            json.dumps({"name": c.name, "description": c.description})
            for c in self.cards.values()
        ) or "No agents connected"

    @classmethod
    async def create(cls, addresses: List[str]):
        inst = cls()
        await inst._async_init_components(addresses)
        return inst

    def create_agent(self) -> Agent:
        return Agent(
            name="HostAgent",
            description="Customer Experience Orchestrator that routes product queries to appropriate agents or handles CRM queries directly.",
            model=LiteLlm(
                api_base="http://localhost:11434/v1",
                model="openai/qwen3:1.7b",
                api_key="ollama",
            ),
            instruction=self.root_instruction,
            tools=[self.call_agent, self.get_user_info],  # ← include here
        )

    async def get_user_info(self, email: str) -> str: # <--- THIS IS THE KEY CHANGE
        """Lookup user details by email address."""
        user = COMBINED_DATA["CRM_DATABASE"].get(email.lower()) # Use COMBINED_DATA
        logging.info(f"Looking up user with email: {email}, found: {user}")
        if not user:
            return f"No user found with email: {email}"

        summary = f"""📄 **User Profile**
        - Name: {user["name"]}
        - Email: {user["email"]}
        - Phone: {user.get("phone", "N/A")}
        - Address: {user.get("address", "N/A")}
        - Account Status: {user["account_status"]}
        - Membership Level: {user.get("membership_level", "N/A")}
        - Last Contact: {user.get("last_contact", "N/A")}
        - Preferences: {', '.join(user.get('preferences', []))}

        🎫 **Support Tickets**:
        """ + "\n".join(
                    f"  • {ticket['issue']} — {ticket['status']}"
                    for ticket in user.get("support_tickets", [])
                )

        # You might also want to add associated orders here as in my previous combined example
        summary += f"""
        🛒 **Associated Orders**:
        """ + "\n".join(
            f"  • {order_id} (Status: {COMBINED_DATA['ORDER_DATABASE'].get(order_id, {}).get('status', 'Unknown')})"
            for order_id in user.get("orders", [])
        ) if user.get("orders") else "  • No orders found."


        return summary

    def root_instruction(self, ctx: ReadonlyContext) -> str:
        return f""" You are HostAgent, the Customer Experience Orchestrator. Your role is to:

        - Understand the customer's request.
        - Choose the correct connected agent or tool based on the topic.
        - Use the appropriate function call format to get information or complete a task.
        - Respond in a clear, professional, and helpful way.

        ---

        ## Tool: call_agent

        Use this when the question is about **products** or **orders**. The tool takes two arguments:

        - `agent_name`: one of "Product Agent" or "Order Management Agent"
        - `task`: a natural language question

        ### Examples:

        - User: *What are the specs of product P001?*  
        Function call:  
            name: call_agent  
            arguments: {{
                "agent_name": "Product Agent",
                "task": "Tell me about P001"
            }}

        - User: *Has my order #123456 been shipped?*  
        Function call:  
            name: call_agent  
            arguments: {{
                "agent_name": "Order Management Agent",
                "task": "What is the status of order #123456?"
            }}

        - User: *Can I cancel order #7890?*  
        Function call:  
            name: call_agent  
            arguments: {{
                "agent_name": "Order Management Agent",
                "task": "I want to cancel order #7890"
            }}

        ---

        ## Tool: get_user_info

        Use this when the customer is asking about **their account**, Requires email.

        ### Example:

        - User: *Can you tell me about my account? My email is john@example.com*  
        Function call:  
            name: get_user_info  
            arguments: {{
                "email": "john@example.com"
            }}
        Always choose the tool and fill in the function call accurately.

        ### Connected Agents:
        {self.agents}

        Date: {datetime.now():%Y-%m-%d}
        """

    async def stream(self, query: str, session_id: str) -> AsyncIterable[dict[str, Any]]:
        sess = await self._runner.session_service.get_session(
            app_name=self._agent.name, user_id=self._user_id, session_id=session_id
        ) or await self._runner.session_service.create_session(
            app_name=self._agent.name, user_id=self._user_id, state={}, session_id=session_id
        )
        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
        async for evt in self._runner.run_async(self._user_id, sess.id, content):
            if evt.is_final_response():
                txt = "\n".join(p.text for p in evt.content.parts if p.text)
                yield {"is_task_complete": True, "content": txt}
            else:
                yield {"is_task_complete": False, "updates": "🧠 HostAgent thinking..."}

    async def call_agent(self, agent_name: str, task: str, tool_context: ToolContext):
        """Delegate product-related tasks to the Product Agent."""
        if agent_name not in self.remote_agent_connections:
            raise ValueError(f"Agent {agent_name} not found")
        client = self.remote_agent_connections[agent_name]

        state = tool_context.state
        task_id = state.get("task_id", str(uuid.uuid4()))
        context_id = state.get("context_id", str(uuid.uuid4()))
        message_id = str(uuid.uuid4())

        payload = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": task}],
                "messageId": message_id,
                "taskId": task_id,
                "contextId": context_id,
            },
        }

        message_request = SendMessageRequest(
            id=message_id, params=MessageSendParams.model_validate(payload)
        )
        send_response: SendMessageResponse = await client.send_message(message_request)

        if not isinstance(send_response.root, SendMessageSuccessResponse) or not isinstance(send_response.root.result, Task):
            return "There was a problem handling your request. Please try again later."

        response_content = send_response.root.model_dump_json(exclude_none=True)
        json_content = json.loads(response_content)

        resp = []
        if json_content.get("result", {}).get("artifacts"):
            for artifact in json_content["result"]["artifacts"]:
                if artifact.get("parts"):
                    resp.extend(artifact["parts"])
        return resp


def _init_root_agent(urls: List[str]):
    async def init():
        inst = await HostAgent.create(urls)
        return inst.create_agent()
    try:
        return asyncio.run(init())
    except RuntimeError:
        return asyncio.get_event_loop().run_until_complete(init())


root_agent = _init_root_agent([
    "http://localhost:10001",  # Product Agent
    "http://localhost:10002",  # Order Management Agent
])
