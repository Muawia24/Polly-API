import requests
import json
from typing import Dict, Optional, Tuple


def vote_on_poll(poll_id: int, option_id: int, access_token: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Cast a vote on an existing poll via the /polls/{poll_id}/vote endpoint.
    
    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        access_token (str): JWT access token for authentication
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict: Vote data following the VoteOut schema
        
    Raises:
        ValueError: If validation fails or response indicates an error
        requests.exceptions.RequestException: If the request fails
    """
    url = f"{base_url}/polls/{poll_id}/vote"
    
    # Validate parameters
    if not poll_id or poll_id <= 0:
        raise ValueError("Poll ID must be a positive integer")
    if not option_id or option_id <= 0:
        raise ValueError("Option ID must be a positive integer")
    if not access_token:
        raise ValueError("Access token is required for voting")
    
    # Prepare the request payload
    payload = {
        "option_id": option_id
    }
    
    # Set headers with authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ValueError("Unauthorized: Invalid or expired access token")
        elif response.status_code == 404:
            raise ValueError("Poll or option not found")
        else:
            response.raise_for_status()  # Raises an exception for other HTTP errors
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to vote on poll: {str(e)}")



def login_and_get_token(username: str, password: str, base_url: str = "http://localhost:8000") -> str:
    """
    Helper function to login and get an access token for voting.
    
    Args:
        username (str): The username for login
        password (str): The password for login
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        str: Access token for authentication
        
    Raises:
        ValueError: If login fails
        requests.exceptions.RequestException: If the request fails
    """
    url = f"{base_url}/login"
    
    # Prepare form data for login (as per OpenAPI spec)
    form_data = {
        "username": username,
        "password": password
    }
    
    try:
        # Make the POST request with form data
        response = requests.post(url, data=form_data)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data["access_token"]
        elif response.status_code == 400:
            raise ValueError("Incorrect username or password")
        else:
            response.raise_for_status()  # Raises an exception for other HTTP errors
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to login: {str(e)}")


# Example usage
if __name__ == "__main__":
    
    # Example 1: Login and vote (Simple version)
    print("Example 1: Login and Vote (Simple)")
    try:
        # First, login to get an access token
        print("Logging in...")
        token = login_and_get_token("testuser4", "testpassword456")
        print(f"Login successful! Token: {token[:20]}...")
        
        # Now vote on a poll (assuming poll_id=1 and option_id=1)
        print("Voting on poll...")
        vote_data = vote_on_poll(poll_id=1, option_id=1, access_token=token)
        print(f"Vote successful! Vote ID: {vote_data['id']}")
        print(f"Voted on option {vote_data['option_id']} at {vote_data['created_at']}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Vote with error handling
    print("Example 2: Vote with Error Handling")
    try:
        # Login
        token = login_and_get_token("testuser4", "testpassword456")
        
        # Vote with error handling
        success, vote_data, error = vote_on_poll_with_error_handling(
            poll_id=1, 
            option_id=2, 
            access_token=token
        )
        
        if success:
            print(f"Vote successful! Vote ID: {vote_data['id']}")
            print(f"User ID: {vote_data['user_id']}")
            print(f"Option ID: {vote_data['option_id']}")
            print(f"Created at: {vote_data['created_at']}")
        else:
            print(f"Vote failed: {error}")
            
    except Exception as e:
        print(f"Login failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Demonstrate error cases
    print("Example 3: Error Cases")
    
    # Test with invalid poll ID
    try:
        token = login_and_get_token("testuser4", "testpassword456")
        vote_data = vote_on_poll(poll_id=999, option_id=1, access_token=token)
    except ValueError as e:
        print(f"Expected error with invalid poll ID: {e}")
    
    # Test with invalid token
    try:
        vote_data = vote_on_poll(poll_id=1, option_id=1, access_token="invalid_token")
    except ValueError as e:
        print(f"Expected error with invalid token: {e}")
