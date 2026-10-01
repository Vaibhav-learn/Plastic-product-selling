import { useState } from 'react';

export default function App() {
    const [notice, setNotice] = useState('');

    function handleSubmit(event) {
    event.preventDefault();
    setNotice('Sign-in will be available when the API is connected.');
    }

    return (
    <main className="login-layout">
        <section className="brand-panel" aria-label="Agency identity">
        <a className="wordmark" href="./" aria-label="Plastic Distribution home">
            <span className="brand-mark" aria-hidden="true">PD</span>
            <span>Plastic Distribution</span>
        </a>
        <div className="brand-copy">
            <p className="eyebrow">AGENCY OPERATIONS</p>
            <h1>Every order,<br />in its place.</h1>
            <p className="brand-description">
            A clearer working day for the people moving products from warehouse to store.
            </p>
        </div>
        <div className="panel-footer">
            <span className="status-dot" aria-hidden="true" />
            <span>Workspace setup in progress</span>
        </div>
        </section>

        <section className="form-panel" aria-labelledby="login-title">
        <div className="form-wrap">
            <p className="eyebrow form-eyebrow">TEAM ACCESS</p>
            <h2 id="login-title">Sign in</h2>
            <p className="form-intro">Use your registered phone number to continue.</p>

            <form onSubmit={handleSubmit}>
            <label htmlFor="phone">Phone number</label>
            <input
            id="phone"
            name="phone"
              type="tel"
              autoComplete="username"
              placeholder="10-digit phone number"
              required
            />

            <label htmlFor="password">Password</label>
            <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="Enter your password"
            required
            />

            <button type="submit">Continue <span aria-hidden="true">→</span></button>
            <p className="form-notice" role="status" aria-live="polite">
              {notice || 'Authentication is not connected yet.'}
            </p>
          </form>
        </div>
        <footer className="form-footer">Plastic Distribution Agency Management</footer>
      </section>
    </main>
  );
}