"""SearXNG search tool for IterBot."""

from typing import List

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    httpx = None


class SearXNGTool:
    """Tool for searching the web using SearXNG search engine."""
    
    @staticmethod
    def search_web(
        query: str,
        url: str = "http://127.0.0.1:8080/search",
        num_results: int = 4,
        search_engines: List[str] = None
    ) -> str:
        """Search the web with configurable parameters using HTTPX
        
        Args:
            query (str): Search query to execute
            url (str): Search API endpoint URL (default: local server)
            num_results (int): Maximum number of results to return (default: 4)
            search_engines (list): List of search engine names (default: empty list)
            
        Returns:
            str: Formatted search results with titles, URLs, and snippets
        """
        if not HTTPX_AVAILABLE:
            return "Error: 'httpx' library is required for SearXNG search. Install with: pip install httpx"
            
        if search_engines is None:
            search_engines = []
            
        try:
            params = {
                "q": query,
                "format": "json"
            }
            
            # Only add parameters if they have values
            if num_results:
                params["num_results"] = num_results
            if search_engines:
                params["engines"] = ",".join(search_engines)
            
            with httpx.Client() as client:  # Context manager for connection pooling
                resp = client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                if data.get("results"):
                    return "\n".join(
                        f"{r.get('title', 'No title')}: {r.get('url', 'No URL')} : {r.get('content', 'No content')}"
                        for r in data["results"][:num_results]
                    )
            return "No results found."
        except httpx.ConnectError:
            return f"Connection error: Could not connect to SearXNG at {url}. Make sure SearXNG is running."
        except httpx.HTTPStatusError as e:
            return f"HTTP error: {e.response.status_code} - {e.response.reason_phrase}"
        except httpx.RequestError as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"Search error: {str(e)}"
