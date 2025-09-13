import requests
import json
from typing import Dict, Optional, Tuple, List
from datetime import datetime


def fetch_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> List[Dict]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        skip (int): Number of items to skip for pagination (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        List[Dict]: List of poll objects following the PollOut schema
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response indicates an error
    """
    url = f"{base_url}/polls"
    
    # Validate parameters
    if skip < 0:
        raise ValueError(400,"Skip parameter must be non-negative")
    if limit <= 0:
        raise ValueError(400,"Limit parameter must be positive")
    
    # Prepare query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises an exception for HTTP errors
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to fetch polls")


if __name__ == "__main__":
    
    
    # Example 2: Fetch polls with simple version
    print("Example 2: Fetch Polls (Simple)")
    try:
        polls = fetch_polls(skip=0, limit=0)
        print(f"Fetched {len(polls)} polls:")
        for poll in polls:
            print(f"  - Poll {poll['id']}: {poll['question']}")
            print(f"    Created: {poll['created_at']}")
            print(f"    Options: {len(poll['options'])}")
            for option in poll['options']:
                print(f"      * {option['text']}")
            print()
    except ValueError as e:
        print(f"Validation error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")