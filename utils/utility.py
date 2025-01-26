import requests
import os, json, asyncio
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException, Timeout, ConnectionError
from flask import session

load_dotenv()

SMARTAPI_BASE_URL = os.getenv("SMARTAPI_BASE_URL")


async def register_user(fullname: str, username: str, password: str):
    data = {
        'fullname': fullname,
        'username': username,
        'password': password
    }

    smartapi_url = SMARTAPI_BASE_URL + "users/add_user"
    print(smartapi_url)
    # Create a session object
    network_session = requests.Session()

    # Set the Content-Type header to application/json for all requests in the session
    network_session.headers.update({'Content-Type': 'application/json'})

    # Send a POST request with JSON data using the session object
    response = network_session.post(url=smartapi_url, json=data)
    print(response.json())
    return response.json()


async def login_user(username: str, password: str):
    try:
        params = {
            'username': username,
            'password': password
        }

        smartapi_url = SMARTAPI_BASE_URL + "users/login"
        print(f"Attempting to log in with URL: {smartapi_url}")

        # Create a session object
        network_session = requests.Session()

        # Set the Content-Type header to application/json for all requests in the session
        network_session.headers.update({'Content-Type': 'application/json'})

        # Send a GET request with parameters
        response = network_session.get(url=smartapi_url, params=params)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Return the JSON response if the request was successful
        return {"success": True, "data": response.json()}

    except HTTPError as http_err:
        return {
            "success": False,
            "error": "HTTP error occurred",
            "details": str(http_err),
            "status_code": response.status_code if 'response' in locals() else None,
        }
    except ConnectionError as conn_err:
        return {
            "success": False,
            "error": "Connection error occurred",
            "details": str(conn_err),
        }
    except Timeout as timeout_err:
        return {
            "success": False,
            "error": "Request timed out",
            "details": str(timeout_err),
        }
    except RequestException as req_err:
        return {
            "success": False,
            "error": "An error occurred during the request",
            "details": str(req_err),
        }
    except Exception as e:
        return {
            "success": False,
            "error": "An unexpected error occurred",
            "details": str(e),
        }


async def check_user_status(username: str):
    params = {
        'username': username
    }

    smartapi_url = SMARTAPI_BASE_URL + "users/check_user_status"
    print(smartapi_url)
    # Create a session object
    network_session = requests.Session()

    # Set the Content-Type header to application/json for all requests in the session
    network_session.headers.update({'Content-Type': 'application/json'})

    # Send a POST request with JSON data using the session object
    response = network_session.get(url=smartapi_url, params=params)
    print(response.json())
    return response.json() # Replace with the actual base URL


async def get_all_aiagents():
    """
    Fetches all AI agents using an HTTP GET request with a bearer token.

    Returns:
        dict: A dictionary containing the response JSON or error details.
    """
    smartapi_url = SMARTAPI_BASE_URL + "aiagents/get_aiagents"
    print(f"Requesting URL: {smartapi_url}")

    # Bearer token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmdlbG1heEBob3RtYWlsLmNvbSIsInBhc3N3b3JkIjoiUGF0cmljayIsImV4cCI6MTczODUwNjYxM30.guuHhfcsB3KsYYantSeLa7kE-y8nguWUx3X2y3C3lFk"
    print(session['token'])
    # Headers for the request
    # session.get('token')
    headers = {
        "Authorization": f"Bearer {session.get('token')}",  # Fixed incorrect formatting of the token
        "Content-Type": "application/json",
    }

    try:
        # Create a session object
        with requests.Session() as network_session:
            # Update session headers
            network_session.headers.update(headers)

            # Send a GET request
            response = network_session.get(url=smartapi_url)

            # Raise an exception for HTTP error responses (4xx and 5xx)
            response.raise_for_status()

            # Return the parsed JSON response
            return response.json()

    except requests.exceptions.RequestException as e:
        # Catch all exceptions related to HTTP requests
        print(f"HTTP request failed: {e}")
        return {"error": "HTTP request failed", "details": str(e)}

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Failed to parse JSON response: {e}")
        return {"error": "Failed to parse JSON response", "details": str(e)}

    except Exception as e:
        # Catch all other exceptions
        print(f"An unexpected error occurred: {e}")
        return {"error": "Unexpected error", "details": str(e)}


def has_less_than_two_words(s):
    words = s.split()  # Split the string by whitespace into words
    return len(words) < 2


def does_not_contain_at(sx):
    return "@" not in sx


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_user("angelmax@hotmail.com", "Patrick"))
