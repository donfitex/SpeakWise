import { Dashboard } from "./Dashboard";
import { useState, useEffect } from "react";
import { api } from "./api";
import { Classroom, Courses } from "./Classroom";
import { Placement } from "./Placement";
import { Account } from "./Account";
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, NavLink, Route, Routes, Link } from "react-router-dom";
import "./styles.css";

function Home() {
  const [signedIn, setSignedIn] = useState(false);
  useEffect(() => {
    api("/learners/me/")
      .then(() => setSignedIn(true))
      .catch(() => {});
  }, []);
  if (signedIn) return <Dashboard />;
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
          <Route path="/classroom/:id" element={<Classroom />} />
          <Route path="/placement" element={<Placement />} />
          <Route path="/" element={<Home />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/progress" element={<Dashboard />} />
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
