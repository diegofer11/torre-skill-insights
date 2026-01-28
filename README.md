# Project overview

A FastAPI application that retrieves user genome from Torre API and analyzes it to identify skills and their demand in
the job market.

---

# Tech stak

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **HTTP client:** httpx
- **Data model:** pydantic
- **Testing:** pytest
- **Tooling:** uvicorn, PyCharm

---

## Installation

Clone the repository and install dependencies with Poetry:

```bash
git clone https://github.com/diegofer11/torre-skill-insights.git
cd torre-skill-insights

# Install dependencies using poetry
pip install poetry
poetry install

# Run the service
poetry run uvicorn app.main:app --reload
```

## Running the Service

The API will be available at http://127.0.0.1:8000

### Usage

Example request:

Get user skills:

```bash
GET /api/v1/users/{username}/torre/skills
```

Get user insights:

```bash
GET /api/v1/users/{username}/insights?currency=USD&periodicity=hourly&lang=en&contextFeature=job_feed&criteria=OR
```

### Testing

Run the test suite with:

```bash
poetry run pytest
```

# Architecture overview

The project is structured as follows:

```
torre-skill-insights/
├── app/
│   ├── main.py              # Application entrypoint
│   ├── api/                 # Routers (endpoints)
│   ├── services/            # Torre API clients
│   ├── models/              # Pydantic schemas
│   └── core/                # Config & utilities
├── tests/                   # Unit & integration tests
├── requirements.txt
└── README.md
```

- **API Layer:** FastAPI routers and services.
- **Service Layer:** Torre API clients.
- **Domain Layer:** Pydantic models and services.
- **Core Layer:** Configuration and utilities.

---

# Features

- Retrieve user genome.
- Analyze genome to identify skills and their demand in the job market.
- Provide insights in JSON format.
- Testable endpoints and services.

# Assumptions

- Focus on the top five skills.
- No persistence layer.
- Authentication isn’t required for public endpoints.

---

# Tradeoffs

- JSON output only, leaving room for future UI integrations.

---

# Next steps

- Add caching to improve performance and reduce Torre API calls.
