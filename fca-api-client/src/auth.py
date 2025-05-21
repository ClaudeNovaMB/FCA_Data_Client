import os

def get_auth_headers():
    """
    Retrieve authentication headers for API requests.

    This function constructs the headers required for API authentication using
    environment variables. It raises a `ValueError` if the credentials are
    not set in the environment variables.

    Returns:
        dict: A dictionary containing the authentication headers.
    """
    api_email = os.getenv('X_AUTH_EMAIL')
    api_key = os.getenv('X_AUTH_KEY')

    if not api_email or not api_key:
        raise ValueError("API credentials are not set in environment variables.")

    return {
        'x-auth-email': api_email,
        'x-auth-key': api_key,
        'accept': 'application/json',
    }