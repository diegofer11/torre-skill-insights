# Project overview

The **Skills Insights Dashboard** is a FastAPI-based application that integrates with the Torre APIs to provide
actionable insights about professional skills and their demand in the job market.

The system retrieves a user's genome and analyzes it to identify the most relevant skills and their demand in the job
market, generating a dashboard that highlights:

- Top skills of the user.
- Market demand for the skills.
- Potential opportunities for the skills.
- Recommendations for the skills.

---

# Tech stak

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **HTTP client:** httpx
- **Data model:** pydantic
- **Testing:** pytest
- **Tooling:** uvicorn, PyCharm

---

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
