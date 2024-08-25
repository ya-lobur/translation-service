# Word Translation Microservice

This microservice provides a JSON API to fetch and store word definitions, synonyms, translations,
and examples using Google Translate. The service stores the fetched data in a NoSQL database (MongoDB)
to minimize external API calls and improve response times.

## Before you start

Note that Google Translate public api is not intended to be used for commercial purposes and Google may start banning
your requests coming from this application (then you see `Some Google API issue occurred` error).

## Features

- Fetch word details including definitions, synonyms, translations, and examples from Google Translate.
- Support for translations in multiple languages.
- Store and retrieve word details from MongoDB.
- Pagination, sorting, and filtering of stored words.
- Delete words from the database.

## Tech Stack

- Language: Python 3.11
- Framework: FastAPI (async)
- Database: MongoDB (NoSQL)
- Containerization: Docker

## Setup Instructions

### 1. Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.11+ and poetry installed if running locally.

### 2. Clone the Repository

```shell
git clone https://github.com/ya-lobur/translation-service.git
```

### 3. .env

**Make sure you have`.env` file with `MONGO_DSN` at least.** (see `[.env.template](.env.template)`)

### 4. Running with Docker

Build and run the application using Docker Compose:

```shell
docker-compose up --build
```

This will start both the FastAPI service and MongoDB in Docker containers.
The service will be accessible at http://localhost:8000.

### 5. Running Locally

If you prefer to run the service locally without Docker:

1. Install requirements with `poetry`:

```shell
poetry install
```

2. Start the MongoDB server: Ensure MongoDB is running on `localhost:27017`.
3. Run the application (from root dir):

```shell
python manage.py
```

## Endpoints

Documentation: http://0.0.0.0:8000/swagger#/

## Future Improvements

- Authentication: Add user authentication and authorization.
- Extended Language Support: Expand the service to handle more complex language scenarios.
- Error Handling: Improve error handling for different edge cases.

