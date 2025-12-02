# AI-Powered Curriculum Generator
A web application that programmatically generates university-level degree roadmaps by matching real-world syllabi against a database of online courses.
### Project Motivation
Structured, sequential, and trusted learning paths are crucial for effective self-education. While resources like MIT OpenCourseWare, edX, and similar open platforms provide high-quality content, learners are often left to build their own curriculums which then leave these resources generally unused in favor of more user-friendly content. Manually curated lists like OSSU (Open Source Society University) are excellent but static and labor-intensive to maintain.
The eventual goal of this project is to automate the creation of these roadmaps. By leveraging vector search and a local LLM, this application aims to dynamically generate a complete, semester-by-semester degree plan that mirrors the structure of an accredited university program, using a constantly updated catalog of online courses.

## Core Features
**`Automated Data Ingestion`**: A Scrapy-based web scraper autonomously crawls course catalogs (e.g., MIT OCW currently) to build and maintain a local PostgreSQL database of available online courses.
**`Syllabus Ingestion`**: A real-world university syllabus (e.g., a Bachelor's in Computer Science) is entered into the system via the Django Admin, defining the required courses for each semester.
**`Vector Search (Retrieval)`**: For each syllabus requirement, the system generates a vector embedding and uses pgvector to perform a semantic search, retrieving the most similar online courses from the database.
**`LLM Reasoning (Generation)`**: The top candidate courses are passed to a locally-run Large Language Model (Phi-3-mini). The LLM analyzes the candidates and selects the single best fit for the syllabus requirement.
Asynchronous & Scalable Architecture: The system is built on a asynchronous foundation using Celery and Redis. This allows for long-running tasks like scraping thousands of pages or backfilling embeddings for the entire database to occur in the background.
### Architecture & Tech Stack
This project is containerized with Docker to ensure a consistent and reproducible environment.
**`Backend`**: Django, Django REST Framework (DRF)
**`Database`**: PostgreSQL with the pgvector extension for vector similarity search.
**`Embeddings`**: sentence-transformers (all-MiniLM-L6-v2) for generating vector representations of course content.
**`LLM Engine`**: A local instance of Phi-3-mini-4k-instruct (GGUF) served via a minimal Flask API.
**`LLM Runtime`**: llama-cpp-python for efficient, CPU-based model inference.
**`Asynchronous Processing`**: Celery (for task management), Redis (as a message broker).
**`Containerization`**: Docker, Docker Compose

## Local Development Setup
**Prerequisites**
- Git
- Docker & Docker Compose
### Running the Application
Clone the repository:
```Bash
git clone https://github.com/V-enis/CourseCrawler.git
cd cc-backend
```
**Configure Environment:**
Create an .env file in the project root. Use the following template, filling in your own secret key and password.
```
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=webdegree
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

HF_INFERENCE_ENDPOINT_URL=http://host.docker.internal:5001/generate
HF_INFERENCE_ENDPOINT_TOKEN=local_token
```

**Build and Start Services:**
This command will build the Docker images and start all required services (Django, Postgres, Redis, Celery Worker).
```Bash
docker-compose up --build -d
```
**Run Database Migrations:**
Apply the initial database schema.
```Bash
docker-compose exec app python manage.py migrate
```
**Run the Local LLM Server:**
In a separate terminal, with your local Python virtual environment activated, start the model API server. (Ensure you have downloaded the model file into a models/ directory first).
```Bash
python llm_api.py
```
**Access the Application:**
The Django application, including the admin panel, is now available at http://localhost:8000.
**Populating the Database**
To populate the database with courses, run the scraper via the custom Django management command:
```Bash
docker-compose exec app python manage.py run_mit_scraper
```