import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "./api";
export type Profile = {
  id: string;
  display_name: string;
  level: string;
  goals: string[];
  pronunciation_model: string;
  daily_minutes: number;
};
export function Account() {
  const [profile, setProfile] = useState<Profile | null>(null),
    [mode, setMode] = useState("login"),
    [error, setError] = useState(""),
    [message, setMessage] = useState(""),
    [busy, setBusy] = useState(false);
  useEffect(() => {
    api("/auth/csrf/")
      .then(() => api<Profile>("/learners/me/"))
      .then(setProfile)
      .catch(() => {});
  }, []);
  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setMessage("");
    setBusy(true);
    const d = Object.fromEntries(new FormData(e.currentTarget));
    try {
      if (profile) {
        const p = await api<Profile>("/learners/me/", {
          method: "PATCH",
          body: JSON.stringify({
            ...d,
            daily_minutes: Number(d.daily_minutes),
            goals: [d.goal],
          }),
        });
        setProfile(p);
        setMessage("Preferences saved.");
      } else if (mode === "reset") {
        await api("/auth/password-reset/", {
          method: "POST",
          body: JSON.stringify(d),
        });
        setMessage("If the account exists, reset instructions have been sent.");
      } else if (mode === "confirm") {
        await api("/auth/password-reset/confirm/", {
          method: "POST",
          body: JSON.stringify(d),
        });
        setMode("login");
        setMessage("Password updated. Sign in to continue.");
      } else {
        await api("/auth/csrf/");
        const p = await api<Profile>(
          `/auth/${mode === "register" ? "register" : "login"}/`,
          {
            method: "POST",
            body: JSON.stringify({ ...d, eligible: d.eligible === "on" }),
          },
        );
        setProfile(p);
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <p className="eyebrow">YOUR LEARNING, YOUR WAY</p>
      <h1>
        {profile
          ? `Welcome, ${profile.display_name}.`
          : "Make room for your voice."}
      </h1>
      <div className="card">
        {error && (
          <p role="alert" className="error">
            {error}
          </p>
        )}
        {message && (
          <p role="status" className="success">
            {message}
          </p>
        )}
        <p>
          <Link to="/placement">
            Find a starting level with a short placement
          </Link>
        </p>
        <form onSubmit={submit}>
          {profile ? (
            <>
              <label>
                Display name
                <input
                  name="display_name"
                  defaultValue={profile.display_name}
                  required
                  maxLength={80}
                />
              </label>
              <label>
                Starting level
                <select name="level" defaultValue={profile.level}>
                  {["pre-A1", "A1", "A2", "B1"].map((v) => (
                    <option key={v}>{v}</option>
                  ))}
                </select>
              </label>
              <label>
                Learning goal
                <select
                  name="goal"
                  defaultValue={profile.goals[0] || "daily-life"}
                >
                  {[
                    "daily-life",
                    "pronunciation",
                    "diction",
                    "grammar",
                    "interviews",
                    "work",
                    "public-speaking",
                    "listening",
                  ].map((v) => (
                    <option key={v}>{v}</option>
                  ))}
                </select>
              </label>
              <label>
                Daily practice (minutes)
                <input
                  name="daily_minutes"
                  type="number"
                  min={5}
                  max={120}
                  defaultValue={profile.daily_minutes}
                />
              </label>
              <label>
                Pronunciation target
                <select
                  name="pronunciation_model"
                  defaultValue={profile.pronunciation_model}
                >
                  {["none", "British", "American"].map((v) => (
                    <option key={v}>{v}</option>
                  ))}
                </select>
              </label>
            </>
          ) : (
            <>
              {["login", "register"].includes(mode) && (
                <label>
                  Username
                  <input
                    name="username"
                    required
                    autoComplete="username"
                    maxLength={150}
                  />
                </label>
              )}
              {["register", "reset"].includes(mode) && (
                <label>
                  Email
                  <input
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                  />
                </label>
              )}
              {mode !== "reset" && (
                <label>
                  Password
                  <input
                    name="password"
                    type="password"
                    autoComplete={
                      mode === "login" ? "current-password" : "new-password"
                    }
                    minLength={mode === "login" ? 1 : 8}
                    required
                  />
                </label>
              )}
              {mode === "confirm" && (
                <>
                  <label>
                    Reset user code
                    <input name="uid" required />
                  </label>
                  <label>
                    Reset token
                    <input name="token" required />
                  </label>
                </>
              )}
              {mode === "register" && (
                <>
                  <label>
                    Display name
                    <input name="display_name" required maxLength={80} />
                  </label>
                  <label className="row">
                    <input
                      style={{ width: "auto" }}
                      name="eligible"
                      type="checkbox"
                      required
                    />
                    I am 16 or older. This pilot is not designed for children.
                  </label>
                </>
              )}
            </>
          )}
          <button disabled={busy}>
            {busy
              ? "Saving…"
              : profile
                ? "Save preferences"
                : mode === "register"
                  ? "Create account"
                  : mode === "reset"
                    ? "Send reset instructions"
                    : mode === "confirm"
                      ? "Change password"
                      : "Sign in"}
          </button>
        </form>
        <div className="row" style={{ marginTop: 24 }}>
          {profile ? (
            <button
              className="secondary"
              onClick={async () => {
                try {
                  await api("/auth/logout/", { method: "POST" });
                  setProfile(null);
                } catch (e) {
                  setError((e as Error).message);
                }
              }}
            >
              Sign out
            </button>
          ) : (
            ["login", "register", "reset", "confirm"].map((v) => (
              <button
                key={v}
                className="secondary"
                onClick={() => {
                  setMode(v);
                  setError("");
                }}
              >
                {v === "login"
                  ? "Sign in"
                  : v === "register"
                    ? "Create account"
                    : v === "reset"
                      ? "Forgot password"
                      : "Use reset code"}
              </button>
            ))
          )}
        </div>
        <p className="small">
          Audio is optional. Recordings require separate consent. Pilot accounts
          are for learners aged 16 and over.
        </p>
      </div>
    </>
  );
}
