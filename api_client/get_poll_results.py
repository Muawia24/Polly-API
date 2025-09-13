import requests
import json
from typing import Dict, Optional, Tuple, List


def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000") -> Dict:
    """
    Get poll results from the /polls/{poll_id}/results endpoint.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict: Poll results following the PollResults schema
        
    Raises:
        ValueError: If validation fails or response indicates an error
        requests.exceptions.RequestException: If the request fails
    """
    url = f"{base_url}/polls/{poll_id}/results"
    
    # Validate parameters
    if not poll_id or poll_id <= 0:
        raise ValueError("Poll ID must be a positive integer")
    
    try:
        # Make the GET request
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError("Poll not found")
        else:
            response.raise_for_status()  # Raises an exception for other HTTP errors
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to get poll results: {str(e)}")


def get_poll_results_with_error_handling(poll_id: int, base_url: str = "http://localhost:8000") -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Get poll results with comprehensive error handling.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Tuple[bool, Optional[Dict], Optional[str]]: 
            - success (bool): True if fetch was successful, False otherwise
            - results_data (Optional[Dict]): Poll results if successful, None otherwise
            - error_message (Optional[str]): Error message if failed, None otherwise
    """
    url = f"{base_url}/polls/{poll_id}/results"
    
    # Validate parameters
    if not poll_id or poll_id <= 0:
        return False, None, "Poll ID must be a positive integer"
    
    try:
        # Make the GET request
        response = requests.get(url)
        
        if response.status_code == 200:
            results_data = response.json()
            return True, results_data, None
        elif response.status_code == 404:
            return False, None, "Poll not found"
        else:
            error_message = f"HTTP {response.status_code}: {response.reason}"
            try:
                error_detail = response.json()
                if isinstance(error_detail, dict) and "detail" in error_detail:
                    error_message = error_detail["detail"]
            except:
                pass
            return False, None, error_message
            
    except requests.exceptions.ConnectionError:
        return False, None, "Connection error: Could not connect to the server"
    except requests.exceptions.Timeout:
        return False, None, "Request timeout: Server took too long to respond"
    except requests.exceptions.RequestException as e:
        return False, None, f"Request error: {str(e)}"
    except json.JSONDecodeError:
        return False, None, "Invalid JSON response from server"
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"


def format_poll_results(results_data: Dict) -> str:
    """
    Helper function to format poll results in a readable way.
    
    Args:
        results_data (Dict): Poll results data from the API
        
    Returns:
        str: Formatted string representation of the results
    """
    if not results_data:
        return "No results data available"
    
    poll_id = results_data.get("poll_id", "Unknown")
    question = results_data.get("question", "Unknown question")
    results = results_data.get("results", [])
    
    output = f"Poll #{poll_id}: {question}\n"
    output += "=" * (len(output) - 1) + "\n\n"
    
    if not results:
        output += "No votes cast yet.\n"
        return output
    
    # Sort results by vote count (descending)
    sorted_results = sorted(results, key=lambda x: x.get("vote_count", 0), reverse=True)
    
    total_votes = sum(result.get("vote_count", 0) for result in sorted_results)
    output += f"Total votes: {total_votes}\n\n"
    
    for i, result in enumerate(sorted_results, 1):
        option_id = result.get("option_id", "Unknown")
        text = result.get("text", "Unknown option")
        vote_count = result.get("vote_count", 0)
        
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        output += f"{i}. {text}\n"
        output += f"   Votes: {vote_count} ({percentage:.1f}%)\n"
        output += f"   Option ID: {option_id}\n\n"
    
    return output


def get_poll_results_summary(poll_id: int, base_url: str = "http://localhost:8000") -> str:
    """
    Get poll results and return a formatted summary.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        str: Formatted summary of poll results
        
    Raises:
        ValueError: If poll not found or validation fails
        requests.exceptions.RequestException: If the request fails
    """
    results_data = get_poll_results(poll_id, base_url)
    return format_poll_results(results_data)


# Example usage
if __name__ == "__main__":
    
    # Example 1: Get poll results (Simple version)
    print("Example 1: Get Poll Results (Simple)")
    try:
        results = get_poll_results(poll_id=1)
        print("Raw results data:")
        print(json.dumps(results, indent=2))
        
        print("\nFormatted results:")
        print(format_poll_results(results))
        
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 2: Get poll results with error handling
    print("Example 2: Get Poll Results (With Error Handling)")
    success, results_data, error = get_poll_results_with_error_handling(poll_id=1)
    
    if success:
        print("Poll results retrieved successfully:")
        print(format_poll_results(results_data))
        
        # Show some statistics
        if results_data and "results" in results_data:
            results_list = results_data["results"]
            total_votes = sum(r.get("vote_count", 0) for r in results_list)
            most_popular = max(results_list, key=lambda x: x.get("vote_count", 0))
            
            print(f"Statistics:")
            print(f"- Total votes cast: {total_votes}")
            print(f"- Most popular option: {most_popular.get('text', 'Unknown')} ({most_popular.get('vote_count', 0)} votes)")
            print(f"- Number of options: {len(results_list)}")
    else:
        print(f"Failed to get poll results: {error}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 3: Get formatted summary directly
    print("Example 3: Get Formatted Summary")
    try:
        summary = get_poll_results_summary(poll_id=1)
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 4: Demonstrate error cases
    print("Example 4: Error Cases")
    
    # Test with invalid poll ID
    try:
        results = get_poll_results(poll_id=999)
    except ValueError as e:
        print(f"Expected error with invalid poll ID: {e}")
    
    # Test with error handling for non-existent poll
    success, results_data, error = get_poll_results_with_error_handling(poll_id=999)
    if not success:
        print(f"Expected error with non-existent poll: {error}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 5: Compare multiple polls
    print("Example 5: Compare Multiple Polls")
    poll_ids = [1, 2, 3]
    
    for poll_id in poll_ids:
        print(f"--- Poll {poll_id} ---")
        success, results_data, error = get_poll_results_with_error_handling(poll_id=poll_id)
        
        if success:
            question = results_data.get("question", "Unknown")
            total_votes = sum(r.get("vote_count", 0) for r in results_data.get("results", []))
            print(f"Question: {question}")
            print(f"Total votes: {total_votes}")
            print()
        else:
            print(f"Error: {error}")
            print()
