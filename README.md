# Enterprise Quality Engineering Framework — ParaBank Financial Services

A test automation framework built for the **ParaBank Financial Services** demo platform. Developed using **Python 3.14+**, **Playwright**, and **Pytest**, this repository demonstrates layered architecture, parallel execution safety, explicit web-first resilience, REST API service separation, and collision-free test data generation.

---

# Technical Stack & Engineering Rationale

- **Language:** Python 3.14+ (Chosen for clean readability, rapid framework development, and expressive syntax)
- **UI Automation Engine:** Playwright (`pytest-playwright`) (Provides native auto-waiting mechanisms and web-first assertions, eliminating static delays)
- **API Service Layer:** Requests & Playwright API Request Context (Direct REST CRUD validation and background state seeding)
- **Test Runner:** Pytest (Offers flexible fixture lifecycle scoping, parameterization, and strict execution markers)
- **Parallelization:** `pytest-xdist` (Multi-worker execution leveraging function-scoped isolated browser contexts)
- **Reporting:** Allure Framework (Generates actionable execution reports, failure screenshots, and execution traces)
- **Data Strategy:** Faker & Sliced UUIDs (Guarantees dynamic, collision-free test data across concurrent workers)
- **CI/CD Integration:** GitHub Actions (Automated headless execution and report artifact publishing on SCM push and pull requests)

---

# Repository Architecture

```text
.
├── .github/
│   └── workflows/
│       └── regression.yml       # GitHub Actions CI pipeline execution
├── config/
│   └── settings.py              # Centralized environment settings and runtime constants
├── framework/
│   ├── api/
│   │   └── bank_client.py       # Isolated REST API Service Client
│   ├── pages/                   # Layered Page Object Model (POM)
│   │   ├── base_page.py         # Abstract base wrapper for Playwright interactions
│   │   ├── login_page.py        # Login UI page object
│   │   ├── register_page.py     # User Registration page object
│   │   ├── overview_page.py     # Account Overview navigation & verification
│   │   ├── transfer_page.py     # Funds Transfer page object
│   │   └── billpay_page.py      # Bill Payment page object
│   └── utils/
│       ├── data_factory.py      # Dynamic, parallel-safe test data factory
│       └── logger.py            # Structured logging wrapper
├── tests/
│   ├── conftest.py              # Pytest fixtures & browser context lifecycle
│   ├── test_ui_flows.py         # End-to-End UI User Journeys
│   ├── test_api_flows.py        # REST API CRUD Chained Scenarios
│   ├── test_negative_cases.py   # Edge-case & Negative Validation
│   └── test_datadriven.py       # Parameterized Data-Driven Tests
├── .gitignore                   # SCM exclusions
├── .python-version              # Python version lock (3.14)
├── pytest.ini                   # Pytest runtime options and marker declarations
├── requirements.txt             # Pinned project dependencies
├── README.md                    # Framework usage guide
└── TECHNICAL_NOTES.md           # Architecture, trade-offs, and scaling design note
```

---

# Prerequisites

- Python: 3.14+
- Git: SCM CLI installed
- Browsers: Chromium (managed via Playwright CLI)

---

# Local Setup & Environment Installation

## 1. Clone the Repository

```bash
git clone https://github.com/miguelbautistag/parabank-playwright-pytest-framework.git
cd parabank-playwright-pytest-framework
```

## 2. Configure Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install Pinned Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Install Playwright Binaries

```bash
playwright install chromium
```

---

# Test Execution Matrix

## Run Complete Suite (Sequential Execution)

```bash
pytest
```

## Run Full Suite in Parallel (2 Workers)

```bash
pytest -n 2
```

## Run Targeted Test Subsets by Marker

```bash
# Execute UI End-to-End Journeys
pytest -m ui

# Execute REST API Service Tests
pytest -m api

# Execute High-Priority Smoke Suite
pytest -m smoke

# Execute Negative & Edge Case Tests
pytest -m negative

# Execute Data-Driven Parameterized Tests
pytest -m datadriven
```

---

# Report Generation (Allure)

## 1. Execute Tests and Capture Results

```bash
pytest --alluredir=allure-results
```

## 2. Serve Report Locally

```bash
allure serve allure-results
```

## 3. Generate Static HTML Report Directory

```bash
allure generate allure-results -o allure-report --clean
```
