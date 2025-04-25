# Agentic AI with Model Context Protocol (MCP)

This project implements an Agentic AI system that connects a Groq-hosted LLM (qwen-qwq-32b model) with various tools through a custom Model Context Protocol (MCP) server. The system enhances the LLM's capabilities by providing contextual information from Wikipedia, internet search (via Tavily API), and financial data (via Yahoo Finance API).

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
