# Book Management System

**JkTech Backend** – Book Management System with AI Search (RAG)  
Developed by **Zaid Alam – Full Stack Developer & Gen AI Engineer**

---

## 📌 Project Overview

This is a backend application used to manage **books, users, reviews, and documents**.  
It also supports **AI-based search and summary generation** using a RAG (Retrieval-Augmented Generation) approach.

📂 **File Storage:** Local Server Storage

---

## ✨ Main Features

### 📚 Books
- Add, update, delete, and view books
- Generate AI summaries for books
- Get book recommendations

### ✍️ Reviews
- Users can add reviews with ratings
- View all reviews of a book
- Generate review summary

### 🔍 AI Search (RAG)
- Search books using natural language
- Semantic search using embeddings
- Automatic reindexing when data changes

### 👥 Users & Roles
- JWT-based login and signup
- Admin and User roles
- Admin can manage users and roles

### 📄 Documents
- Upload documents
- Download documents
- Delete documents
- All files stored locally

---

## 🔗 API Routes

### 🔐 Authentication Routes
| Method | Route | Description |
|------|------|-------------|
| POST | /auth/signup | User registration |
| POST | /auth/login | User login |
| POST | /auth/logout | User logout |
| POST | /auth/create-admin | Create admin user |

---

### 📚 Book Routes
| Method | Route | Description |
|------|------|-------------|
| POST | /books | Create a new book |
| GET | /books | Get all books |
| GET | /books/{id} | Get book by ID |
| PUT | /books/{id} | Update book |
| DELETE | /books/{id} | Delete book |
| POST | /books/{id}/generate-summary | Generate AI summary |
| POST | /books/{id}/reindex | Reindex book |

---

### ✍️ Review Routes
| Method | Route | Description |
|------|------|-------------|
| POST | /books/{id}/reviews | Add review |
| GET | /books/{id}/reviews | Get reviews |
| GET | /books/{id}/summary | Review summary |

---

### 🔍 Search Routes
| Method | Route | Description |
|------|------|-------------|
| GET / POST | /search | Semantic search |
| POST | /reindex-all | Reindex all books |
| GET | /debug/embeddings | Debug embeddings |

---

### 👮 Admin Routes (Admin Only)
| Method | Route | Description |
|------|------|-------------|
| POST | /admin/users | Create user |
| GET | /admin/users | List users |
| PUT | /admin/users/{id} | Update user |
| DELETE | /admin/users/{id} | Delete user |
| GET | /admin/users/roles | List roles |
| POST | /admin/users/roles | Create role |

---

### 📄 Document Routes
| Method | Route | Description |
|------|------|-------------|
| POST | /documents/upload | Upload document |
| GET | /documents | List documents |
| GET | /documents/{id}/download | Download document |
| DELETE | /documents/{id} | Delete document |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- OpenRouter API Key

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
DB_NAME=book_management
DB_USER=postgres
DB_PASSWORD=your_password

OPENROUTER_API_KEY=your_api_key
```

### Run Server

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📘 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🏗️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Sentence Transformers (RAG)
- Pytest

---

## 📄 License

MIT License © 2026  
**Zaid Alam – Full Stack Developer & Gen AI Engineer**
