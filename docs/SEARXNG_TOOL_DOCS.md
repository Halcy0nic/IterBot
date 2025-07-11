# SearXNG Tool for IterBot

## Overview

The SearXNG tool provides web search capabilities for IterBot agents using the SearXNG metasearch engine. SearXNG is a privacy-focused search engine that aggregates results from multiple search engines without tracking users.

## Features

- **Configurable endpoint**: Connect to local or remote SearXNG instances
- **Multiple search engines**: Specify which search engines to use
- **Result limiting**: Control the number of results returned
- **Error handling**: Graceful handling of connection and API errors
- **HTTPX client**: Modern async-capable HTTP client with connection pooling

## Installation Requirements

```bash
pip install httpx
```

You also need a running SearXNG instance. See [SearXNG Installation Guide](https://github.com/searxng/searxng) for setup instructions.

## Quick Start

### Local SearXNG Instance

```python
from iterbot import IterBotReactAgent
from IterBotTools import SearXNGTool, get_default_tools

# Add search capability to default tools
tools = get_default_tools()
tools["search_web"] = SearXNGTool.search_web

# Create agent with search capability
agent = IterBotReactAgent(
    model='llama3.2',
    tools=tools,
    custom_system_prompt="You can search the web for current information. Always cite sources."
)

# Use the agent
result = agent.run("Search for the latest developments in AI")
print(result)
```

## API Reference

### SearXNGTool.search_web()

```python
SearXNGTool.search_web(
    query: str,
    url: str = "http://127.0.0.1:8080/search",
    num_results: int = 4,
    search_engines: List[str] = None
) -> str
```

**Parameters:**
- `query` (str): Search query to execute
- `url` (str): Search API endpoint URL (default: local server)
- `num_results` (int): Maximum number of results to return (default: 4)
- `search_engines` (list): List of search engine names (optional)

**Returns:**
- `str`: Formatted search results with titles, URLs, and content snippets

## Usage Examples

### Basic Search

```python
from IterBotTools import SearXNGTool

# Simple search with defaults
result = SearXNGTool.search_web("Python programming")
print(result)
```

### Custom Configuration

```python
# Search with specific parameters
result = SearXNGTool.search_web(
    query="machine learning",
    num_results=6,
    search_engines=["google", "bing", "duckduckgo"]
)
print(result)
```

### Remote SearXNG Instance

```python
# Search using remote instance
result = SearXNGTool.search_web(
    query="quantum computing",
    url="https://searx.example.com/search",
    num_results=5
)
print(result)
```

### Integration with IterBot

```python
from iterbot import IterBotReactAgent
from IterBotTools import SearXNGTool, get_default_tools

# Create custom search functions for different use cases
def search_academic(query: str) -> str:
    """Search for academic content."""
    return SearXNGTool.search_web(
        query=query,
        search_engines=["google scholar", "semantic scholar", "arxiv"],
        num_results=6
    )

def search_news(query: str) -> str:
    """Search for news content."""
    return SearXNGTool.search_web(
        query=query,
        search_engines=["google news", "bing news"],
        num_results=5
    )

def search_general(query: str) -> str:
    """General web search."""
    return SearXNGTool.search_web(query=query)

# Create specialized agent
tools = {
    "search_academic": search_academic,
    "search_news": search_news,
    "search_general": search_general
}
tools.update(get_default_tools())

agent = IterBotReactAgent(
    tools=tools,
    custom_system_prompt="""You have specialized search capabilities:
    - search_academic: For scholarly content
    - search_news: For current news
    - search_general: For general web content
    Choose the appropriate search method based on the user's needs."""
)
```

## Available Search Engines

Common search engines supported by SearXNG (availability depends on your SearXNG configuration):

- `google`
- `bing`
- `duckduckgo`
- `startpage`
- `google scholar`
- `semantic scholar`
- `arxiv`
- `google news`
- `bing news`
- `reddit`
- `stackoverflow`
- `github`
- `wikipedia`

Check your SearXNG instance's `/preferences` page for the complete list of available engines.

## Error Handling

The SearXNG tool includes comprehensive error handling:

- **Connection errors**: When SearXNG instance is not reachable
- **HTTP errors**: When the search API returns error status codes
- **Missing dependencies**: When the `httpx` library is not installed
- **Invalid responses**: When the API response format is unexpected

Example error messages:
```
"Connection error: Could not connect to SearXNG at http://127.0.0.1:8080/search. Make sure SearXNG is running."
"Error: 'httpx' library is required for SearXNG search. Install with: pip install httpx"
"HTTP error: 500 - Internal Server Error"
```

## SearXNG Setup

### Quick Local Setup with Docker

```bash
# Clone SearXNG
git clone https://github.com/searxng/searxng.git
cd searxng

# Run with Docker
docker compose up -d
```

SearXNG will be available at `http://localhost:8080`

### Configuration

Create a custom `settings.yml` for your SearXNG instance:

```yaml
# Basic configuration
server:
  port: 8080
  bind_address: "0.0.0.0"

search:
  safe_search: 0
  autocomplete: ""
  default_lang: "en"
  formats:
    - html
    - json

engines:
  - name: google
    disabled: false
  - name: bing
    disabled: false
  - name: duckduckgo
    disabled: false
```

## Best Practices

1. **Rate limiting**: Be mindful of search frequency to avoid overwhelming the SearXNG instance
2. **Engine selection**: Choose appropriate engines for your use case (academic, news, general)
3. **Result limits**: Use reasonable `num_results` values to balance thoroughness with performance
4. **Error handling**: Always handle the case where SearXNG might be unavailable
5. **Privacy**: Use SearXNG instances you trust, as they can see your search queries

## Troubleshooting

### SearXNG Not Responding
- Check if SearXNG is running: `curl http://localhost:8080`
- Verify the URL in your search function
- Check SearXNG logs for errors

### No Results Returned
- Verify your search query is valid
- Check if the specified engines are enabled in SearXNG
- Try with different search engines

### Slow Performance
- Reduce `num_results`
- Use fewer search engines
- Check your SearXNG instance performance
- Consider using a local SearXNG instance

## Integration with Other Tools

```python
# Combine with time tools for time-aware searches
from IterBotTools import TimeTool

def time_aware_search(query: str) -> str:
    current_date = TimeTool.get_current_date()
    enhanced_query = f"{query} after:{current_date}"
    return SearXNGTool.search_web(enhanced_query)

tools = get_default_tools()
tools["search_recent"] = time_aware_search
```
