
import "./index.css";

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
    description: "Submit supported financial transaction records to the scoring service."
  },
  {
    number: "02",
    title: "Analyse financial behaviour",
    description: "The ML service processes transaction-derived features to estimate risk."
  },
  {
    number: "03",
    title: "Receive a score",
    description: "Get a structured response with a score and risk category."
  }
];

function App() {
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

              <a
                className="text-link"
                href="https://github.com/codeloom-217/Credo"
                target="_blank"
                rel="noreferrer"
              >
                Explore the code <span aria-hidden="true">↗</span>
              </a>
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

        <section className="technology-section section-container" id="technology">
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

            <div className="architecture-connector">
              <span />
            </div>

            <div className="architecture-node">
              <span className="node-index">02</span>
              <div>
                <strong>Spring Boot</strong>
                <span>Backend API layer</span>
              </div>
            </div>

            <div className="architecture-connector">
              <span />
            </div>

            <div className="architecture-node">
              <span className="node-index">03</span>
              <div>
                <strong>FastAPI + ML</strong>
                <span>Scoring service</span>
              </div>
            </div>

            <div className="architecture-connector">
              <span />
            </div>

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
            <p className="eyebrow">FOLLOW THE PROJECT</p>
            <h2>
              Building a more
              <br />
              <span>complete picture.</span>
            </h2>
            <p>
              Explore the codebase and follow the development of CREDO's
              alternative credit scoring API.
            </p>
            <a
              className="button button-light"
              href="https://github.com/codeloom-217/Credo"
              target="_blank"
              rel="noreferrer"
            >
              Explore CREDO on GitHub <span aria-hidden="true">↗</span>
            </a>
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

export default App;
