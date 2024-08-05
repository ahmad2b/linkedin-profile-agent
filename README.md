# LinkedIn Profile Agent

LinkedIn Profile Agent is a FastAPI-based application that allows users to search for LinkedIn profiles and companies using the ProxyCurl API. The application also integrates with Upstash Redis for caching.

## Features

- Search LinkedIn profiles by URL
- Search LinkedIn companies by URL
- Health check endpoint
- Docker support for development
- OpenAPI schema generation for integration with custom GPTs

## Requirements

- Python 3.8+
- Docker (for development)
- ProxyCurl API Key
- Upstash Redis URL and Token

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/ahmad2b/linkedin-profile-agent.git
   cd linkedin-profile-agent
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   poetry install
   ```

4. Create a `.env` file based on `env.example` and fill in your environment variables:

   ```sh
   cp env.example .env
   ```

5. Run the application:

   ```sh
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Docker Development

1. Build the Docker image:

   ```sh
   docker build -t linkedin-profile-agent -f Dockerfile.dev .
   ```

2. Run the Docker container:

   ```sh
   docker run --env-file .env -p 8000:8000 linkedin-profile-agent
   ```

## Endpoints

### Health Check

- **GET** `/health`
  - **Description**: Check the health of the application.
  - **Response**: `200 OK` if the application is healthy.

### Search Profile

- **POST** `/search/profile`
  - **Description**: Search for a LinkedIn profile by URL.
  - **Request Body**:
  ```json
  {
  	"profile_url": "https://www.linkedin.com/in/example"
  }
  ```
  - **Response**: JSON object containing profile information.

### Search Company

- **POST** `/search/company`
  - **Description**: Search for a LinkedIn company by URL.
  - **Request Body**:
  ```json
  {
  	"company_url": "https://www.linkedin.com/company/example"
  }
  ```
  - **Response**: JSON object containing company information.

## Environment Variables

- `PROXYCURL_API_KEY`: Your ProxyCurl API key.
- `UPSTASH_REDIS_REST_URL`: Upstash Redis REST URL.
- `UPSTASH_REDIS_REST_TOKEN`: Upstash Redis REST token.
- `PORT`: Port to run the application (default: 8000).

## Use Cases

### OpenAPI Schema and Custom GPT Integration

Thanks to FastAPI's built-in support for OpenAPI, this application can generate an OpenAPI schema that can be used to integrate with custom GPTs. This allows you to create a Linkedin profile agent chatbot that users can interact with to fetch LinkedIn profile and company information.

### Example Use Case

You can create a custom GPT model that uses the OpenAPI schema of this application to add actions for searching LinkedIn profiles and companies. This can be used to build a chatbot that helps users find LinkedIn profiles and companies, providing a conversational interface for LinkedIn data.

Try the custom GPT here: [LinkedIn Profile Agent](https://chatgpt.com/g/g-eEeZCLQ2M-in-profile-agent)

> **Note**: If the custom GPT does not work, it may be due to the ProxyCurl API limit being reached. In that case, you can clone this repository and deploy the application to your own server with your own ProxyCurl API key and create a custom GPT model that integrates with your server.

## License

This project is licensed under the MIT License.
