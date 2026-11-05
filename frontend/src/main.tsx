import { Account } from "./Account";
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, NavLink, Route, Routes, Link } from "react-router-dom";
import "./styles.css";

function Home() {
  return (
    <>
      <p className="eyebrow">A LITTLE PRACTICE. A CLEARER VOICE.</p>
      <h1>
        Your next chapter
        <br />
        starts with a conversation.
      </h1>
      <p className="intro">
        Build everyday English, one thoughtful lesson at a time. Learn at your
        pace, with room to listen, try, and try again.
      </p>
      <Link className="button" to="/courses">
        Explore your classroom <span aria-hidden="true">↗</span>
      </Link>
      <section className="grid" aria-label="How you learn">
        {[
          [
            "01",
            "Understand",
            "Short explanations. Real-life examples. One clear goal.",
          ],
          [
            "02",
            "Practise",
            "Type or speak. Take your time and find your words.",
          ],
          ["03", "Grow", "Useful feedback and a practical next step."],
        ].map(([n, t, d]) => (
          <article className="card" key={n}>
            <p className="eyebrow">{n} / THE METHOD</p>
            <h2>{t}</h2>
            <p>{d}</p>
          </article>
        ))}
      </section>
      <aside className="note">
        <strong>Your voice belongs here.</strong> We focus on clear
        communication, respect English varieties, and always offer a typed
        alternative.
      </aside>
    </>
  );
}
function Courses() {
  return (
    <>
      <p className="eyebrow">YOUR LEARNING PATH</p>
      <h1>
        Small lessons.
        <br />
        Real progress.
      </h1>
      <div className="card">
        <h2>Your classroom is taking shape</h2>
        <p>
          Our first curriculum will cover everyday English from pre-A1 through
          B1. Published lessons will appear here.
        </p>
        <Link to="/">Return home</Link>
      </div>
    </>
  );
}
function App() {
  return (
    <BrowserRouter>
      <a href="#main" className="skip">
        Skip to content
      </a>
      <header>
        <Link to="/" className="brand" aria-label="SpeakWise home">
          <span className="mark" aria-hidden="true">
            s
          </span>
          SpeakWise<span className="badge">STUDIO</span>
        </Link>
        <nav aria-label="Main navigation">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/courses">Classroom</NavLink>
          <NavLink to="/progress">My progress</NavLink>
          <NavLink to="/account">My account</NavLink>
        </nav>
      </header>
      <main id="main" tabIndex={-1}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/courses" element={<Courses />} />
          <Route
            path="/progress"
            element={
              <div className="card">
                <h1>A little better, every day.</h1>
                <p>
                  Your learning history will live here once you complete your
                  first lesson.
                </p>
              </div>
            }
          />
          <Route path="/account" element={<Account />} />
          <Route
            path="*"
            element={
              <>
                <h1>Let’s find your way back.</h1>
                <Link to="/">Go home</Link>
              </>
            }
          />
        </Routes>
      </main>
      <footer>
        <span>SpeakWise · English for your everyday.</span>
        <span>Learn with clarity. Speak with purpose.</span>
      </footer>
    </BrowserRouter>
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
