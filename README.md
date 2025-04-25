# Rutter Interview Preparation - External REST APIs

## Table of Contents

- [Learning Objectives](#learning-objectives)
- [Query Parameters](#query-parameters)
- [HTTP Headers](#http-headers)
- [Authentication Methods](#authentication-methods)
- [Error Handling in Requests](#error-handling-in-requests)
- [Advanced Request Handling](#advanced-request-handling)
  - [Sessions](#sessions)
  - [Retry Strategies](#retry-strategies)
  - [Adapters](#adapters)
  - [Pagination vs Streaming vs Batching](#pagination-vs-streaming-vs-batching)
- [Using .env Files for Authentication](#using-env-files-for-authentication)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Practice APIs](#practice-apis)
- [Contributing](#contributing)

## Learning Objectives

1. **HTTP Client Fundamentals**
   - Understanding HTTP methods (GET, POST, PUT, DELETE)
   - Working with headers and query parameters
   - Handling different response types (JSON, XML, etc.)

2. **API Integration Best Practices**
   - Error handling and status codes
   - Rate limiting and retries
   - Authentication methods (API keys, OAuth, etc.)
   - Pagination handling

3. **Documentation Navigation**
   - Reading and understanding API documentation
   - Working with ambiguous or incomplete documentation
   - Making educated assumptions when documentation is unclear

4. **Real-world Scenarios**
   - Working with different response formats
   - Handling edge cases
   - Debugging API issues
   - Performance considerations

## Query Parameters

Query parameters (params) act as filters to retrieve specific data from the API. They are appended to the URL after a '?' and separated by '&'.

### Common Query Parameter Patterns

1. **Single condition**:
   ```python
   params = {"userId": 1}  # Get todos for user 1
   # URL becomes: /todos?userId=1
   ```

2. **Multiple conditions** (AND logic):
   ```python
   params = {
       "userId": 1,
       "completed": True
   }  # Get completed todos for user 1
   # URL becomes: /todos?userId=1&completed=true
   ```

3. **List of values** (OR logic):
   ```python
   params = {
       "id": [1, 2, 3]
   }  # Get todos with ID 1, 2, or 3
   # URL becomes: /todos?id=1&id=2&id=3
   ```

4. **Range queries** (if API supports):
   ```python
   params = {
       "minPrice": 10,
       "maxPrice": 20
   }  # Get items priced between 10 and 20
   ```

5. **Pagination and sorting**:
   ```python
   params = {
       "page": 1,
       "limit": 10,
       "sort": "created_at"
   }
   ```

### Important Notes About Query Parameters

- Available parameters and their behavior depend on the API
- Always check the API documentation for:
  - Supported parameters
  - Parameter value formats
  - Special operators (>, <, contains, etc.)
  - Pagination methods
  - Sorting options
- The `requests` library automatically handles URL encoding of parameters
- Parameters are case-sensitive in most APIs
- Some APIs have limits on the number or length of parameters

## HTTP Headers

HTTP headers are key-value pairs that provide additional information about the request or response. They can be used for:
- Content negotiation
- Authentication
- Caching
- Rate limiting
- Tracking
- Security

### Common Request Headers

1. **Content-Type and Accept**
   ```python
   headers = {
       "Content-Type": "application/json",  # What we're sending
       "Accept": "application/json"         # What we want to receive
   }
   ```
   - `Content-Type`: Specifies the format of the data being sent
   - `Accept`: Tells the server what format we want the response in

2. **Authentication**
   ```python
   headers = {
       "Authorization": "Bearer your_token_here",
       "API-Key": "your_api_key_here"
   }
   ```
   - Used for various authentication methods
   - Common patterns: Bearer tokens, API keys, Basic auth

3. **User-Agent**
   ```python
   headers = {
       "User-Agent": "MyApp/1.0 (Platform; Version)"
   }
   ```
   - Identifies the client making the request
   - Helps servers track and manage different clients
   - Some APIs require specific User-Agent strings

4. **Rate Limiting and Tracking**
   ```python
   headers = {
       "X-RateLimit-Limit": "100",
       "X-RateLimit-Remaining": "99",
       "X-Request-ID": "unique-id-here"
   }
   ```
   - Used for rate limiting information
   - Request tracking and debugging

5. **Caching**
   ```python
   headers = {
       "If-None-Match": "etag-value",
       "If-Modified-Since": "date-string"
   }
   ```
   - Control caching behavior
   - Reduce unnecessary data transfer

### Important Notes About Headers

- Headers are case-insensitive in HTTP/1.1
- Some APIs require specific headers
- Custom headers often start with `X-` (though this convention is becoming less common)
- Headers can be used for API versioning
- Some headers are automatically added by the `requests` library
- Headers can be used for security features like CORS

## Authentication Methods

### Common Authentication Methods

1. **API Keys**
```python
# .env
API_KEY=sk_test_1234567890abcdefghijklmnopqrstuvwxyz

# Python code
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

headers = {
    "X-API-Key": api_key
    # or
    "Authorization": f"ApiKey {api_key}"
}

response = requests.get(
    "https://api.example.com/data",
    headers=headers
)
```
- Simple string that identifies your application
- Usually provided when you sign up for the API
- Sent in headers with each request
- Easy to implement but less secure
- Example: OpenWeatherMap API key

2. **Bearer Tokens**
```python
# .env
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz

# Python code
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(
    "https://api.github.com/user/repos",
    headers=headers
)
```
- Temporary access tokens
- Can be obtained through OAuth2 or other methods
- Can expire after some time
- More secure than API keys
- Example: GitHub personal access token

3. **Basic Authentication**
```python
# .env
API_USERNAME=admin
API_PASSWORD=secret123

# Python code
import os
import base64
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

# Encode credentials
credentials = base64.b64encode(
    f"{username}:{password}".encode("utf-8")
).decode("utf-8")

headers = {
    "Authorization": f"Basic {credentials}"
}

response = requests.get(
    "https://api.example.com/protected",
    headers=headers
)
```
- Username and password encoded in base64
- Simple but less secure
- Used for basic access control
- Example: Some internal APIs

### OAuth2

OAuth2 is not a separate authentication method, but a framework that results in a Bearer token. It's more complex but more secure than simple API keys.

```python
# OAuth2 Flow Example (Authorization Code)
# 1. Redirect user to authorization URL
auth_url = "https://accounts.google.com/o/oauth2/auth"
params = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "redirect_uri": "http://your-app.com/callback",
    "scope": "email profile",
    "response_type": "code"
}

# 2. After user approves, exchange code for token
token_url = "https://oauth2.googleapis.com/token"
data = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "code": code,
    "redirect_uri": "http://your-app.com/callback",
    "grant_type": "authorization_code"
}

response = requests.post(token_url, data=data)
token_data = response.json()
access_token = token_data["access_token"]

# 3. Use the token as a Bearer token
headers = {
    "Authorization": f"Bearer {access_token}"
}
```

### Other Authentication Methods

4. **JWT (JSON Web Tokens)**
```python
# .env
JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ

# Python code
headers = {
    "Authorization": f"Bearer {os.getenv('JWT_TOKEN')}"
}
```
- Self-contained tokens
- Can include user data
- Signed but not encrypted
- Common in microservices because:
  - No database lookups needed (token contains user data)
  - Each service can verify tokens independently
  - Contains user context (roles, permissions)
  - Enables stateless communication between services
  - Improves scalability and performance

5. **AWS Signature**
```python
# Complex signature calculation required
headers = {
    "Authorization": "AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request, SignedHeaders=host;range;x-amz-date, Signature=fe5f80f77d5fa3beca038a248ff027d0445342fe2855ddc963176630326f1024"
}
```
- Used by AWS services
- Complex signature calculation
- Very secure

### Choosing an Authentication Method

1. **For Public APIs**:
   - API Keys (simple, permanent access)
   - Bearer Tokens (more secure, temporary access)

2. **For User Data**:
   - OAuth2 (user authorization)
   - JWT (self-contained user data)

3. **For Internal Services**:
   - Basic Auth (simple internal systems)
   - JWT (microservices)

4. **For Cloud Services**:
   - AWS Signature (AWS services)
   - Service-specific authentication

## Error Handling in Requests

The `requests` library has several types of exceptions that can occur during API calls. Here's a comprehensive guide to handling them:

### Common Exceptions

1. **HTTPError** (for HTTP status codes >= 400)
```python
try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()  # Raises HTTPError for 4XX/5XX responses
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    # Handle specific status codes
    if e.response.status_code == 404:
        print("Resource not found")
    elif e.response.status_code == 401:
        print("Unauthorized")
    elif e.response.status_code == 429:
        print("Too many requests")
```
- Raised for HTTP status codes 4XX (client errors) and 5XX (server errors)
- Contains the response object with status code and message
- Use `response.raise_for_status()` to trigger this

2. **RequestException** (base class for all requests exceptions)
```python
try:
    response = requests.get("https://api.example.com/data")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    if isinstance(e, requests.exceptions.ConnectionError):
        print("Connection error - check your network")
    elif isinstance(e, requests.exceptions.Timeout):
        print("Request timed out")
```
- Parent class for all requests exceptions
- Use as a catch-all for any request-related error
- Can check specific error types using `isinstance()`

### Other Important Exceptions

3. **ConnectionError**
```python
try:
    response = requests.get("https://api.example.com/data")
except requests.exceptions.ConnectionError as e:
    print("Failed to connect to the server")
    print(f"Error: {e}")
```
- Network problems (DNS failure, refused connection, etc.)
- No internet connection
- Server is down

4. **Timeout**
```python
try:
    response = requests.get(
        "https://api.example.com/data",
        timeout=(3.05, 27)  # (connect timeout, read timeout)
    )
except requests.exceptions.Timeout as e:
    print("Request timed out")
```
- Request takes too long
- Can set different timeouts for connection and reading

5. **SSLError**
```python
try:
    response = requests.get("https://api.example.com/data")
except requests.exceptions.SSLError as e:
    print("SSL certificate verification failed")
```
- SSL/TLS certificate problems
- Common in self-signed certificates

### Best Practices for Error Handling

1. **Specific to General**:
```python
try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    # Handle HTTP errors (4XX, 5XX)
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError as e:
    # Handle connection problems
    print(f"Connection Error: {e}")
except requests.exceptions.Timeout as e:
    # Handle timeouts
    print(f"Timeout Error: {e}")
except requests.exceptions.RequestException as e:
    # Catch-all for any other request-related errors
    print(f"Request failed: {e}")
```

2. **Retry Logic**:
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)
```

3. **Logging Errors**:
```python
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"API request failed: {e}")
    logger.error(f"URL: {e.request.url}")
    logger.error(f"Method: {e.request.method}")
```

### Common HTTP Status Codes to Handle

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error
- 502: Bad Gateway
- 503: Service Unavailable
- 504: Gateway Timeout

## Advanced Request Handling

### Sessions

A `requests.Session()` object allows you to persist certain parameters across requests. It's particularly useful when making multiple requests to the same API.

```python
# Without Session
response1 = requests.get("https://api.example.com/data", headers={"Authorization": "Bearer token"})
response2 = requests.get("https://api.example.com/data", headers={"Authorization": "Bearer token"})  # Repeating headers

# With Session
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})

response1 = session.get("https://api.example.com/data")  # Headers automatically included
response2 = session.get("https://api.example.com/data")  # Headers automatically included
```

Benefits of using Sessions:
- Persists cookies across requests
- Maintains connection pooling (faster)
- Reuses headers and other parameters
- Better for making multiple requests to the same API

### Retry Strategies

The `Retry` class helps handle transient failures. Here are different scenarios:

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Scenario 1: Basic retry for any 5XX error
retry_strategy = Retry(
    total=3,  # Total number of retries
    backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
    status_forcelist=[500, 502, 503, 504]
)

# Scenario 2: Aggressive retry for rate limiting
retry_strategy = Retry(
    total=5,
    backoff_factor=2,  # Wait 2, 4, 8, 16, 32 seconds
    status_forcelist=[429]  # Only retry on rate limits
)

# Scenario 3: Conservative retry for sensitive operations
retry_strategy = Retry(
    total=2,
    backoff_factor=0.5,  # Wait 0.5, 1 second
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]  # Only retry GET requests
)

# Scenario 4: Custom retry for specific error codes
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[408, 429, 500, 502, 503, 504],
    respect_retry_after_header=True  # Honor server's retry-after header
)
```

### Adapters

An adapter is a component that handles the actual HTTP request/response cycle. When you mount an adapter, you're telling the Session which adapter to use for which protocol:

```python
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)

# Mount the adapter for both HTTP and HTTPS
session.mount("http://", adapter)
session.mount("https://", adapter)
```

Why mount adapters?
- Different protocols might need different handling
- You can have different retry strategies for different endpoints
- Allows for protocol-specific optimizations

### Pagination vs Streaming vs Batching

#### Pagination
Use when you need to process all data, but in manageable chunks:

```python
def handle_pagination(url, params=None):
    page = 1
    while True:
        response = requests.get(url, params={"page": page, **(params or {})})
        data = response.json()
        if not data:  # No more data
            break
        for item in data:
            yield item
        page += 1

# Usage
for item in handle_pagination("https://api.example.com/items"):
    process_item(item)
```

Key points about pagination:
- Not all APIs use "page" parameter - some use:
  - `offset` and `limit`
  - `cursor` or `next_token`
  - `since_id` or `max_id`
- Always check API docs for pagination method
- Use when you need ALL the data

#### Streaming
Use when you need to process data as it arrives:

```python
response = requests.get("https://api.example.com/large-file", stream=True)
for chunk in response.iter_content(chunk_size=8192):
    process_chunk(chunk)
```

Use streaming when:
- Response is very large
- You want to process data as it arrives
- Memory efficiency is important
- You don't need all data at once

#### Batching
Use when you need to send multiple requests efficiently:

```python
def batch_requests(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        response = requests.post(
            "https://api.example.com/batch",
            json={"items": batch}
        )
        yield from response.json()
```

Use batching when:
- You need to send multiple related requests
- API has rate limits
- You want to reduce network overhead
- You need to maintain order of operations

### Key Differences and When to Use Each

| Method | Control | Use Case | Memory Usage | Network Usage |
|--------|---------|----------|--------------|---------------|
| Pagination | Client-side | Need all data | Moderate | Sequential |
| Streaming | Server-side | Large files/real-time | Low | Continuous |
| Batching | Client-side | Multiple operations | Moderate | Reduced |

Remember:
- Not all APIs support all methods
- Always check API documentation
- Consider rate limits and performance
- Choose based on your specific use case

## Using .env Files for Authentication

### Why Use .env Files?

1. **Security**
   - Keeps sensitive credentials out of your code
   - Prevents accidental commits of secrets to version control
   - Allows different credentials for different environments (dev, staging, prod)

2. **Configuration Management**
   - Easy to switch between different API keys/tokens
   - No need to modify code when credentials change
   - Can have different .env files for different environments

3. **Best Practices**
   - Follows the 12-factor app methodology
   - Makes your code more portable
   - Easier to manage in team environments

### Example Setup

1. **Create .env file**:
```bash
# .env
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz
OPENWEATHER_API_KEY=sk_test_1234567890abcdefghijklmnopqrstuvwxyz
STRIPE_SECRET_KEY=sk_test_1234567890abcdefghijklmnopqrstuvwxyz
```

2. **Add .env to .gitignore**:
```bash
# .gitignore
.env
.env.*
!.env.example
```

3. **Create .env.example**:
```bash
# .env.example
GITHUB_TOKEN=your_github_token_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here
```

4. **Use in Python code**:
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
github_token = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"Bearer {github_token}"
}

# Make API request
response = requests.get(
    "https://api.github.com/user/repos",
    headers=headers
)
```

### Best Practices for .env Files

1. **Never commit .env to version control**
   - Add `.env` to your `.gitignore`
   - Only commit `.env.example`

2. **Use different .env files for different environments**
   ```bash
   .env.development
   .env.staging
   .env.production
   ```

3. **Document required environment variables**
   - Keep `.env.example` up to date
   - Document in README which variables are needed

4. **Validate environment variables**
   ```python
   def validate_env_vars():
       required_vars = ["GITHUB_TOKEN", "API_KEY"]
       missing_vars = [var for var in required_vars if not os.getenv(var)]
       if missing_vars:
           raise ValueError(f"Missing required environment variables: {missing_vars}")
   ```

5. **Use default values when appropriate**
   ```python
   # Use default value if environment variable not set
   api_key = os.getenv("API_KEY", "default_key_for_development")
   ```

### Common Mistakes to Avoid

1. **Hardcoding credentials**
   ```python
   # DON'T DO THIS
   token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
   
   # DO THIS INSTEAD
   token = os.getenv("GITHUB_TOKEN")
   ```

2. **Forgetting to load .env**
   ```python
   # DON'T FORGET THIS
   load_dotenv()
   ```

3. **Not handling missing variables**
   ```python
   # DON'T DO THIS
   token = os.getenv("GITHUB_TOKEN")  # Could be None
   
   # DO THIS INSTEAD
   token = os.getenv("GITHUB_TOKEN")
   if not token:
       raise ValueError("GITHUB_TOKEN environment variable not set")
   ```

## Project Structure

- `requirements.txt` - Project dependencies
- `src/` - Source code directory
  - `basic_requests.py` - Basic HTTP client usage examples
  - `advanced_requests.py` - Advanced scenarios and best practices
  - `real_world_examples.py` - Practical examples with real APIs
- `tests/` - Test cases for API interactions
- `.env.example` - Example environment variables file

## Getting Started

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your API keys
5. Start exploring the examples in the `src` directory

## Practice APIs

We'll use the following free APIs for practice:
- JSONPlaceholder (https://jsonplaceholder.typicode.com/)
- OpenWeatherMap (https://openweathermap.org/api)
- GitHub API (https://docs.github.com/en/rest)

## Contributing

Feel free to add more examples or improve existing ones. This is a learning resource, so contributions are welcome!