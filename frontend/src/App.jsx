
import "./index.css";
import { Routes, Route, Link } from "react-router-dom";

const features = [
  {
    number: "01",
    title: "Beyond credit history",
    description:
      "Understand financial behaviour through transaction patterns, income consistency, and everyday financial activity."
  },
  {
    number: "02",
    title: "Built for thin-file borrowers",
    description:
      "Explore alternative signals for gig workers, small businesses, and people with limited traditional credit history."
  },
  {
    number: "03",
    title: "Designed for integration",
    description:
      "A developer-oriented scoring API designed to connect with lender systems and existing underwriting workflows."
  }
];

const steps = [
  {
    number: "01",
    title: "Send transaction data",
    description:
      "Submit supported financial transaction records to the scoring service."
  },
  {
    number: "02",
    title: "Analyse financial behaviour",
    description:
      "The ML service processes transaction-derived features to estimate risk."
  },
  {
    number: "03",
    title: "Receive a score",
    description:
      "Get a structured response with a score and risk category."
  }
];

function LandingPage() {
  return (
    <div className="site-wrapper">
      <header className="navbar">
        <a className="brand" href="#home" aria-label="CREDO home">
          <span className="brand-symbol">C</span>
          <span>CREDO</span>
        </a>

        <nav className="nav-links" aria-label="Main navigation">
          <a href="#approach">Our approach</a>
          <a href="#how-it-works">How it works</a>
          <a href="#technology">Technology</a>
          <Link to="/docs">API Docs</Link>
        </nav>

        <a
          className="nav-cta"
          href="https://github.com/codeloom-217/Credo"
          target="_blank"
          rel="noreferrer"
        >
          View on GitHub <span aria-hidden="true">↗</span>
        </a>
      </header>

      <main>
        <section className="hero section-container" id="home">
          <div className="hero-content">
            <div className="eyebrow">
              <span className="status-dot" />
              ALTERNATIVE CREDIT INTELLIGENCE
            </div>

            <h1>
              A broader view of
              <br />
              financial <span>behaviour.</span>
            </h1>

            <p className="hero-description">
              CREDO explores a new approach to credit risk assessment using
              transaction-derived financial signals, built with lenders and
              underserved borrowers in mind.
            </p>

            <div className="hero-actions">
              <a className="button button-primary" href="#how-it-works">
                Explore the approach <span aria-hidden="true">→</span>
              </a>

              <Link className="text-link" to="/docs">
                Explore API Documentation <span aria-hidden="true">↗</span>
              </Link>
            </div>

            <div className="hero-note">
              <span className="note-line" />
              An early-stage alternative credit scoring project
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-topline">
              <span>ASSESSMENT PREVIEW</span>
              <span className="preview-label">ILLUSTRATIVE</span>
            </div>

            <div className="score-card">
              <div className="score-heading">
                <div>
                  <p className="small-label">CREDO SCORE</p>
                  <h2>Financial profile</h2>
                </div>
                <div className="profile-icon">C</div>
              </div>

              <div className="score-display">
                <div className="score-number">64</div>
                <div className="score-out-of">/ 100</div>
              </div>

              <div className="score-track">
                <div className="score-progress" />
              </div>

              <div className="score-meta">
                <span>Illustrative score</span>
                <span className="risk-pill">MODERATE</span>
              </div>

              <div className="card-divider" />

              <div className="signal-row">
                <div className="signal-icon">↗</div>
                <div className="signal-copy">
                  <strong>Transaction signals</strong>
                  <span>Income, spending and account activity</span>
                </div>
                <span className="signal-arrow">↗</span>
              </div>

              <div className="signal-row">
                <div className="signal-icon">◷</div>
                <div className="signal-copy">
                  <strong>Financial patterns</strong>
                  <span>Behaviour-derived model features</span>
                </div>
                <span className="signal-arrow">↗</span>
              </div>
            </div>

            <p className="visual-disclaimer">
              Concept illustration only. Not a real borrower assessment or
              production credit decision.
            </p>
          </div>
        </section>

        <section className="trust-strip">
          <div className="section-container trust-inner">
            <span className="trust-heading">BUILT WITH</span>
            <span className="tech-name">Python</span>
            <span className="trust-separator">/</span>
            <span className="tech-name">FastAPI</span>
            <span className="trust-separator">/</span>
            <span className="tech-name">Java</span>
            <span className="trust-separator">/</span>
            <span className="tech-name">Spring Boot</span>
            <span className="trust-separator">/</span>
            <span className="tech-name">PostgreSQL</span>
          </div>
        </section>

        <section className="approach-section section-container" id="approach">
          <div className="section-heading">
            <div>
              <p className="eyebrow">THE OPPORTUNITY</p>
              <h2>
                Financial potential
                <br />
                deserves a <span>wider lens.</span>
              </h2>
            </div>

            <p className="section-intro">
              Traditional credit histories do not always capture the full
              picture. CREDO investigates whether everyday financial activity
              can provide additional context for risk assessment.
            </p>
          </div>

          <div className="feature-grid">
            {features.map((feature) => (
              <article className="feature-card" key={feature.number}>
                <div className="feature-number">{feature.number}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <a href="#how-it-works" className="feature-link">
                  Learn more <span aria-hidden="true">↗</span>
                </a>
              </article>
            ))}
          </div>
        </section>

        <section className="process-section" id="how-it-works">
          <div className="section-container process-layout">
            <div className="process-intro">
              <p className="eyebrow">HOW IT WORKS</p>
              <h2>
                From transaction
                <br />
                data to <span>insight.</span>
              </h2>
              <p>
                A simple view of the intended scoring workflow, from structured
                input to an API response.
              </p>
            </div>

            <div className="steps-list">
              {steps.map((step) => (
                <article className="step" key={step.number}>
                  <div className="step-number">{step.number}</div>
                  <div className="step-content">
                    <h3>{step.title}</h3>
                    <p>{step.description}</p>
                  </div>
                  <span className="step-arrow" aria-hidden="true">↗</span>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section
          className="technology-section section-container"
          id="technology"
        >
          <div className="technology-copy">
            <p className="eyebrow">THE TECHNOLOGY</p>
            <h2>
              Practical engineering.
              <br />
              <span>Purposeful intelligence.</span>
            </h2>
            <p>
              CREDO brings together a Python-based machine learning service and
              a Java backend as an early foundation for an alternative credit
              scoring API.
            </p>
            <Link className="button button-primary" to="/docs">
              Read the API docs <span aria-hidden="true">→</span>
            </Link>
          </div>

          <div className="architecture-card">
            <div className="architecture-label">SYSTEM OVERVIEW</div>

            <div className="architecture-node">
              <span className="node-index">01</span>
              <div>
                <strong>Lender application</strong>
                <span>API request</span>
              </div>
            </div>

            <div className="architecture-connector"><span /></div>

            <div className="architecture-node">
              <span className="node-index">02</span>
              <div>
                <strong>Spring Boot</strong>
                <span>Backend API layer</span>
              </div>
            </div>

            <div className="architecture-connector"><span /></div>

            <div className="architecture-node">
              <span className="node-index">03</span>
              <div>
                <strong>FastAPI + ML</strong>
                <span>Scoring service</span>
              </div>
            </div>

            <div className="architecture-connector"><span /></div>

            <div className="architecture-node">
              <span className="node-index">04</span>
              <div>
                <strong>Structured response</strong>
                <span>Score and risk category</span>
              </div>
            </div>

            <p className="architecture-note">
              Conceptual architecture. Availability and integration depend on
              the current implementation and deployment.
            </p>
          </div>
        </section>

        <section className="cta-section section-container">
          <div className="cta-content">
            <p className="eyebrow">DEVELOPER RESOURCES</p>
            <h2>
              Integrate CREDO.
              <br />
              <span>Explore the API.</span>
            </h2>
            <p>
              Learn how a lender application sends a request to the Java API
              and receives a structured scoring response.
            </p>
            <Link className="button button-light" to="/docs">
              Explore API Documentation <span aria-hidden="true">→</span>
            </Link>
          </div>
          <div className="cta-mark" aria-hidden="true">C.</div>
        </section>
      </main>

      <footer className="footer section-container">
        <a className="brand footer-brand" href="#home">
          <span className="brand-symbol">C</span>
          <span>CREDO</span>
        </a>

        <p>
          An early-stage project exploring alternative credit risk assessment.
        </p>

        <Link to="/docs">API Documentation</Link>

        <a
          href="https://github.com/codeloom-217/Credo"
          target="_blank"
          rel="noreferrer"
        >
          GitHub ↗
        </a>

        <span className="copyright">© {new Date().getFullYear()} CREDO</span>
      </footer>
    </div>
  );
}

function DocsPage() {
  const requestExample = `{
  "transactions": [
    {
      "customer_id": "TEST001",
      "transaction_date": "2026-06-01",
      "transaction_type": "CREDIT",
      "amount": 15000,
      "balance": 18000,
      "transaction_mode": "UPI",
      "narration": "Payment received"
    }
  ]
}`;

  const responseExample = `[
  {
    "customerId": "TEST001",
    "credoScore": 82,
    "riskBand": "Low",
    "predictedOutcome": 1,
    "predictedProbability": 0.8177924530884291
  }
]`;

  return (
    <div className="site-wrapper docs-page">
      <header className="navbar">
        <Link className="brand" to="/">
          <span className="brand-symbol">C</span>
          <span>CREDO</span>
        </Link>

        <nav className="nav-links" aria-label="Documentation navigation">
          <Link to="/">Home</Link>
          <a href="#getting-started">Getting started</a>
          <a href="#java-integration">Java integration</a>
          <a href="#api-reference">API reference</a>
        </nav>

        <a
          className="nav-cta"
          href="https://github.com/codeloom-217/Credo"
          target="_blank"
          rel="noreferrer"
        >
          GitHub ↗
        </a>
      </header>

      <main className="section-container docs-content">
        <section id="getting-started" className="docs-hero">
          <p className="eyebrow">CREDO DEVELOPER PORTAL</p>
          <h1>
            API documentation<span>.</span>
          </h1>
          <p className="hero-description">
            Learn how to integrate CREDO's alternative credit scoring API
            into a lender application using the Java Spring Boot backend.
          </p>

          <div className="docs-badges">
            <span>REST API</span>
            <span>JSON</span>
            <span>Spring Boot</span>
            <span>FastAPI ML</span>
          </div>
        </section>

        <section className="docs-section">
          <p className="eyebrow">OVERVIEW</p>
          <h2>How the integration works</h2>
          <p>
            A client sends its request to the Spring Boot backend. The Java
            service processes the request and communicates with the FastAPI
            machine learning service. The response is returned to the client
            through Java.
          </p>

          <div className="docs-flow">
            <article className="docs-flow-node">
              <span>01</span>
              <h3>Lender application</h3>
              <p>Sends a JSON request</p>
            </article>

            <div className="docs-flow-arrow">↓</div>

            <article className="docs-flow-node docs-flow-primary">
              <span>02</span>
              <h3>Java · Spring Boot</h3>
              <p>Public backend endpoint: POST /v1/score</p>
            </article>

            <div className="docs-flow-arrow">↓</div>

            <article className="docs-flow-node">
              <span>03</span>
              <h3>Python · FastAPI</h3>
              <p>Feature processing and model prediction</p>
            </article>

            <div className="docs-flow-arrow">↓</div>

            <article className="docs-flow-node">
              <span>04</span>
              <h3>JSON response</h3>
              <p>Returned to the client through Spring Boot</p>
            </article>
          </div>

          <p className="docs-note">
            The diagram describes the intended architecture. The exact internal
            request and field mapping must match the current backend client
            and ML service implementation.
          </p>
        </section>

        <section className="docs-section" id="java-integration">
          <p className="eyebrow">JAVA INTEGRATION</p>
          <h2>Connect through Spring Boot</h2>
          <p>
            Clients should call the Java API, not the internal ML service
            directly. This keeps validation, authentication and API behaviour
            in the backend layer.
          </p>

          <div className="docs-info-grid">
            <article className="docs-info-card">
              <span>HTTP method</span>
              <strong>POST</strong>
            </article>
            <article className="docs-info-card">
              <span>Backend endpoint</span>
              <strong>/v1/score</strong>
            </article>
            <article className="docs-info-card">
              <span>Content type</span>
              <strong>application/json</strong>
            </article>
            <article className="docs-info-card">
              <span>Local backend</span>
              <strong>localhost:8080</strong>
            </article>
          </div>

          <h3>Local development URL</h3>
          <pre className="docs-code">
            <code>http://localhost:8080/v1/score</code>
          </pre>

          <p className="docs-note">
            Localhost is accessible only from your own computer. After
            deployment, replace it with the public backend URL.
          </p>
        </section>

        <section className="docs-section" id="api-reference">
          <p className="eyebrow">API REFERENCE</p>
          <h2>Score endpoint</h2>
          <div className="endpoint-line">
            <span className="http-method">POST</span>
            <code>/v1/score</code>
          </div>

          <h3>Request body example</h3>
          <p>
            This is a conceptual example of transaction input. Verify the
            actual required JSON structure against your Java
            <code> ScoreRequest </code> DTO before using it.
          </p>

          <pre className="docs-code">
            <code>{requestExample}</code>
          </pre>

          <button
            className="button button-primary docs-copy-button"
            onClick={() => navigator.clipboard.writeText(requestExample)}
          >
            Copy request JSON
          </button>

          <h3>Response example</h3>
          <p>
            Example response from development testing. Actual scores and
            probabilities depend on the supplied data and model.
          </p>

          <pre className="docs-code">
            <code>{responseExample}</code>
          </pre>

          <button
            className="button button-primary docs-copy-button"
            onClick={() => navigator.clipboard.writeText(responseExample)}
          >
            Copy response JSON
          </button>

          <h3>Response fields</h3>
          <div className="docs-table-wrap">
            <table className="docs-table">
              <thead>
                <tr>
                  <th>Field</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>customerId</code></td>
                  <td>Identifier associated with the scoring request.</td>
                </tr>
                <tr>
                  <td><code>credoScore</code></td>
                  <td>Numeric CREDO score returned by the backend.</td>
                </tr>
                <tr>
                  <td><code>riskBand</code></td>
                  <td>Risk category, such as Low or Moderate.</td>
                </tr>
                <tr>
                  <td><code>predictedOutcome</code></td>
                  <td>Predicted class returned by the model.</td>
                </tr>
                <tr>
                  <td><code>predictedProbability</code></td>
                  <td>Model probability associated with its predicted class.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="docs-section">
          <p className="eyebrow">AUTHENTICATION</p>
          <h2>Secure your API requests</h2>
          <p>
            The current development backend uses HTTP Basic authentication.
            Production deployments should use securely managed credentials
            over HTTPS and avoid exposing credentials in browser code.
          </p>
          <p className="docs-note">
            Never place database passwords, model service secrets or backend
            credentials in the React frontend or public documentation.
          </p>
        </section>

        <section className="docs-section">
          <p className="eyebrow">TESTING</p>
          <h2>Test with Postman</h2>
          <ol className="docs-list">
            <li>Start the Spring Boot backend.</li>
            <li>Ensure the FastAPI ML service is running and reachable.</li>
            <li>Create a POST request to the local score endpoint.</li>
            <li>Set the request body to JSON using the verified request schema.</li>
            <li>Configure the development authentication and send the request.</li>
            <li>Inspect the returned score and risk category.</li>
          </ol>
        </section>

        <section className="docs-bottom-cta">
          <h2>Ready to explore the code?</h2>
          <p>Review the CREDO implementation and follow its development.</p>
          <a
            className="button button-light"
            href="https://github.com/codeloom-217/Credo"
            target="_blank"
            rel="noreferrer"
          >
            View CREDO on GitHub ↗
          </a>
          <p><Link to="/">← Back to landing page</Link></p>
        </section>
      </main>

      <footer className="footer section-container">
        <Link className="brand footer-brand" to="/">
          <span className="brand-symbol">C</span>
          <span>CREDO</span>
        </Link>
        <p>Alternative credit intelligence · Developer documentation</p>
        <span className="copyright">
          © {new Date().getFullYear()} CREDO
        </span>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/docs" element={<DocsPage />} />
    </Routes>
  );
}

export default App;
