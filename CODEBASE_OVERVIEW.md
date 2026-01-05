# Research Paper Manager - Codebase Overview

## Project Purpose
A full-stack web application for managing academic research papers with OpenAlex API integration for discovering and adding scholarly works to a personal library.

## Tech Stack

### Backend
- **FastAPI** (v0.128.0) - Modern Python web framework
- **SQLAlchemy** (v2.0.45) - ORM for database operations
- **Pydantic** (v2.12.5) - Data validation and schemas
- **httpx** (v0.28.1) - Async HTTP client for OpenAlex API
- **Uvicorn** (v0.40.0) - ASGI server
- **SQLite** - Database (papers.db)
- **python-dotenv** - Environment variable management

### Frontend
- **React** (v18.3.1) - UI library
- **Vite** (v6.0.7) - Build tool and dev server (runs on port 3000)
- **Vanilla CSS** - Styling (no framework)
- **Native Fetch API** - HTTP requests

---

## Project Structure

```
research-paper-manager/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── database.py        # SQLAlchemy database configuration
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic validation schemas
│   │   ├── crud.py            # Database CRUD operations
│   │   ├── routers/
│   │   │   ├── papers.py      # Paper CRUD endpoints
│   │   │   └── search.py      # OpenAlex integration endpoints
│   │   └── services/
│   │       └── openalex.py    # OpenAlex API service
│   ├── requirements.txt
│   └── seed_data.py           # Database seeding script
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── PaperList.jsx  # Paper list container
│   │   │   └── PaperCard.jsx  # Individual paper card
│   │   ├── services/
│   │   │   └── api.js         # Backend API client
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js         # Vite build configuration
│
├── .gitignore
├── README.md
├── file_struc.md              # Project structure documentation
├── phase3.md                  # OpenAlex integration docs
└── phase4.md                  # Frontend development docs
```

---

## Backend Architecture

### API Endpoints

#### Papers Router (`backend/app/routers/papers.py`)
- `GET /papers/` - List all papers (with pagination)
- `GET /papers/{paper_id}` - Get single paper
- `POST /papers/` - Create new paper
- `PUT /papers/{paper_id}` - Update paper
- `DELETE /papers/{paper_id}` - Delete paper

#### Search Router (`backend/app/routers/search.py`)
- `POST /search` - Search OpenAlex database
  - Request: `{ query: str, limit: int }`
  - Returns: List of papers with metadata
- `POST /papers/from-openalex` - Add paper from OpenAlex to library
  - Request: `{ openalex_id: str, notes: str }`
  - Returns: Created paper object

#### Root Endpoint
- `GET /` - API health check

### Key Backend Components

**`main.py`**
- FastAPI application initialization
- CORS middleware configured for localhost:3000
- Database table creation on startup
- Router registration

**`database.py`**
- SQLAlchemy engine setup with SQLite
- Session management with SessionLocal
- Dependency injection function (get_db)

**`models.py`**
- Paper model with fields: id, title, authors, year, abstract, url, notes

**`schemas.py`**
- PaperBase, PaperCreate, PaperUpdate, Paper schemas
- Pydantic validation for API requests/responses

**`crud.py`**
- get_papers() - Retrieve all papers with pagination
- get_paper() - Get single paper by ID
- create_paper() - Add new paper
- update_paper() - Update existing paper
- delete_paper() - Remove paper

**`services/openalex.py`**
- search_papers() - Search OpenAlex API
- get_paper_by_id() - Fetch specific paper details
- Transforms OpenAlex format to app schema
- 10-second timeout on requests
- Handles up to 5 authors per paper

---

## Frontend Architecture

### Component Hierarchy
```
App
└── PaperList
    └── PaperCard (multiple instances)
```

### Key Frontend Components

**`App.jsx`**
- Main application wrapper
- Header with title
- Renders PaperList component

**`components/PaperList.jsx`**
- Fetches papers from backend on mount
- Loading, error, and empty state handling
- Renders grid of PaperCard components
- Displays paper count

**`components/PaperCard.jsx`**
- Displays individual paper information
- Shows title, authors, year, abstract (truncated to 300 chars)
- External link to paper
- Notes display

