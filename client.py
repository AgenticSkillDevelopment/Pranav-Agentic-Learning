from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"], ##ensure absolute path
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp/weather",
                "transport": "streamable-http"
            }
        }
    )
#agent = create_react_agent(client, ChatGroq(model="llama3-8b-8192"))

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    agent=create_react_agent(
        model,tools
        )
    
    math_response=await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": "What is 100+200?"}
        ]}
        )
    
    print("Math Response: ",math_response["messages"][-1].content)

    weather_response=await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": "What is the weather in Tokyo?"}
        ]}
        )
    
    print("Weather Response: ",weather_response["messages"][-1].content)


asyncio.run(main())









