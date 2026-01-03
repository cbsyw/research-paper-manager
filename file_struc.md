research-paper-manager/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Makes 'app' a package
│   │   ├── main.py               # FastAPI app, startup logic, include routers
│   │   ├── database.py           # SQLAlchemy engine, session, Base
│   │   ├── models.py             # Paper SQLAlchemy model
│   │   ├── schemas.py            # Pydantic models for validation
│   │   ├── crud.py               # Database functions (get, create, update, delete)
│   │   │
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── papers.py         # /papers endpoints
│   │   │   └── search.py         # /search, /add-from-openalex endpoints
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       └── openalex.py       # OpenAlex API calls
│   │
│   ├── requirements.txt          # Python dependencies
│   └── seed_data.py              # Script to populate initial data
│
├── frontend/
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── PaperList.jsx     # Displays list of papers
│   │   │   ├── PaperCard.jsx     # Single paper display
│   │   │   ├── SearchBar.jsx     # OpenAlex search interface
│   │   │   └── PaperDetail.jsx   # Detailed view/edit form
│   │   │
│   │   ├── services/
│   │   │   └── api.js            # HTTP calls to backend
│   │   │
│   │   ├── App.jsx               # Main component
│   │   └── main.jsx              # React entry point
│   │
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Build configuration
│
├── .gitignore                    # Ignore node_modules, venv, *.db
├── README.md                     # Project documentation
└── papers.db                     # SQLite database (auto-generated, gitignored)
