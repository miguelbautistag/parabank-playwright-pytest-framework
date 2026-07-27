# Architectural Design & Engineering Notes

**Candidate:** Miguel Bautista
**Role:** QA Automation Engineer
**Target Domain:** Financial Services (ParaBank Demo Application)
**Execution Stack:** Python 3.14+, Playwright (`pytest-playwright`), Pytest, `pytest-xdist`, Allure, Faker

---

## 1. Primary Architectural Choices & Engineering Trade-offs

### 1. Layered Page Object Model (POM) with Separation of Concerns
* **Decision:** Encapsulated page locators and browser interactions inside `framework/pages/`, keeping them separated from business assertions inside `tests/`.
* **Rationale:** UI locators and interaction patterns change frequently as application layouts evolve. Keeping presentation logic inside dedicated Page Objects ensures that locator changes require updates in a single class rather than across multiple test cases.
* **Trade-off:** Introduces initial abstraction files compared to writing raw Playwright scripts. However, it significantly reduces maintenance overhead as the suite grows.

### 2. Isolated REST API Service Client (`bank_client.py`)
* **Decision:** Constructed a dedicated REST API service client alongside UI Page Objects rather than forcing all setup steps through the browser interface.
* **Rationale:** Running setup operations through the UI increases execution duration and risk. Isolating API communication inside a dedicated client allows API endpoints to be validated independently and provides background data seeding for UI tests.
* **Trade-off:** Requires maintaining JSON request models alongside UI Page Objects.

### 3. Collision-Free Data Strategy via Sliced UUIDs
* **Decision:** Built a `DataFactory` utilizing `Faker` combined with short UUID slices (`uuid.uuid4().hex[:8]`).
* **Rationale:** ParaBank uses a shared database state. Generating static usernames or account names during parallel execution causes database uniqueness collisions. Appending short UUIDs ensures each worker generates unique entities.
* **Trade-off:** Test data is dynamic and cannot be hardcoded for debugging. Diagnostics rely on execution logs and Allure attachments.

---

## 2. Flakiness Prevention Strategy

1. **Zero Hardcoded Delays (`time.sleep()`):** Static delays make suites slow and unreliable under varying network conditions. All UI interactions rely on Playwright’s auto-waiting mechanisms (actionability, visibility, DOM attachment).
2. **Web-First Auto-Waiting Assertions:** Utilized Playwright's `expect(locator)` assertions, which poll the DOM dynamically until conditions are met or timeouts expire.
3. **Thread-Safe Worker Isolation:** Configured function-scoped `browser_context` fixtures per `pytest-xdist` worker (`gw0`, `gw1`). Each test executes within an isolated browser context with independent cookies and session storage.

---

## 3. Scaling Strategy (500+ Tests & Multiple Contributors)

If the automation suite grows to hundreds of tests with multiple engineering contributors, the following adjustments should be prioritized:

1. **Domain-Based Directory Organization:** Refactor `framework/pages/` and `tests/` into domain-bounded subdirectories (`banking/`, `customer_service/`, `admin/`) to prevent merge conflicts and clarify ownership.
2. **CI Pipeline Sharding:** Transition from local parallel workers (`pytest -n 2`) to GitHub Actions CI matrix sharding (`strategy: matrix`), distributing test execution across isolated cloud runners.
3. **API-Driven Preconditions:** Replace UI setup flows (such as form-based registration) with direct REST API state seeding to reduce UI execution time.

---

## 4. Future Enhancements & Refactoring Roadmap

With additional development time, the following improvements would be introduced:

1. **Containerized Execution Environment:** Package the framework using `Dockerfile` and `docker-compose.yml` to standardize execution dependencies across developer workstations and CI runners.
2. **Visual Regression Validation:** Integrate Playwright screenshot comparisons (`expect(page).to_have_screenshot()`) for visual dashboard components.
3. **Contract Testing:** Introduce JSON Schema validation for the REST API client to catch backend schema changes before running end-to-end tests.
