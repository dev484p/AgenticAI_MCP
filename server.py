import httpx
import logging
import json
import urllib.parse
from typing import Any
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server with timeout configuration
mcp = FastMCP(
    "search-services",
    server_timeout=60,  # Increase timeout to 60 seconds
    request_timeout=30  # Individual request timeout
)

# Constants
WIKI_API_BASE = "https://en.wikipedia.org/w/api.php"
TAVILY_API_BASE = "https://api.tavily.com"
YAHOO_FINANCE_BASE = "https://query1.finance.yahoo.com/v8/finance/chart/"
USER_AGENT = "search-app/1.0"

# Load API key from environment variable
with open("./keys.json", "r") as file:
        data = json.load(file)
TAVILY_API_KEY = data["TAVILY_API"]
if not TAVILY_API_KEY:
    logger.error("TAVILY_API_KEY environment variable not set")
    raise ValueError("TAVILY_API_KEY environment variable not set")

async def make_api_request(url: str, params: dict = None, headers: dict = None, json: dict = None) -> dict[str, Any] | None:
    """Make a generic API request with proper error handling."""
    default_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    if headers:
        default_headers.update(headers)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if json:
                response = await client.post(url, json=json, headers=default_headers)
            else:
                response = await client.get(url, params=params, headers=default_headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request failed for {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
        return None

@mcp.tool()
async def wiki_search(query: str, limit: int = 3) -> str:
    """Search Wikipedia for articles."""
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": limit
        }
        
        data = await make_api_request(WIKI_API_BASE, params=params)
        
        if not data or "query" not in data or not data["query"]["search"]:
            return "No Wikipedia articles found for your query."
        
        results = []
        for item in data["query"]["search"]:
            title = item["title"]
            snippet = item["snippet"].replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
            results.append(f"Title: {title}\nSummary: {snippet}\nURL: {url}")
        
        return "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error in wiki_search: {e}")
        return "Failed to search Wikipedia due to an internal error."

@mcp.tool()
async def internet_search(query: str, limit: int = 3, include_raw_content: bool = False) -> str:
    """Search the internet using Tavily API."""
    try:
        request_data = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "include_raw_content": include_raw_content,
            "include_images": False,
            "max_results": limit
        }
        
        data = await make_api_request(f"{TAVILY_API_BASE}/search", json=request_data)
        
        if not data:
            return "Failed to perform internet search. Please try again later."
        
        results = []
        
        if data.get("answer"):
            results.append(f"Quick Answer: {data['answer']}")
        
        if data.get("results"):
            for idx, result in enumerate(data["results"][:limit], 1):
                result_str = f"{idx}. {result.get('title', 'No title')}\n   URL: {result.get('url', 'No URL')}"
                if result.get("content"):
                    result_str += f"\n   Content: {result['content'][:500]}..."  # Truncate content
                results.append(result_str)
        
        if data.get("follow_up_questions"):
            results.append("\nSuggested follow-up questions:")
            results.extend(f"- {q}" for q in data["follow_up_questions"])
        
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        logger.error(f"Error in internet_search: {e}")
        return "Failed to perform internet search due to an internal error."

@mcp.tool()
async def yahoo_finance_search(symbol: str, period: str = "1mo") -> str:
    """Get stock information from Yahoo Finance."""
    try:
        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"]
        if period not in valid_periods:
            return f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        
        params = {
            "symbol": symbol,
            "range": period,
            "interval": "1d",
            "includePrePost": "false"
        }
        
        data = await make_api_request(f"{YAHOO_FINANCE_BASE}{symbol}", params=params)
        
        if not data or "chart" not in data or not data["chart"]["result"]:
            return f"Could not retrieve data for symbol {symbol}"
        
        result = data["chart"]["result"][0]
        meta = result["meta"]
        indicators = result["indicators"]["quote"][0]
        
        timestamps = result["timestamp"]
        dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
        
        latest_idx = -1
        latest_date = dates[latest_idx]
        latest_open = indicators["open"][latest_idx]
        latest_high = indicators["high"][latest_idx]
        latest_low = indicators["low"][latest_idx]
        latest_close = indicators["close"][latest_idx]
        latest_volume = indicators["volume"][latest_idx]
        
        response = [
            f"Stock: {meta['symbol']} ({meta['exchangeName']})",
            f"Currency: {meta['currency']}",
            f"Current Price: {meta['regularMarketPrice']}",
            f"Previous Close: {meta['chartPreviousClose']}",
            "\nLatest Trading Day:",
            f"Date: {latest_date}",
            f"Open: {latest_open}",
            f"High: {latest_high}",
            f"Low: {latest_low}",
            f"Close: {latest_close}",
            f"Volume: {latest_volume}"
        ]
        
        return "\n".join(response)
    except Exception as e:
        logger.error(f"Error in yahoo_finance_search: {e}")
        return f"Failed to retrieve finance data for {symbol} due to an internal error."

if __name__ == "__main__":
    try:
        logger.info("Starting MCP server...")
        mcp.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise