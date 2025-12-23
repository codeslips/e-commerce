# Change: Add Minimal Scaffold to Make Project Runnable

## Why

The project has Docker configuration and documentation but lacks the actual source code files needed to build and run the containers. Users cannot currently start the application with `docker-compose up`.

## What Changes

- Add minimal `backend/main.py` with FastAPI app that returns stub responses
- Add `backend/requirements.txt` with required Python dependencies
- Add `backend/models.py` with Pydantic model definitions
- Add `frontend/index.html` with basic HTML structure
- Add `frontend/js/app.js` with empty/stub JavaScript
- Add `frontend/css/style.css` with minimal styles
- Add `data/orders.json` with empty array for order data
- Add `data/products.json` with empty array for product data
- Fix healthcheck endpoint in docker-compose.yml (port mismatch)

## Impact

- Affected specs: project-bootstrap (new capability)
- Affected code: `backend/`, `frontend/`, `data/`

