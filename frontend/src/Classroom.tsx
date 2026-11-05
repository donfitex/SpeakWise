import { Recorder } from "./Recorder";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "./api";
export type Activity = {
  id: string;
  kind: string;
  prompt: string;
  example: string;
  hint: string;
  options: string[];
  cues: Record<string, unknown>;
};
export type Session = {
  id: string;
  title: string;
  objective: string;
  explanation: string;
  position: number;
  total: number;
  completed: boolean;
  activity: Activity | null;
  turns: { speaker: string; content: string }[];
};
type Course = {
  id: string;
  title: string;
  units: {
    id: string;
    title: string;
    level: string;
    lessons: {
      id: string;
      title: string;
      objective: string;
      minutes: number;
      prerequisites: string[];
    }[];
  }[];
};
export function Courses() {
  const [courses, setCourses] = useState<Course[]>([]),
    [loading, setLoading] = useState(true),
    [error, setError] = useState("");
  const navigate = useNavigate();
  async function load() {
    setError("");
    setLoading(true);
    try {
      setCourses((await api<{ results: Course[] }>("/courses/")).results);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    void load();
  }, []);
  async function start(id: string) {
    setError("");
    try {
      const s = await api<Session>("/lesson-sessions/", {
        method: "POST",
        body: JSON.stringify({ lesson_version: id }),
      });
      navigate(`/classroom/${s.id}`);
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <>
      <p className="eyebrow">YOUR LEARNING PATH</p>
      <h1>
        Small lessons.
        <br />
        Real progress.
      </h1>
      <p className="intro">
        Choose a starting point. Every lesson gives you a model, practice, and
        room to retry.
      </p>
      {loading && <p role="status">Opening your course map…</p>}
      {error && (
        <div className="error" role="alert">
          {error}
          <div className="row">
            <button onClick={load}>Retry</button>
            <Link to="/account">Sign in</Link>
          </div>
        </div>
      )}
      {!loading && !error && !courses.length && (
        <p className="card">No published lessons yet. Check back soon.</p>
      )}
      {courses.map((c) => (
        <section key={c.id}>
          <h2>{c.title}</h2>
          <p className="small">
            Synthetic pilot content · educational review pending
          </p>
          {c.units.map((u) => (
            <section key={u.id}>
              <h3>{u.title}</h3>
              <div className="grid" style={{ marginTop: 12 }}>
                {u.lessons.map((l) => (
                  <article className="card" key={l.id}>
                    <span className="pill">
                      {u.level} · {l.minutes} min
                    </span>
                    <h2>{l.title}</h2>
                    <p>{l.objective}</p>
                    {l.prerequisites.length > 0 && (
                      <p className="small">
                        Complete prerequisite lessons first.
                      </p>
                    )}
                    <button onClick={() => start(l.id)}>
                      Start or resume <span aria-hidden="true">→</span>
                    </button>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </section>
      ))}
    </>
  );
}
export function Classroom() {
  const { id } = useParams();
  const [session, setSession] = useState<Session | null>(null),
    [answer, setAnswer] = useState(""),
    [error, setError] = useState(""),
    [feedback, setFeedback] = useState(""),
    [busy, setBusy] = useState(false),
    [hint, setHint] = useState(false);
  async function load() {
    setError("");
    try {
      setSession(await api<Session>(`/lesson-sessions/${id}/`));
    } catch (e) {
      setError((e as Error).message);
    }
  }
  useEffect(() => {
    void load();
  }, [id]);
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!session?.activity) return;
    setBusy(true);
    setError("");
    try {
      const data = await api<{
        session: Session;
        attempt: { result: { feedback: string; correct: boolean } };
      }>(`/lesson-sessions/${id}/turns/`, {
        method: "POST",
        body: JSON.stringify({
          activity_id: session.activity.id,
          answer,
          request_id: crypto.randomUUID(),
        }),
      });
      setSession(data.session);
      setFeedback(data.attempt.result.feedback);
      if (data.attempt.result.correct) {
        setAnswer("");
        setHint(false);
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <Link to="/courses">← Course map</Link>
      {error && (
        <div className="error" role="alert">
          {error}
          <button onClick={load}>Reload lesson</button>
        </div>
      )}
      {!session && !error && <p role="status">Preparing your lesson…</p>}
      {session && (
        <>
          <p className="eyebrow">YOUR PRIVATE CLASSROOM · SCRIPTED TEACHER</p>
          <h1>{session.title}</h1>
          <p className="intro">{session.objective}</p>
          <label htmlFor="lesson-progress">
            {session.position} of {session.total} activities complete
          </label>
          <progress
            id="lesson-progress"
            value={session.position}
            max={session.total}
          />
          <div className="split" style={{ marginTop: 24 }}>
            <section className="card">
              <div className="teacher">
                <strong>Your teacher</strong>
                <p>{session.explanation}</p>
              </div>
              {session.completed ? (
                <>
                  <h2>You made room for progress.</h2>
                  <p>
                    Lesson complete. Try one of the model phrases in your day,
                    then come back for a short review.
                  </p>
                  <Link className="button" to="/progress">
                    See your next step
                  </Link>
                </>
              ) : (
                session.activity && (
                  <>
                    <p className="eyebrow">
                      {session.activity.kind} · YOUR TURN
                    </p>
                    <h2>{session.activity.prompt}</h2>
                    <p>
                      Model: <strong>{session.activity.example}</strong>
                    </p>
                    {session.activity.kind === "speaking" && (
                      <Recorder key={session.activity.id} />
                    )}
                    <form onSubmit={submit}>
                      <label>
                        Your answer
                        {session.activity.options.length ? (
                          <select
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            required
                          >
                            <option value="">Choose an answer</option>
                            {session.activity.options.map((o) => (
                              <option key={o}>{o}</option>
                            ))}
                          </select>
                        ) : (
                          <textarea
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            required
                            maxLength={4000}
                            rows={3}
                          />
                        )}
                      </label>
                      <div className="row">
                        <button disabled={busy || !answer.trim()}>
                          {busy ? "Checking…" : "Check my answer"}
                        </button>
                        <button
                          type="button"
                          className="secondary"
                          onClick={() => setHint(!hint)}
                          aria-expanded={hint}
                        >
                          A little help
                        </button>
                      </div>
                      {hint && <p className="note">{session.activity.hint}</p>}
                    </form>
                  </>
                )
              )}
              {feedback && (
                <p role="status" className="success">
                  {feedback}
                </p>
              )}
            </section>
            <aside className="card">
              <p className="eyebrow">LESSON NOTES</p>
              <h2>One step at a time.</h2>
              <p>
                Your progress saves after every answer. Leave and resume
                whenever you need.
              </p>
              <p className="small">
                Typed practice evaluates the reference task, not pronunciation
                or overall English proficiency.
              </p>
              <details>
                <summary>Our conversation</summary>
                {session.turns.map((t, i) => (
                  <p key={i}>
                    <strong>
                      {t.speaker === "teacher" ? "Teacher" : "You"}:
                    </strong>{" "}
                    {t.content}
                  </p>
                ))}
              </details>
            </aside>
          </div>
        </>
      )}
    </>
  );
}
