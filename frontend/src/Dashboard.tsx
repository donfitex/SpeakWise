import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "./api";
import type { Profile } from "./Account";
import type { Session } from "./Classroom";
type Recommendation = {
  lesson_version: string | null;
  title?: string;
  review?: boolean;
  reason: string;
};
type Progress = {
  skills: {
    skill: string;
    estimate: number;
    evidence_count: number;
    next_review_due: string;
  }[];
  note: string;
};
type Summary = {
  completed_lessons: number;
  practice_attempts: number;
  recorded_practice_seconds: number;
  resume: { id: string; title: string }[];
};
type History = {
  count: number;
  next: string | null;
  results: {
    id: string;
    title: string;
    activity_type: string;
    created_at: string;
    assessment_id: string | null;
    result: {
      feedback: string;
      correct: boolean;
      next_step: string;
      rubric_version: number;
    };
  }[];
};
export function Dashboard() {
  const [data, setData] = useState<{
      profile: Profile;
      recommendation: Recommendation;
      progress: Progress;
      summary: Summary;
    } | null>(null),
    [history, setHistory] = useState<History | null>(null),
    [page, setPage] = useState(1),
    [error, setError] = useState(""),
    [message, setMessage] = useState(""),
    [report, setReport] = useState(""),
    [reason, setReason] = useState("");
  const navigate = useNavigate();
  async function load() {
    setError("");
    try {
      const [profile, recommendation, progress, summary] = await Promise.all([
        api<Profile>("/learners/me/"),
        api<Recommendation>("/learners/me/recommendations/"),
        api<Progress>("/learners/me/progress/"),
        api<Summary>("/learners/me/summary/"),
      ]);
      setData({ profile, recommendation, progress, summary });
    } catch (e) {
      setError((e as Error).message);
    }
  }
  useEffect(() => {
    void load();
  }, []);
  useEffect(() => {
    api<History>(`/learners/me/history/?page=${page}`)
      .then(setHistory)
      .catch((e) => setError((e as Error).message));
  }, [page]);
  async function start() {
    if (!data?.recommendation.lesson_version) return;
    try {
      const s = await api<Session>("/lesson-sessions/", {
        method: "POST",
        body: JSON.stringify({
          lesson_version: data.recommendation.lesson_version,
          review: data.recommendation.review,
        }),
      });
      navigate(`/classroom/${s.id}`);
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <>
      <p className="eyebrow">YOUR LEARNING JOURNAL</p>
      <h1>
        {data
          ? `${data.profile.display_name}, keep finding your words.`
          : "A little better, every day."}
      </h1>
      {error && (
        <div className="error" role="alert">
          {error}
          <div className="row">
            <button onClick={load}>Retry</button>
            <Link to="/account">Sign in</Link>
          </div>
        </div>
      )}
      {!data && !error && <p role="status">Gathering your learning notes…</p>}
      {data && (
        <>
          <p className="intro">
            {data.profile.level} · {data.profile.daily_minutes} minutes a day ·{" "}
            {data.profile.goals.join(", ") || "Choose a goal in My account"}
          </p>
          <div className="grid">
            {[
              ["Lessons completed", data.summary.completed_lessons],
              ["Practice attempts", data.summary.practice_attempts],
              [
                "Recorded practice",
                `${Math.round(data.summary.recorded_practice_seconds)} seconds`,
              ],
            ].map(([label, value]) => (
              <article className="card" key={label}>
                <p className="eyebrow">{label}</p>
                <h2>{value}</h2>
              </article>
            ))}
          </div>
          <section className="note" style={{ justifyContent: "space-between" }}>
            <div>
              <p className="eyebrow">YOUR NEXT STEP</p>
              <h2>
                {data.recommendation.title || "Keep the conversation going"}
              </h2>
              <p>{data.recommendation.reason}</p>
            </div>
            {data.recommendation.lesson_version ? (
              <button onClick={start}>Start practice →</button>
            ) : (
              <Link className="button" to="/courses">
                Review course map
              </Link>
            )}
          </section>
          {!!data.summary.resume.length && (
            <section>
              <h2>Pick up where you paused</h2>
              {data.summary.resume.map((s) => (
                <p key={s.id}>
                  <Link to={`/classroom/${s.id}`}>{s.title} →</Link>
                </p>
              ))}
            </section>
          )}
          <section>
            <h2>Your skill notes</h2>
            <p className="small">{data.progress.note}</p>
            {!data.progress.skills.length ? (
              <p className="card">
                Complete a controlled text activity to begin collecting
                evidence. There is no overall mastery score.
              </p>
            ) : (
              <div className="grid">
                {data.progress.skills.map((s) => (
                  <article className="card" key={s.skill}>
                    <h3>{s.skill}</h3>
                    <p>Recent task estimate: {s.estimate.toFixed(1)} / 5</p>
                    <p>
                      {s.evidence_count} evidence{" "}
                      {s.evidence_count === 1 ? "record" : "records"}
                    </p>
                    <p className="small">
                      Review due{" "}
                      {new Date(s.next_review_due).toLocaleDateString()}
                    </p>
                  </article>
                ))}
              </div>
            )}
          </section>
          <section>
            <h2>Practice history</h2>
            {message && (
              <p role="status" className="success">
                {message}
              </p>
            )}
            {!history?.results.length ? (
              <p className="card">Your first attempt will appear here.</p>
            ) : (
              <div className="stack">
                {history.results.map((a) => (
                  <article className="card" key={a.id}>
                    <div className="row">
                      <h3>{a.title}</h3>
                      <span className="pill">
                        {a.activity_type} ·{" "}
                        {a.result.correct
                          ? "Reference matched"
                          : "Retry suggested"}
                      </span>
                    </div>
                    <p>{a.result.feedback}</p>
                    <p>{a.result.next_step}</p>
                    <p className="small">
                      Rubric version {a.result.rubric_version} ·{" "}
                      {new Date(a.created_at).toLocaleString()}
                    </p>
                    {a.assessment_id && (
                      <button
                        className="secondary"
                        onClick={() => setReport(a.assessment_id!)}
                      >
                        Report inaccurate feedback
                      </button>
                    )}
                  </article>
                ))}
                <div className="row">
                  <button
                    disabled={page === 1}
                    onClick={() => setPage(page - 1)}
                  >
                    Previous
                  </button>
                  <span>
                    Page {page} · {history.count} attempts
                  </span>
                  <button
                    disabled={!history.next}
                    onClick={() => setPage(page + 1)}
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
            {report && (
              <form
                className="card"
                onSubmit={async (e) => {
                  e.preventDefault();
                  try {
                    await api(`/assessments/${report}/report/`, {
                      method: "POST",
                      body: JSON.stringify({ reason }),
                    });
                    setMessage("Your report was saved for review.");
                    setReport("");
                    setReason("");
                  } catch (err) {
                    setError((err as Error).message);
                  }
                }}
              >
                <label>
                  What should we review?
                  <textarea
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    required
                    maxLength={1000}
                  />
                </label>
                <button>Send report</button>
                <button
                  type="button"
                  className="secondary"
                  onClick={() => setReport("")}
                >
                  Cancel
                </button>
              </form>
            )}
          </section>
        </>
      )}
    </>
  );
}
