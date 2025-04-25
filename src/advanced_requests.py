"""
Advanced HTTP Client Examples using the requests library

This module demonstrates advanced concepts and best practices:
- Session management
- Rate limiting
- Retries
- Timeouts
- Authentication
- Pagination
- Response streaming
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Dict, Any, List, Generator
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URLs for different APIs
JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
GITHUB_API_URL = "https://api.github.com"

class RateLimitedSession:
    """
    A session class that implements rate limiting and retries.
    """
    def __init__(self, requests_per_second: float = 1.0):
        self.session = requests.Session()
        self.requests_per_second = requests_per_second
        self.last_request_time = 0
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make a request with rate limiting and retries.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional arguments for requests.request
            
        Returns:
            Response object
        """
        # Implement rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < 1/self.requests_per_second:
            time.sleep(1/self.requests_per_second - elapsed)
        
        response = self.session.request(method, url, **kwargs)
        self.last_request_time = time.time()
        return response

def handle_pagination(url: str, params: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
    """
    Demonstrates handling paginated API responses.
    
    Args:
        url: API endpoint URL
        params: Query parameters
        
    Yields:
        Items from paginated responses
    """
    session = RateLimitedSession()
    page = 1
    params = params or {}
    
    while True:
        params["page"] = page
        response = session.request("GET", url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break
            
        for item in data:
            yield item
            
        page += 1

def stream_large_response(url: str) -> Generator[bytes, None, None]:
    """
    Demonstrates streaming large responses.
    
    Args:
        url: URL to stream from
        
    Yields:
        Chunks of the response
    """
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

def github_api_example() -> List[Dict[str, Any]]:
    """
    Demonstrates working with the GitHub API including authentication.
    
    Returns:
        List of repositories
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    session = RateLimitedSession(requests_per_second=0.5)
    response = session.request(
        "GET",
        f"{GITHUB_API_URL}/user/repos",
        headers=headers,
        params={"sort": "updated", "per_page": 100}
    )
    response.raise_for_status()
    
    return response.json()

def handle_timeouts() -> Optional[Dict[str, Any]]:
    """
    Demonstrates handling request timeouts.
    
    Returns:
        Response data if successful, None if timeout occurs
    """
    try:
        response = requests.get(
            f"{JSONPLACEHOLDER_URL}/posts/1",
            timeout=(3.05, 27)  # (connect timeout, read timeout)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def batch_requests(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Demonstrates making multiple requests efficiently.
    
    Args:
        urls: List of URLs to request
        
    Returns:
        List of response data
    """
    session = RateLimitedSession()
    responses = []
    
    for url in urls:
        response = session.request("GET", url)
        response.raise_for_status()
        responses.append(response.json())
    
    return responses

if __name__ == "__main__":
    # Example usage
    print("Handling Pagination:")
    for post in handle_pagination(f"{JSONPLACEHOLDER_URL}/posts"):
        print(json.dumps(post, indent=2))
        break  # Just show first item for demo
    
    print("\nStreaming Large Response:")
    for chunk in stream_large_response(f"{JSONPLACEHOLDER_URL}/posts"):
        print(f"Received chunk of size: {len(chunk)}")
        break  # Just show first chunk for demo
    
    print("\nHandling Timeouts:")
    result = handle_timeouts()
    if result:
        print(json.dumps(result, indent=2))
    
    print("\nBatch Requests:")
    urls = [
        f"{JSONPLACEHOLDER_URL}/posts/{i}" for i in range(1, 4)
    ]
    results = batch_requests(urls)
    for result in results:
        print(json.dumps(result, indent=2)) 