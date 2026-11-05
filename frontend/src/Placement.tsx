import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";
type Placement = {
  id: string;
  answered: number;
  total: number;
  question: { skill: string; prompt: string; options: string[] } | null;
  result: {
    suggested_level: string;
    confidence: string;
    explanation: string;
  } | null;
};
export function Placement() {
  const [session, setSession] = useState<Placement | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  async function run(answer?: string) {
    setBusy(true);
    setError("");
    try {
      setSession(
        await api<Placement>(
          session
            ? `/placement-sessions/${session.id}/answers/`
            : "/placement-sessions/",
          {
            method: "POST",
            body: JSON.stringify({ answer, index: session?.answered }),
          },
        ),
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <p className="eyebrow">FIND YOUR STARTING POINT</p>
      <h1>
        A beginning,
        <br />
        not a label.
      </h1>
      <div className="card">
        {error && (
          <p role="alert" className="error">
            {error} <Link to="/account">Sign in</Link>
          </p>
        )}
        {!session ? (
          <>
            <p>
              Try four short text questions. This advisory placement checks
              vocabulary, grammar, and reading. It cannot measure listening or
              pronunciation.
            </p>
            <button disabled={busy} onClick={() => run()}>
              Start placement
            </button>
          </>
        ) : session.result ? (
          <>
            <h2>Try {session.result.suggested_level}</h2>
            <p>{session.result.explanation}</p>
            <p>Confidence: {session.result.confidence}</p>
            <Link className="button" to="/account">
              Choose your level
            </Link>
          </>
        ) : (
          <>
            <p className="eyebrow">
              {session.answered + 1} OF {session.total} ·{" "}
              {session.question?.skill}
            </p>
            <h2>{session.question?.prompt}</h2>
            <div className="row">
              {session.question?.options.map((a) => (
                <button key={a} disabled={busy} onClick={() => run(a)}>
                  {a}
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </>
  );
}
