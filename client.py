# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
# from langchain_groq import ChatGroq

# from dotenv import load_dotenv
# load_dotenv()

# import asyncio

# async def main():
#     client=MultiServerMCPClient(
#         {
#             "math":{
#                 "command":"python",
#                 "args":["mathserver.py"], ## Ensure correct absolute path
#                 "transport":"stdio",
            
#             },
#             "weather": {
#                 "url": "http://localhost:8000/mcp",  # Ensure server is running here
#                 "transport": "streamable_http",
#             }

#         }
#     )

#     import os
#     os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

#     tools=await client.get_tools()
#     model=ChatGroq(model="qwen-qwq-32b")
#     agent=create_react_agent(
#         model,tools
#     )

#     math_response = await agent.ainvoke(
#         {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
#     )

#     print("Math response:", math_response['messages'][-1].content)

#     weather_response = await agent.ainvoke(
#         {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
#     )
#     print("Weather response:", weather_response['messages'][-1].content)

# asyncio.run(main())

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # Load tools from MCP servers
    tools = await client.get_tools()
    tool_names = [tool.name for tool in tools]
    print("✅ Registered tools:", tool_names)

    # Check that required tools are available
    assert "multiple" in tool_names, "'multiple' tool not found in registered tools"
    assert "get_weather" in tool_names, "'get_weather' tool not found in registered tools"

    # Use a model that supports tool calling
    model = ChatGroq(model="llama3-8b-8192")

    agent = create_react_agent(model, tools)

    # Math query
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print("📐 Math response:", math_response['messages'][-1].content)

    # Weather query
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("🌦️ Weather response:", weather_response['messages'][-1].content)

asyncio.run(main())