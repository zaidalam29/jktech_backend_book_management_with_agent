# Document Intelligence & QnA Backend

JKTech Internal Backend System  
Author: **Zaid Alam**  
Role: *Full Stack Developer & Generative AI Engineer*

---

## Overview

This backend service is designed to manage **books, documents, users, and reviews** while providing **AI-powered search and summarization** capabilities.

The system follows a **Retrieval-Augmented Generation (RAG)** approach to deliver context-aware responses from stored content.  
All documents and assets are stored on the **local server** and indexed for semantic search.

---

## Core Modules

### Book Management
- Create, update, view, and delete books
- Generate automated AI summaries
- Recommend related books based on content similarity

### Review Management
- Submit reviews with ratings
- Retrieve book-specific reviews
- Generate summarized feedback using AI

### Intelligent Search (RAG)
- Natural language query support
- Semantic search powered by vector embeddings
- Automatic reindexing on data updates

### User Access Control
- JWT-based authentication
- Role-based authorization
- Administrative user and role management

### Document Handling
- Upload documents for processing
- Download stored files
- Remove documents when required
- Local file system storage

---

## API Routes

### Authentication

**POST /auth/signup**  
Registers a new user in the system.

**POST /auth/login**  
Authenticates a user and issues a JWT token.

**POST /auth/logout**  
Terminates the current user session.

**POST /auth/create-admin**  
Creates an administrator account.

---

### Books

**POST /books**  
Creates a new book entry.

**GET /books**  
Returns all available books.

**GET /books/{id}**  
Fetches details of a specific book.

**PUT /books/{id}**  
Updates an existing book record.

**DELETE /books/{id}**  
Deletes a book from the system.

**POST /books/{id}/generate-summary**  
Generates an AI-based summary for the selected book.

**POST /books/{id}/reindex**  
Rebuilds the search index for the book.

---

### Reviews

**POST /books/{id}/reviews**  
Adds a review and rating for a book.

**GET /books/{id}/reviews**  
Retrieves all reviews linked to the book.

**GET /books/{id}/summary**  
Generates a summarized overview of reviews using AI.

---

### Search & Indexing

**GET /search**  
Executes a semantic search using query parameters.

**POST /search**  
Executes a semantic search using request body input.

**POST /reindex-all**  
Reindexes all books and documents.

**GET /debug/embeddings**  
Provides embedding data for debugging purposes.

---

### Administration (Restricted)

**POST /admin/users**  
Creates a new user.

**GET /admin/users**  
Lists all users.

**PUT /admin/users/{id}**  
Updates user information.

**DELETE /admin/users/{id}**  
Deletes a user.

**GET /admin/users/roles**  
Returns available roles.

**POST /admin/users/roles**  
Creates a new role.

---

### Documents

**POST /documents/upload**  
Uploads a document for storage and indexing.

**GET /documents**  
Lists all uploaded documents.

**GET /documents/{id}/download**  
Downloads a document by ID.

**DELETE /documents/{id}**  
Deletes a document from the system.

---

## Project Setup Guide

### System Requirements

- Python 3.10 or higher
- PostgreSQL database
- OpenRouter API key

---

### Installation

```bash
git clone <repository-url>
cd jktech_backend_book_management_with_agent
pip install -r requirements.txt

```

### Environment (.env)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jktech_document_agent
DB_USER=postgres
DB_PASSWORD=your_password

LLM_KEY=your_api_key
```

### Run Server

```bash
uvicorn app.main:app --reload
```

---

## Testing

```bash
pytest tests/ -v
```

---

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Sentence Transformers (RAG)
- Pytest

---

**Zaid Alam – Full Stack Developer & Gen AI Engineer**
