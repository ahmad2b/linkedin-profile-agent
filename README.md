# LinkedIn Profile Agent

This project provides a powerful foundation for building a customGPT that let you interact with users' or companies LinkedIn profiles. Built with FastAPI and Upstash Redis, the application offers a comprehensive suite of features to streamline your LinkedIn interactions.

## Custom GPT Integration

Thanks to FastAPI's built-in support for OpenAPI, this application can generate an OpenAPI schema that can be used to integrate with custom GPTs. This allows you to create a LinkedIn profile agent GPT that users can interact with to fetch LinkedIn profile and company information and interact with it.

### Example Use Case

You can create a custom GPT model that uses the OpenAPI schema of this application to add actions for searching LinkedIn profiles and companies. This can be used to build a GPT that helps users find LinkedIn profiles and companies, providing a conversational interface for LinkedIn data.

Try the custom GPT here: [LinkedIn Profile Agent](https://chatgpt.com/g/g-eEeZCLQ2M-in-profile-agent)

> **Note**: If the custom GPT does not work, it may be due to the ProxyCurl API limit being reached. In that case, you can clone this repository and deploy the application to your own server with your own ProxyCurl API key and create a custom GPT model that integrates with your server.

## Requirements

- Python 3.9+
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

## License

This project is licensed under the MIT License.
