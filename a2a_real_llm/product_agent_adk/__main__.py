import logging
import os

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv

from agent import create_agent  # This should be the Product Agent defined earlier
from agent_executor import ProductAgentExecutor  # Your custom executor if needed
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    host = "localhost"
    port = 10001

    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="product_info_retrieval",
        name="Product Info & Inventory",
        description="Retrieves detailed information, specs, availability, and reviews for products.",
        tags=["products", "inventory", "catalog"],
        examples=[
            "What is P001?",
            "Is P005 available in stock?",
            "What are customers saying about P003?",
        ],
    )
    agent_card = AgentCard(
        name="Product Agent",
        description="Provides detailed product info, specs, stock status, and review summaries.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        capabilities=capabilities,
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        skills=[skill],
    )
    adk_agent = create_agent()
    runner = Runner(
        app_name=agent_card.name,
        agent=adk_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    agent_executor = ProductAgentExecutor(runner)

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()