**`services/api.js`**
- Centralized API client with base URL (http://localhost:8000)
- CRUD methods for papers
- OpenAlex search and add functionality
- Error handling wrapper

### State Management
- React hooks (useState, useEffect)
- Local component state
- No global state management (yet)

### Styling Approach
- Modular CSS files per component
- Clean, minimal design
- Responsive layout with flexbox/grid
- Color scheme: Dark blue header (#2c3e50), light gray background (#f5f5f5)

---

## Database Schema

### Database: SQLite (papers.db)

#### Papers Table
```
Table: papers
- id: Integer (Primary Key, Indexed)
- title: String (Indexed)
- authors: String
- year: Integer
- abstract: Text
- url: String
- notes: Text
```

### Pydantic Schemas
- **PaperBase**: All fields optional except title
- **PaperCreate**: Inherits from PaperBase (for POST requests)
- **PaperUpdate**: All fields optional (for PUT requests)
- **Paper**: Includes id field (for responses)

---

## Current Development Status

### Completed Features ✅
- Backend API with CRUD operations
- OpenAlex API integration
- Frontend basic display
- Paper library management
- Search OpenAlex database
- Add papers to personal library
- Card-based UI for browsing papers

### Seeding Script
`seed_data.py` fetches 15 biology papers from OpenAlex sorted by citation count and populates the database if empty.

---

## Technical Considerations

### Migration to PostgreSQL
Currently uses SQLite, but migration to PostgreSQL would be straightforward:
- Add `psycopg2-binary` dependency
- Update connection string in `database.py`
- Remove SQLite-specific `connect_args`
- No changes needed to models or CRUD operations (SQLAlchemy handles differences)

### Benefits of PostgreSQL Migration
- Better for production deployment
- Handles concurrent writes better
- More scalability
- Better full-text search capabilities
- Industry standard for web apps

---

## Planned Features & Enhancements

### 1. Search Functionality
- Add search bar component in frontend
- Search by title, authors, keywords
- Filter by year, tags, or custom criteria
- Real-time search results

### 2. Home/Explanation Page
- Landing page explaining the app's purpose
- How-to guide for using the platform
- Feature overview
- Getting started tutorial

### 3. User Authentication
- Email-based sign in
- Verification code system (no password)
- User sessions and JWT tokens
- Protected routes and user-specific libraries

### 4. Paper Swipe Feature (Discovery Mode)
**Concept**: Tinder-style interface for discovering research papers

**Components**:
- Interest selection on first use (topics, keywords, research areas)
- Card-based UI with swipe gestures
  - Swipe right / Like button → Save to "Interested" list
  - Swipe left / Dislike button → Pass on paper
- Recommendation algorithm
  - Analyzes liked/disliked papers
  - Uses paper metadata (title, abstract, authors, keywords)
  - Suggests similar papers from OpenAlex
  - Machine learning integration (optional: collaborative filtering, content-based filtering)
- Session tracking
  - Save swipe history
  - Learn user preferences over time
  - Improve recommendations based on behavior

**Technical Requirements**:
- Database table for user preferences and swipe history
- Recommendation engine/algorithm
- Touch/gesture support for mobile
- Animation library for card swiping (react-spring, framer-motion)

### 5. Card Management
- Add custom paper cards manually
- Remove papers from library
- Drag-and-drop reordering
- Bulk actions (delete multiple, export)
- Import papers from BibTeX, RIS, or CSV

### 6. Enhanced Note-Taking
- Rich text editor for notes (Markdown support)
- Highlight and annotate papers
- Tags and categories
- Search within notes
- Link notes between related papers
- Export notes as PDF or Markdown
- Collaborative notes (if multi-user)

### 7. Additional Features to Consider
- Paper collections/folders
- Citation management and export
- Reading progress tracker
- Bookmarks and highlights
- PDF viewer integration
- Export library to reference managers (Zotero, Mendeley)
- Dark mode
- Mobile-responsive design improvements
- Email notifications for new papers in areas of interest
- Social features (share papers, follow researchers)

---

## Development Workflow

### Running Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### Database Seeding
```bash
cd backend
python seed_data.py
```

---

## Architecture Patterns Used

- **RESTful API** design
- **Separation of concerns** (models, schemas, CRUD, services)
- **Dependency injection** for database sessions
- **Service layer** for external API integration
- **CRUD pattern** for database operations
- **Component-based UI** architecture
- **Async/await** patterns throughout
- **Type safety** with Pydantic schemas

---

## Future Technical Improvements

1. **State Management**: Add Redux or Context API for global state
2. **Testing**: Unit tests (pytest), integration tests, E2E tests (Playwright/Cypress)
3. **Docker**: Containerize backend and frontend for easy deployment
4. **CI/CD**: GitHub Actions for automated testing and deployment
5. **API Documentation**: Enhanced Swagger/OpenAPI docs
6. **Caching**: Redis for API response caching
7. **Rate Limiting**: Protect API endpoints from abuse
8. **Logging**: Structured logging with log aggregation
9. **Monitoring**: Application performance monitoring (APM)
10. **Database Migrations**: Alembic for schema versioning
11. **TypeScript**: Convert frontend to TypeScript for type safety
12. **Mobile App**: React Native version
13. **Offline Support**: Service workers and PWA capabilities

---

## Contact & Documentation

- **Repository**: [GitHub Link]
- **API Docs**: http://localhost:8000/docs (when running)
- **Project Phases**: See `phase3.md` and `phase4.md` for development history

---

*Last Updated: 2027-01-05*
