"""
Basic HTTP Client Examples using the requests library

This module demonstrates fundamental concepts of working with HTTP APIs:
- Basic GET requests
- Query parameters
- Headers
- Response handling
- Error handling
"""

import requests
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Base URL for JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"

def basic_get_request() -> Dict[str, Any]:
    """
    Demonstrates a basic GET request to fetch todos.
    
    Returns:
        Dict containing the response data
    """
    response = requests.get(f"{BASE_URL}/todos/1")
    
    # Check if request was successful
    response.raise_for_status()
    
    return response.json()

def get_with_query_params(user_id: int = 1) -> list[Dict[str, Any]]:
    """
    Demonstrates GET request with query parameters.
    
    Args:
        user_id: ID of the user whose todos to fetch
        
    Returns:
        List of todos for the specified user
    """
    params = {
        "userId": user_id,
        "completed": True
    }
    response = requests.get(f"{BASE_URL}/todos", params=params)
    response.raise_for_status()
    
    return response.json()

def get_with_headers() -> Dict[str, Any]:
    """
    Demonstrates GET request with custom headers.
    
    Returns:
        Dict containing the response data
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "RutterInterviewPrep/1.0"
    }
    
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    response.raise_for_status()
    
    return response.json()

def handle_errors() -> Optional[Dict[str, Any]]:
    """
    Demonstrates error handling in API requests.
    
    Returns:
        Dict containing the response data if successful, None if error occurs
    """
    try:
        # This will fail as post 999 doesn't exist
        response = requests.get(f"{BASE_URL}/posts/999")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def create_post(title: str, body: str, user_id: int = 1) -> Dict[str, Any]:
    """
    Demonstrates POST request to create a new resource.
    
    Args:
        title: Post title
        body: Post body
        user_id: User ID
        
    Returns:
        Dict containing the created post data
    """
    data = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    
    response = requests.post(f"{BASE_URL}/posts", json=data)
    response.raise_for_status()
    
    return response.json()

def update_post(post_id: int, title: str, body: str) -> Dict[str, Any]:
    """
    Demonstrates PUT request to update a resource.
    
    Args:
        post_id: ID of the post to update
        title: New title
        body: New body
        
    Returns:
        Dict containing the updated post data
    """
    data = {
        "title": title,
        "body": body
    }
    
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=data)
    response.raise_for_status()
    
    return response.json()

def delete_post(post_id: int) -> bool:
    """
    Demonstrates DELETE request to remove a resource.
    
    Args:
        post_id: ID of the post to delete
        
    Returns:
        bool indicating success
    """
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    return response.status_code == 200

if __name__ == "__main__":
    # Example usage
    print("Basic GET Request:")
    print(json.dumps(basic_get_request(), indent=2))
    
    print("\nGET with Query Parameters:")
    print(json.dumps(get_with_query_params(), indent=2))
    
    print("\nGET with Headers:")
    print(json.dumps(get_with_headers(), indent=2))
    
    print("\nError Handling:")
    handle_errors()
    
    print("\nCreate Post:")
    new_post = create_post(
        title="Test Post",
        body="This is a test post created at " + datetime.now().isoformat()
    )
    print(json.dumps(new_post, indent=2))
    
    print("\nUpdate Post:")
    updated_post = update_post(
        post_id=1,
        title="Updated Title",
        body="Updated body content"
    )
    print(json.dumps(updated_post, indent=2))
    
    print("\nDelete Post:")
    print(f"Success: {delete_post(1)}") 