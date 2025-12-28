import React from 'react';
import '../css/AboutPage.css';

// --- 1. IMPORT YOUR IMAGES ---
// This assumes your images are in `src/assets/about/`.
// Vite will handle the pathing and optimization.
import heroImage from '../assets/about/hero-all-degrees.png';
import dockerArchImage from '../assets/about/architecture-docker-ps.png';
import scrapersImage from '../assets/about/scrapers.png';
import scraperEmbeddingLogs from '../assets/about/scraper-embedding-logs.png';
import vectorDbImage from '../assets/about/data-vector-db.png';
import ragPipelineImage from '../assets/about/rag-pipeline.png';


const AboutPage = () => {
    return (
        <div className="about-page-container main-content">
            <div className="about-section">
                {/* --- 2. USE THE IMPORTED IMAGE VARIABLES --- */}
                <div className="image-container hero-image">
                    <img src={heroImage} alt="All Degrees page showing a grid of generated degrees" />
                </div>
                <h1>Building a Guided Path Through Open Knowledge</h1>
                <p>
                    University accredited courses are available en masse on the internet. However high-quality the content is, the absence of a clear, sequential structure leaves complicated curriculum construction in the user's hands.
                </p>
                <p>
                    <strong>OSSU (Open Source Society University)</strong> approaches this issue creatively, with a community of educated individuals finding, vetoing and cultivating structured paths to mimic a traditional degree. However, with a quick-changing internet landscape and the constraints of human labor, this leads to massive overhauls when a resource is no longer available (see the complications of Coursera changing their audit policies).
                </p>
                <p>
                    This project was born from a simple question: Can we use modern AI to honor the rigor of a traditional university education while embracing the freedom of open-source learning (and have it all done automatically)? The goal was not to replace the university, but to build a bridge to it.
                </p>
            </div>

            <div className="about-section">
                <h2>The Blueprint</h2>
                <p>
                    To build a system that could handle tens of thousands of courses and complex AI tasks, I chose to build the entire application on a containerized, microservice-inspired foundation using Docker. This ensures the project is portable, reproducible, and ready for the cloud. The architecture is composed of several independent services that work in concert:
                </p>
                <ul className="architecture-list">
                    <li><strong>Django + Gunicorn:</strong> The API Server, serving a REST API to the frontend.</li>
                    <li><strong>PostgreSQL + pgvector:</strong> The Data, storing course information and enabling high-speed semantic search on AI-generated vector embeddings.</li>
                    <li><strong>Redis:</strong> The Message Broker, an in-memory data store that decouples the main application from long-running tasks.</li>
                    <li><strong>Celery:</strong> The Workhorse, running background workers for everything from web scraping to AI inference.</li>
                    <li><strong>Flask + Llama.cpp:</strong> The AI Core, a dedicated server that runs the `Phi-3-mini` language model, acting as the "expert academic advisor."</li>
                </ul>
                <div className="image-container">
                    <img src={dockerArchImage} alt="Terminal showing Docker services running" />
                </div>
            </div>

            <div className="about-section">
                <h2>The Data Pipeline</h2>
                <h3>Automated Scraping with Scrapy and Celery Beat</h3>
                <p>
                    The process begins with a suite of web scrapers built with Scrapy. These spiders are designed to crawl university course catalogs (currently MIT OCW). To make this a live system, I used Celery Beat, a scheduler that automatically triggers the scrapers on a weekly basis, ensuring the data is always fresh.
                </p>
                <div className="image-container">
                    <img src={scrapersImage} alt="Celery worker logs showing a scraper task in progress" />
                </div>

                <h3>AI-Powered Data Enrichment</h3>
                <p>
                    Once a course is saved, a `post_save` signal triggers a background task. This task uses `sentence-transformers` to convert the course's content into a 384-dimensional vector embedding—a mathematical representation of its meaning. This allows us to search for courses based on conceptual similarity, not just keywords.
                </p>
                <div className="image-container">
                    <img src={scraperEmbeddingLogs} alt="Logs showing embedding generation tasks" />
                    <hr style={{ borderColor: 'var(--border-color)', margin: '1rem 0' }} />
                    <img src={vectorDbImage} alt="pgAdmin view showing vector embeddings in the database" />
                </div>
                <p>A view of course embeddings in pgAdmin.</p>
            </div>

            <div className="about-section">
                <h2>The AI Core: The RAG Pipeline</h2>
                <p>
                    This is the heart of the project: a <strong>Retrieval-Augmented Generation (RAG)</strong> pipeline that constructs degrees from the database.
                </p>
                <ol className="rag-steps">
                    <li className="rag-step-item"><strong>Retrieval:</strong> For each syllabus requirement, the system performs a vector search against the database to find the top 5 most similar online courses.</li>
                    <li className="rag-step-item"><strong>Augmentation & Generation:</strong> These candidates, along with the curriculum context, are formatted into a detailed prompt and sent to the local `Phi-3-mini` language model, which reasons about the options and selects the single best fit.</li>
                </ol>
                <div className="image-container">
                    <img src={ragPipelineImage} alt="Composite image showing the RAG pipeline in action" />
                </div>
            </div>

            <div className="about-section">
                <h2>Challenges & Lessons Learned</h2>
                <h3>Translation of Mental Models</h3>
                <p>
                    With a system that has so many moving parts, trying to understand how to formulate Django models to both contain all of the information required while not having too many blank fields was a major pain point. To avoid migration issues, the models include optional fields that will eventually be filled as the project becomes more robust.
                </p>
                <h3>Inconsistent Data</h3>
                <p>
                    One of the first major hurdles was data inconsistency from the scrapers.
                    While data normalization and cleaning are parts of any scraping pipeline, the dynamic between the construction of the models and the information available made me trim down the information on each object. I refactored my Scrapy items to use `output_processors` to enforce a clean schema at the source, and cut down on unnecessary fields to ensure uniform presentation.
                </p>
                <h3>Containerized Development</h3>
                <p>
                    Moving to a multi-container Docker environment was a learning curve. Understanding how the development process changes when you're no longer dealing with a singular running server led to many hiccups in docker builds. Eventually, the process will smooth out when you re-formulate your approach to understand containerized development and begin debugging, testing, and troubleshooting soley within the Docker Compose environment.
                </p>
            </div>
        </div >
    );
};

export default AboutPage;