import { useState } from "react";
import { api } from "./api";
export function PrivacyControls() {
  const [message, setMessage] = useState(""),
    [error, setError] = useState("");
  return (
    <section className="card" style={{ marginTop: 24 }}>
      <h2>Your data, your choice.</h2>
      <p>
        Audio preview stays on your device until submitted. Processing audio
        expires within ten minutes and is deleted after processing. Session
        answers and transcripts expire after 90 days of session inactivity.
        Account deletion removes active learner records; deployment backups
        follow the operator’s published retention policy.
      </p>
      {message && (
        <p role="status" className="success">
          {message}
        </p>
      )}
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
      <div className="row">
        <button
          className="secondary"
          onClick={async () => {
            try {
              await api("/learners/me/consent/", {
                method: "POST",
                body: JSON.stringify({ granted: false }),
              });
              setMessage(
                "Audio consent withdrawn. Pending recordings have been deleted.",
              );
            } catch (e) {
              setError((e as Error).message);
            }
          }}
        >
          Withdraw audio consent
        </button>
        <button
          className="secondary"
          onClick={async () => {
            try {
              const data = await api("/learners/me/data/");
              const url = URL.createObjectURL(
                new Blob([JSON.stringify(data, null, 2)], {
                  type: "application/json",
                }),
              );
              const a = document.createElement("a");
              a.href = url;
              a.download = "speakwise-my-data.json";
              a.click();
              setTimeout(() => URL.revokeObjectURL(url), 1000);
              setMessage("Your export was downloaded. Keep it private.");
            } catch (e) {
              setError((e as Error).message);
            }
          }}
        >
          Download my data
        </button>
      </div>
      <details>
        <summary>Delete my account and learning records</summary>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(e.currentTarget));
            try {
              await api("/learners/me/data/", {
                method: "DELETE",
                body: JSON.stringify(data),
              });
              window.location.assign("/");
            } catch (err) {
              setError((err as Error).message);
            }
          }}
        >
          <p>
            This permanently deletes your active account, progress, answers,
            transcripts, and processing audio.
          </p>
          <label>
            Current password
            <input
              name="password"
              type="password"
              autoComplete="current-password"
              required
            />
          </label>
          <label>
            Type DELETE to confirm
            <input name="confirmation" required pattern="DELETE" />
          </label>
          <button>Delete my account</button>
        </form>
      </details>
    </section>
  );
}
