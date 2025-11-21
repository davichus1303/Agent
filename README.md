🚀 Overview
Agnostic Data Agent is a universal ingestion service designed to receive generic JSON payloads, automatically determine which rule to apply using the agent_rules.json configuration file, and execute the appropriate stored procedure in SQL Server asynchronously, without blocking the API.
This eliminates hard-coded partner-specific integrations and enables a scalable, domain-agnostic, configuration-driven ingestion pipeline.

🧠 Features
✔ Automatic rule selection via match_criteria
✔ Clean Architecture (domain-driven design separation)
✔ FastAPI with immediate 202 Accepted response
✔ Background asynchronous processing
✔ SQL Server Stored Procedure execution (PyODBC)
✔ Explicit and pass-through field mapping strategies
✔ Pytest test suite (unit tests + mocks)
✔ Docker + Docker Compose setup (API + SQL Server)
✔ GitHub Actions workflow for CI testing

📂 Project Structure
.
├── agent_rules.json
├── app
│   ├── api
│   │   └── ingest_controller.py
│   ├── core
│   │   └── config.py
│   ├── domain
│   │   ├── models.py
│   │   └── rule_engine.py
│   ├── infrastructure
│   │   ├── rules_loader.py
│   │   └── sql_connection.py
│   ├── main.py
│   ├── schemas
│   │   └── ingest_request.py
│   ├── services
│   │   ├── ingest_service.py
│   │   └── sp_executor.py
│   └── workers
│       └── background_worker.py
├── tests
│   ├── test_ingest_api.py
│   ├── test_rule_engine.py
│   └── test_sp_executor.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md


🧩 Architecture
The system follows Clean Architecture, ensuring separation of concerns and ease of maintenance.
🔹 API Layer (app/api)
Handles HTTP requests only.
Returns 202 Accepted immediately.
No business logic inside controllers.
🔹 Domain Layer (app/domain)
Contains the core intelligence:


RuleEngine: Determines which rule matches the received payload


Models: Pure business models


This layer is completely isolated from infrastructure.
🔹 Services Layer (app/services)
Coordinates domain and infrastructure:


IngestService: Background entry point


SPExecutor: Calls stored procedures


🔹 Infrastructure Layer (app/infrastructure)
Concrete implementations:


Loading agent_rules.json


SQL Server connection (PyODBC)


🔹 Workers (app/workers)
Handles queuing and async task execution (FastAPI background tasks).

⚙️ Running with Docker
1. Build and start
docker compose build
docker compose up

API docs available at:
👉 http://localhost:8000/api/docs
SQL Server runs at:
👉 localhost:1433

🔧 Environment Variables
Injected via docker-compose.yml:
MSSQL_HOST=mssql
MSSQL_USER=sa
MSSQL_PASSWORD=YourStrong!Passw0rd
MSSQL_DATABASE=master
RULES_FILE=/app/agent_rules.json

You may override using a .env file.

🔄 Rule Engine
The service reads all rules from agent_rules.json at startup.
Example rule:
{
  "domain_id": "FINANCE_PARTNER_X",
  "match_criteria": {
    "source_system": "SAP_CLOUD"
  },
  "target_action": {
    "type": "stored_procedure",
    "name": "sp_insert_transaction",
    "mapping_strategy": "explicit",
    "params_map": {
      "@ref_external": "transaction_id",
      "@amount": "total_amount",
      "@currency": "currency_code"
    }
  }
}

Adding new partners requires no code changes, only updating this file.

📥 Example Ingestion Request
Request
POST /api/ingest
Content-Type: application/json

{
  "source_system": "SAP_CLOUD",
  "transaction_id": "TX-99",
  "total_amount": 500.00,
  "currency_code": "USD"
}

Response
HTTP/1.1 202 Accepted
{
  "status": "accepted",
  "rule_applied": "FINANCE_PARTNER_X",
  "message": "Payload queued for processing"
}

Internal execution (async)
EXEC sp_insert_transaction 
     @ref_external='TX-99',
     @amount=500.00,
     @currency='USD'


🧪 Testing (Pytest)
Run all tests:
pytest -q

The test suite covers:


Rule matching logic


Stored procedure mapping


API ingest behavior (202 response + background queueing)


All external dependencies (SQL Server) are mocked.

🔁 CI Pipeline (GitHub Actions)
The workflow (.github/workflows/tests.yml) validates:


Python installation


Dependency installation


Pytest execution


Runs automatically on every push and pull request.
