# Agentic AI with Model Context Protocol (MCP)

This project implements an Agentic AI system that connects a Groq-hosted LLM (qwen-qwq-32b model) with various tools through a custom Model Context Protocol (MCP) server. The system enhances the LLM's capabilities by providing contextual information from Wikipedia, internet search (via Tavily API), and financial data (via Yahoo Finance API).

## About MCP

The Model Context Protocol (MCP) is an open standard developed by Anthropic to standardize how applications provide context to large language models (LLMs). It facilitates seamless integration between LLM applications and external data sources and tools, allowing AI systems to interact dynamically with various services through a standardized interface. 

Key Features of MCP:
* Standardization: Provides a universal protocol for interfacing AI assistants with structured tools and data layers.
* Modular Architecture: Follows a client–server pattern over a persistent stream, typically mediated by a host AI system.
* Dynamic Introspection: Supports dynamic discovery of tools and resources through methods like tools/list and resources/list.

Security: Incorporates host-mediated authentication and supports secure transport protocols.​
By adopting MCP, developers can build AI applications that are more interoperable, secure, and capable of complex workflows.​

To add new tools to the MCP server:​
* Define the Tool: Create a new function that handles the specific task or data retrieval.​
* Register the Tool: Update the server's tool registry to include the new function, specifying the tool's name and description.​
* Handle Requests: Ensure the server can route incoming requests to the appropriate tool based on the query.​
This modular approach allows for easy expansion of the server's capabilities, enabling the language model to access a broader range of contextual information.

## Features

- **MCP Server**: Central hub that provides access to various tools
- **Three Integrated Tools**:
  1. Wikipedia Search - for factual information retrieval
  2. Internet Search - powered by Tavily API for comprehensive web results
  3. Yahoo Finance API - for real-time stock and financial data
- **Groq API Integration**: Ultra-fast LLM processing using qwen-qwq-32b model
- **Client-Server Architecture**: Clean separation between tool management and LLM interaction

## Prerequisites

Before you begin, ensure you have the following:

- Install UV fro python [installation](https://docs.astral.sh/uv/getting-started/installation/) 
- Groq API key. Refer to the [documentation](https://docs.aicontentlabs.com/articles/groq-api-key/)
- Tavily API key (sign up at [Tavily AI](https://tavily.com/))

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/dev484p/AgenticAI_MCP
   cd AgenticAI_MCP
   ```
2. Install dependencies:
   ```
   uv add "mcp[cli]"
   ```
3. Set up your environment variables:
   Update Groq and Tavily api key in keys.json
   
4. Optional (To run the server with the MCP Inspector for development):
  ```
  uv run mcp dev server.py
  ```
5. Run the following command to initiate the chatbot:
   ```
   uv run client.py
   ```
   
## Available Tools
The system provides three tools through the MCP server:

* Wiki Search:
  Access Wikipedia information
  Example query: "Tell me about the history of artificial intelligence"

*Internet Search (Tavily):
  Get comprehensive web search results
  Example query: "What are the latest developments in quantum computing?"

*Yahoo Finance:
  Access stock prices and financial data
  Example query: "What is the current price of AAPL stock?"

## Refrence
* https://modelcontextprotocol.io/introduction
* https://github.com/langchain-ai/langchain-mcp-adapters
* https://github.com/krishnaik06/MCP-CRASH-Course
