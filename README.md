# AI-Powered Curriculum Generator

A full-stack web application that programmatically generates university-level degree roadmaps using a Retrieval-Augmented Generation (RAG) pipeline.

This repository is a monorepo containing:
- **`/cc-backend`**: A Django REST Framework API that manages data ingestion, a `pgvector` database, and the core AI logic.
- **`/cc-frontend`**: A React single-page application that provides the user interface for browsing generated degrees.

For a detailed narrative of the project's motivation, architecture, and challenges, please see the **"About"** page of the live application.

---

## Core Technologies

| Category                | Technology                                         |
| ----------------------- | -------------------------------------------------- |
| **Backend**             | Django, Django REST Framework, Gunicorn            |
| **Frontend**            | React, Vite, TanStack Query, Axios                 |
| **Database**            | PostgreSQL with `pgvector`                           |
| **AI (Embeddings)**     | `sentence-transformers`                            |
| **AI (Reasoning)**      | `Phi-3-mini-4k-instruct` (GGUF) via `llama-cpp-python` |
| **Async Tasks**         | Celery, Redis                                      |
| **Infrastructure**      | Docker, Docker Compose                             |

---

## Local Development Setup

This project is fully containerized with Docker, providing a consistent and reproducible environment for both frontend and backend development.

### Prerequisites
- Git
- Docker & Docker Compose
- A local Python environment (for running the LLM server)

### 1. Clone & Configure

```bash
git clone https://github.com/V-enis/CourseCrawler.git
cd CourseCrawler
```
Create a .env file in the project root (/CourseCrawler). Use the following template, filling in your own secret key and password.
```python
# .env - For Local Docker Development

# Django
SECRET_KEY=your-super-secret-key-for-local-dev
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (used by Docker)
POSTGRES_DB=webdegree
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Local LLM API
HF_INFERENCE_ENDPOINT_URL=http://host.docker.internal:5001/generate
HF_INFERENCE_ENDPOINT_TOKEN=local_token
```
### 2. Download the LLM Model
The local LLM server requires a model file. Use the huggingface-cli to download the recommended version into the cc-backend/models/ directory.
```bash
# First, ensure you have the CLI tool installed in your local Python env
pip install huggingface-hub

# Download the model file into the backend directory
huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-q4.gguf --local-dir ./cc-backend/models --local-dir-use-symlinks False
```
### 3. Run the Full Stack
This project requires two separate processes to be run.
- **First, in one terminal, start all the containerized services:**
```bash
# From the project root (/CourseCrawler)
docker-compose up --build -d
```
This will start the Django API, PostgreSQL DB, Redis, Celery workers, and the React Vite dev server.
- **Second, in a separate terminal, start the local LLM API server:**
```bash
# Navigate to the backend directory
cd cc-backend

# Activate your local Python virtual environment
# e.g., .\.venv\Scripts\activate

# Start the server
python llm_api.py
```
### 4. Initialize the Database
The first time you run the application, you need to set up the database schema and populate it with data.
```bash
# Apply migrations
docker-compose exec app python manage.py migrate

# Create a superuser to access the Django Admin
docker-compose exec app python manage.py createsuperuser

# Run the scraper to populate the course database
docker-compose exec app sh -c "cd cc_scrapers && scrapy crawl mit"
```
### 5. Access the Application
- Frontend Application: `http://localhost:3000`
- Backend API / Django Admin: `http://localhost:8000/admin`
## Useful Commands
All `docker-compose` commands should be run from the project root (/CourseCrawler).
- **Generate a Degree**:
After entering a syllabus in the admin, run this command with the syllabus ID.
```bash
docker-compose exec app python manage.py generate_degree <degree_id>
```
- **Backfill Embeddings**:
If courses are missing embeddings, run this to queue generation tasks.
```bash
docker-compose exec app python manage.py backfill_embeddings
```
- **Connect to Database CLI**:
```bash
docker-compose exec db psql -U postgres -d webdegree
```