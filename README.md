
# CREDO — Alternative Credit Scoring API

**Making credit assessment more inclusive through alternative financial data.**

CREDO is a B2B alternative credit-scoring API designed to help lenders assess borrowers who may have limited or no traditional credit history. It analyzes financial transaction patterns to generate a credit score, risk classification, and machine-learning prediction that can support lending decisions.

The project focuses on gig workers, first-time borrowers, small shopkeepers, and individuals whose financial activity may not be fully represented by traditional credit bureau records.

> **Project status:** MVP / Development  
> **Category:** Research-Based Project  
> **Application domain:** FinTech / Financial Inclusion  
> **Technical domain:** Machine Learning, REST APIs, Backend Engineering

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [Target Users](#target-users)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Machine Learning Approach](#machine-learning-approach)
- [API Documentation](#api-documentation)
- [Getting Started](#getting-started)
- [Testing with Postman](#testing-with-postman)
- [Project Structure](#project-structure)
- [Security](#security)
- [Current Limitations](#current-limitations)
- [Future Scope](#future-scope)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Problem Statement

Traditional credit assessment often relies heavily on credit bureau history and established financial records. This can make it difficult to evaluate applicants who are new to formal credit systems, even when they have regular income and consistent financial activity.

Examples include:

- Gig workers with irregular or platform-based earnings.
- First-time borrowers with limited credit history.
- Small shopkeepers and micro-business owners.
- Individuals with limited traditional credit records but observable transaction activity.

CREDO explores whether alternative financial indicators can provide lenders with additional information for credit assessment.

## Our Solution

CREDO provides a lender-facing REST API that connects a backend application to a machine-learning scoring service.

The service processes financial features derived from transaction data and returns a structured scoring response. Lenders can integrate this response into their own underwriting workflows.

CREDO is designed as a decision-support tool. Its score is not a guarantee of repayment and does not independently approve or reject a loan.

## Key Features

- **Alternative credit scoring:** Uses transaction-derived financial features to assess financial patterns.
- **Machine-learning predictions:** Uses a Random Forest classification model.
- **Risk classification:** Returns a risk band such as Low, Moderate, or High, according to the current scoring implementation.
- **REST API:** Provides a structured response through a Spring Boot backend.
- **ML service separation:** Uses FastAPI to expose the Python-based scoring service independently.
- **API key authentication:** Protects the Spring Boot API using an `X-API-Key` request header.
- **API testing:** Supports endpoint testing through Postman.
- **Modular architecture:** Separates the frontend, backend, and ML service.

## Target Users

CREDO is intended for:

- Banks and non-banking financial companies (NBFCs).
- FinTech lending platforms.
- Digital lenders and loan origination systems (LOS).
- Financial service providers exploring alternative credit assessment.

Borrower onboarding, consent collection, lending decisions, loan disbursal, and repayment servicing remain the responsibility of the integrating lender unless implemented through separate integrations.

---

## System Architecture

```text
                 Lender's Backend
                        |
                        | HTTPS + API Key
                        v
              +----------------------+
              |  CREDO REST API      |
              |  Spring Boot         |
              |  Port: 8080          |
              +----------------------+
                        |
                        | HTTP request
                        v
              +----------------------+
              |  FastAPI ML Service  |
              |  Python              |
              |  Port: 8000          |
              +----------------------+
                        |
                        v
              +----------------------+
              | Feature Processing   |
              | Random Forest Model  |
              +----------------------+
                        |
                        v
              Scoring Response
                        |
                        v
                 Lender's Backend
```

The React frontend provides the project's landing page and API documentation interface. It is separate from the lender's own application.

### Service responsibilities

| Component | Responsibility |
|---|---|
| React frontend | Landing page and API documentation |
| Spring Boot backend | REST endpoints, request handling, and API key authentication |
| FastAPI ML service | Python-based scoring and prediction |
| Random Forest model | Classification based on financial features |
| PostgreSQL | Planned for future persistent storage |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Java 21 | Backend development |
| Spring Boot | REST API and backend services |
| Gradle | Backend build and dependency management |
| Spring Security | API authentication |
| Python | Machine-learning implementation |
| FastAPI | ML service API |
| scikit-learn | Random Forest model |
| pandas / NumPy | Data processing and numerical computation |
| React | Frontend interface |
| Vite | Frontend development server and build tooling |
| JavaScript | Frontend development |
| Postman | API testing |
| Git and GitHub | Version control and source-code hosting |
| PostgreSQL | Planned database integration |

---

## Machine Learning Approach

CREDO uses transaction-derived features to explore alternative credit assessment.

### 1. Transaction data

The development dataset contains synthetic financial transaction records with fields such as:

- `customer_id`
- `transaction_date`
- `transaction_type`
- `amount`
- `balance`
- `transaction_mode`
- `narration`

The dataset is intended for development and experimentation, not as evidence of real-world lending performance.

### 2. Feature engineering

The current feature set includes financial indicators such as:

- Total and average income.
- Total and average expenses.
- Income and expense transaction counts.
- Average, minimum, and maximum balance.
- Total transaction count.
- Income and expense volatility.
- Expense-to-income ratio.
- Savings rate.

Additional transaction-activity indicators have also been explored, including transaction-mode diversity, transaction-type diversity, and average monthly transaction activity.

The exact features supplied to the trained model must match the feature list stored with that model.

### 3. Prediction

The Random Forest classifier produces a prediction and probability based on the features it receives. The scoring service maps model outputs into CREDO's score and risk-band response.

**Important:** The model's probability is a model estimate, not a guarantee of repayment or a validated probability of default. Its interpretation depends on the target labels used during training.

### 4. Model evaluation

Model evaluation has included classification metrics and analysis such as:

- Training and validation performance.
- Cross-validation.
- Confusion matrix.
- ROC curve.
- Feature importance.
- Feature correlation.

Further evaluation on representative, consented real-world data is required before the model can be considered suitable for lending decisions.

---

## API Documentation

### Base URL

Local Spring Boot backend:

```text
http://localhost:8080
```

### Score endpoint

**Endpoint:** `POST /v1/score`

The endpoint accepts a scoring request and returns a structured result. The exact request body must follow the DTO/schema implemented in the current backend and ML service.

### Authentication

CREDO's development API uses an API key in the request header.

```http
X-API-Key: YOUR_API_KEY
```

Do not include the API key in a URL, frontend source code, or a publicly committed file.

### Example response

The following example illustrates the response shape returned during development:

```json
[
  {
    "customerId": "TEST001",
    "credoScore": 82,
    "riskBand": "Low",
    "predictedOutcome": 1,
    "predictedProbability": 0.8177924530884291
  }
]
```

Field descriptions:

| Field | Description |
|---|---|
| `customerId` | Customer reference included in the scoring result |
| `credoScore` | Score generated by the current scoring implementation |
| `riskBand` | Risk category assigned by the implementation |
| `predictedOutcome` | Predicted class according to the trained model's label mapping |
| `predictedProbability` | Model probability associated with the class selected by the implementation |

The example is a development response, not a statement that a score of 82 guarantees creditworthiness.

### Error handling

Requests without a valid API key are expected to receive an HTTP `401 Unauthorized` response, for example:

```json
{
  "error": "Invalid or missing API key"
}
```

For the complete request schema and available routes, refer to the API documentation exposed by the running services and the corresponding request/response DTOs in the source code.

---

## Getting Started

### Prerequisites

Install the following tools before running the project:

- Git
- Java Development Kit (JDK) 21
- Python
- Node.js and npm
- Postman (for API testing)

### 1. Clone the repository

```bash
git clone https://github.com/codeloom-217/Credo.git
cd Credo
```

### 2. Start the FastAPI ML service

Open a terminal:

```powershell
cd ml-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The ML service should be available at:

```text
http://localhost:8000
```

FastAPI's interactive documentation is normally available at:

```text
http://localhost:8000/docs
```

**Note:** The `requirements.txt` file must exist in `ml-service`. If the project uses a different dependency file, install the dependencies listed there instead.

### 3. Start the Spring Boot backend

Open a second terminal:

```powershell
cd Backend
```

Set the development API key in the current PowerShell session:

```powershell
$env:CREDO_API_KEY = "replace-with-your-own-development-key"
```

Start the backend:

```powershell
.\gradlew.bat bootRun
```

The backend should be available at:

```text
http://localhost:8080
```

Keep the ML service running while testing an end-to-end scoring request.

### 4. Start the React frontend

Open a third terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, commonly:

```text
http://localhost:5173
```

### Running services

| Service | Default local port |
|---|---:|
| React / Vite | 5173 |
| Spring Boot | 8080 |
| FastAPI | 8000 |

These ports assume the applications are using their default configurations.

---

## Testing with Postman

1. Start the FastAPI ML service.
2. Start the Spring Boot backend with `CREDO_API_KEY` set.
3. Create a Postman request using `POST`.
4. Set the URL to `http://localhost:8080/v1/score`.
5. Select **Authorization → No Auth**.
6. Under **Headers**, add:

   | Key | Value |
   |---|---|
   | `X-API-Key` | The same key configured in the backend |

7. Under **Body → raw → JSON**, enter a request matching the actual `ScoreRequest` DTO and ML service schema.
8. Click **Send** and inspect the response.

A successful request should return the scoring response. An absent or incorrect API key should be rejected.

---

## Project Structure

The repository is organized into separate application components.

```text
Credo/
├── Backend/
│   ├── gradlew
│   ├── build.gradle
│   └── src/
│       └── main/
│           ├── java/
│           │   └── com/credo/Backend/
│           │       └── security/
│           │           └── SecurityConfig.java
│           └── resources/
│               └── application.properties
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   └── src/
│       ├── App.jsx
│       └── main.jsx
│
├── ml-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── scoring.py
│   │   ├── features.py
│   │   ├── momentum.py
│   │   └── schemas.py
│   ├── data/
│   ├── models/
│   └── requirements.txt
│
└── README.md
```

This is a representative structure. The exact contents of directories may change as development continues.

---

## Security

The current MVP includes API key authentication for the Spring Boot API.

Security considerations:

- Configure the API key through an environment variable.
- Never commit real API keys or other secrets to GitHub.
- Use HTTPS when deployed outside a local development environment.
- Keep the ML service private where possible and prevent unauthorized direct access.
- Validate request payloads and handle errors safely.
- Restrict access to financial data and collect it only with appropriate authorization and consent.
- Avoid logging sensitive financial information.

The current shared-key approach is a development-level authentication mechanism. It does not yet provide a complete lender registration, per-lender credential management, key revocation, or full audit system.

---

## Current Limitations

CREDO is an evolving research and development project.

- The transaction dataset used for model development is synthetic.
- Model performance on synthetic data may not generalize to real borrowers.
- PostgreSQL persistence is planned and may not yet be implemented.
- Automated lender registration and individual lender credential management are not yet complete.
- Account Aggregator consent and live financial-data ingestion are not yet represented as a completed production integration.
- Score calibration, fairness testing, explainability, and independent validation require further work.
- The score should not be used as the sole basis for a real lending decision.

## Future Scope

Potential next steps include:

- PostgreSQL integration for persistent storage.
- Secure, individual API credentials for each approved lender.
- API key rotation and revocation.
- Account Aggregator integration and consent-aware financial-data ingestion.
- Better monitoring, logging, rate limiting, and audit trails.
- Model explainability and more comprehensive evaluation.
- Validation on representative, appropriately consented financial datasets.
- Deployment with HTTPS, managed secrets, and service monitoring.
- Momentum analysis to track changes in financial activity over time, once implemented and validated.

---

## Contributing

Contributions, suggestions, and issue reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request describing the change.

For major changes, open an issue first to discuss the proposed approach.

## Disclaimer

CREDO is an educational and research-oriented prototype for exploring alternative credit scoring. It is not a licensed credit bureau, and its outputs are not guaranteed to be accurate, fair, or suitable for real-world underwriting. Production use would require appropriate legal and regulatory review, privacy protections, security controls, model validation, and lender oversight.

## License

No license has been specified yet. Unless a license is added to the repository, the project should not be assumed to be available for unrestricted reuse.


