# FCA API Client

This project is a lightweight, scriptable client for querying and retrieving firm and individual data from the FCA’s Financial Services Register API. It provides a structured way to interact with the API, including proper authentication and response parsing.

## Features

- **Authenticated API Requests**: Handles authentication using API credentials stored in environment variables.
- **Data Retrieval**: Methods for retrieving firm and individual data based on Firm Reference Numbers (FRNs).
- **Structured Response Parsing**: Parses API responses into structured formats for easy access to relevant data.
- **Utility Functions**: Includes functions for rate limiting, retry logic, and logging.

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

3. Set up your environment variables for API credentials:
   ```
   export FCA_API_KEY='your_api_key'
   ```

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