# main.py

import logging
import os

from dotenv import load_dotenv
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore,InMemoryPushNotifier
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
import httpx
from agent_executor import OrderAgentExecutor

load_dotenv()
logging.basicConfig(level=logging.INFO)

def main():
    host = "localhost"
    port = 10002

    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="order_status_tracking",
        name="Order Tracking",
        description="Check order status, estimated delivery, and tracking number.",
        tags=["orders", "shipping", "returns"],
        examples=[
            "Where is my order ORD123?",
            "Has order ORD456 shipped?",
            "What is the estimated delivery date for ORD789?",
        ],
    )

    agent_card = AgentCard(
        name="Order Management Agent",
        description="Handles order status, tracking, returns, and modifications.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        capabilities=capabilities,
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        skills=[skill],
    )

    httpx_client = httpx.AsyncClient()
    request_handler = DefaultRequestHandler(
            agent_executor=OrderAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()
