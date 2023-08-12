# ToDo Backend

This project provides a RESTful API for managing ToDos. It offers endpoints to create, update, delete, and retrieve ToDos. It's built using Flask and integrates with a SQL database. 

## Features

- RESTful API endpoints for CRUD operations on ToDos.
- Filter ToDos based on completion and deletion status.
- Integrated database for persistent storage.
- Unit tests to validate the service behavior.

## Setup using Docker Compose

To simplify the setup, we've provided a `docker-compose.yml` file. Before starting, ensure you have Docker and Docker Compose installed on your machine.

### Steps:

1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_name>
```

2. Build the Docker image and start the services using Docker Compose:

```bash
docker-compose up --build
```
After executing the above command, the ToDo API should be running on http://127.0.0.1:5001.

3. To stop the service:
```bash
docker-compose down
```
## Testing with Docker Compose
We've integrated unit tests to ensure that our API behaves as expected. To run these tests using Docker Compose:
```bash
docker-compose -f docker-compose.test.yml up --build
```

## Troubleshooting
1. Port Conflicts: Ensure that no other services are running on port 5001. If required, you can change the port in the docker-compose.yml file.

2. Checking Logs: To monitor the behavior or debug any issues, check the logs of a specific service:

```bash
docker-compose logs web
```
Configuration Issues: If you face any issues related to the configuration, ensure all required files are correctly set up and the environment variables are correctly set in the docker-compose.yml file.

