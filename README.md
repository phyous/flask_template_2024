# Flask Template Repository

A minimal Flask application template with Poetry dependency management and pytest setup.

## Setup

1. Install Poetry (dependency management):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Initialize the project:
   ```bash
   poetry install
   ```

## Running the Server

Start the Flask development server:
```bash
poetry run python src/app.py
```

The server will start on `http://localhost:8000`. You can verify it's running by accessing the healthcheck endpoint:
```bash
curl http://localhost:8000/healthcheck
```

## Running Tests

Execute the test suite using pytest:
```bash
poetry run pytest
```

For verbose output and to see print statements:
```bash
poetry run pytest -v -s
```