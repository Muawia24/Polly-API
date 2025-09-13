import requests
import json
from typing import Dict, Optional, Tuple, List
from datetime import datetime


def register_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Simple version of register_user that raises exceptions on failure.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict: User data on successful registration
        
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response indicates an error (like username already exists)
    """
    url = f"{base_url}/register"
    if not username or not password:
        raise ValueError(400,"Username and password are required")
    payload = {"username": username, "password": password}
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise ValueError(400,"Username already registered")
    else:
        response.raise_for_status()  # Raises an exception for other HTTP errors




# Example usage
if __name__ == "__main__":
    
    # Example 1: Using the simple version with exceptions
    print("Example 1: User Registration")
    try:
        user_data = register_user("testuser4", "testpassword456")
        print(f"Registration successful! User ID: {user_data['id']}, Username: {user_data['username']}")
    except ValueError as e:
        print(f"Registration failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
