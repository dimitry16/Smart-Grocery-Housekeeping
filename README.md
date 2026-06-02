# Smart Grocery Housekeeping

A full-stack web application that helps users track their grocery inventory and reduce food waste. Manage your pantry, scan items via barcode or camera-based object recognition, get recipe suggestions based on expiring ingredients, and view usage analytics.

## Features

- **Inventory Management** — Add, update, and delete food items with details like brand, category, quantity, and expiration date
- **Barcode Scanning** — Scan product barcodes with your camera to auto-populate item details via the Open Food Facts API
- **Object Recognition** — Identify fruits and vegetables using Google Vision API through your device camera
- **Recipe Suggestions** — Get recipe ideas based on items expiring within 3 days (powered by Spoonacular API)
- **Saved Recipes** — Bookmark recipes for later reference
- **Usage Reports** — Track consumption patterns and food waste analytics
- **Expiration Alerts** — Color-coded badges indicating expired, expiring soon, or safe items
- **PWA Support** — Installable as a progressive web app to use as a native mobile app

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 19, Vite, React Router 7, Tailwind CSS, shadcn/ui |
| Backend | Python, FastAPI, SQLAlchemy (async), Alembic |
| Database | PostgreSQL (local or Google Cloud SQL) |
| Auth | JWT with Argon2 password hashing |
| External APIs | Open Food Facts, Google Vision, Spoonacular |
| Infrastructure | Docker, Nginx, Google Cloud Run, GitHub Actions |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── auth/                    # JWT authentication
│   │   ├── database/                # Models & DB connection
│   │   ├── external_api_services/   # Google Vision, recipes
│   │   ├── food_items/              # Inventory CRUD
│   │   ├── recipes/                 # Recipe logic
│   │   ├── reports/                 # Usage analytics
│   │   ├── users/                   # User management
│   │   ├── main.py                  # FastAPI app entry point
│   │   └── config.py               # Settings
│   ├── alembic/                     # Database migrations
│   ├── tests/                       # Test suite
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   ├── pages/                   # Page views
│   │   ├── lib/                     # Utilities & API client
│   │   └── App.jsx                  # Routing & layout
│   ├── nginx.conf
│   └── Dockerfile
│
└── .github/workflows/               # CI/CD pipelines
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys:
#   POSTGRES_SERVER, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
#   SECRET_KEY (generate with: openssl rand -hex 32)
#   TEST_DATABASE_URL (Create another database, locally, for testing API endpoints)
#   SPOONACULAR_API_KEY (optional, for recipe suggestions)

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. 

Access the Interactive API documentation at:
- ReDocs: `http://localhost:8000/redoc`
- Swagger UI: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm ci

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`.

### Docker Deployment

```bash
# Backend
cd backend
docker build -t grocery-backend .
docker run -p 8000:8000 --env-file .env grocery-backend

# Frontend
cd frontend
docker build -t grocery-frontend --build-arg VITE_API_BASE_URL=http://localhost:8000 .
docker run -p 80:80 grocery-frontend
```

## API Endpoints

| Prefix | Description |
|--------|-------------|
| `/v1/tokens` | Authentication (login, token refresh) |
| `/v1/users` | User registration and profile |
| `/v1/food-items` | CRUD operations for pantry items |
| `/v1/recipes` | Recipe suggestions and saved recipes |
| `/v1/vision` | Object recognition via Google Vision |
| `/v1/reports` | Usage analytics and reporting |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `POSTGRES_SERVER` | Yes | PostgreSQL host |
| `POSTGRES_DB` | Yes | Database name |
| `POSTGRES_USER` | Yes | Database user |
| `POSTGRES_PASSWORD` | Yes | Database password |
| `SECRET_KEY` | Yes | JWT signing key |
| `TEST_DATABASE_URL` | Yes | Test database connection URL used to isolate test data during API endpoint testing. |
| `SPOONACULAR_API_KEY` | No | Spoonacular API key for recipes |
| `GOOGLE_APPLICATION_CREDENTIALS` | No | Path to GCP service account JSON for Vision API |

## Running Tests

```bash
cd backend
pytest tests/
```

## License

This project is for educational purposes.
