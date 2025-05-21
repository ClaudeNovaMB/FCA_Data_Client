# FCA API Client

This project is a lightweight, scriptable client for querying and retrieving firm and individual data from the FCA’s Financial Services Register API. It provides a structured way to interact with the API, including proper authentication and response parsing.

## Features

- **Authenticated API Requests**: Handles authentication using API credentials stored in environment variables.
- **Data Retrieval**: Methods for retrieving firm and individual data based on Firm Reference Numbers (FRNs).
- **Structured Response Parsing**: Parses API responses into structured formats for easy access to relevant data.
- **Utility Functions**: Includes functions for rate limiting, retry logic, and logging.

## Other tools I used (The best relational DB in the world IMO)
1. Docker
2. Containerised TimeScaleDB

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fca-api-client.git
   cd fca-api-client
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Register on the FCA Registrations website to obtain an API key:
   - Visit the [FCA Registrations website](https://register.fca.org.uk/Developer/s/).
   - Sign up for an account if you don’t already have one.
   - Navigate to the API section and generate an API key.

4. Create a `.env` file in the root of the project directory and add the following variables:
   ```
   X_AUTH_EMAIL='your@email.com'  # Your registered email for the FCA API
   X_AUTH_KEY='your_api_key'      # The API key obtained from the FCA Registrations website
   DATABASE_URL='your_database_connection_string'  # Connection string for your database
   ```
   Replace the placeholder values with your actual credentials.

   **Note:** Do not commit the `.env` file to version control to keep your credentials secure. You can add `.env` to your `.gitignore` file to ensure it is ignored by Git.


## Usage

To use the client, you can import the necessary modules and create an instance of the API client. Here’s a simple example:

```python
from src.client import FCAClient

client = FCAClient()
firm_data = client.get_firm_data(frn='123456')
print(firm_data)
```

## Testing

To run the tests, use the following command:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.