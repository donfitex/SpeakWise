import { useEffect, useRef, useState } from "react";
import { Recorder } from "./Recorder";
import { api } from "./api";
type Job = {
  id: string;
  status: string;
  transcript: string;
  result: { feedback?: string; simulated?: boolean; confidence?: string };
};
export function SpeechPractice({ sessionId }: { sessionId: string }) {
  const [job, setJob] = useState<Job | null>(null),
    [error, setError] = useState("");
  const uploadKey = useRef<{ blob: Blob; key: string } | null>(null);
  async function send(blob: Blob) {
    setError("");
    if (uploadKey.current?.blob !== blob)
      uploadKey.current = { blob, key: crypto.randomUUID() };
    const form = new FormData();
    form.append(
      "audio",
      blob,
      blob.type.includes("mp4") ? "recording.m4a" : "recording.webm",
    );
    form.append("request_id", uploadKey.current!.key);
    setJob(
      await api<Job>(`/lesson-sessions/${sessionId}/speech-attempts/`, {
        method: "POST",
        body: form,
      }),
    );
  }
  useEffect(() => {
    if (!job || !["queued", "processing"].includes(job.status)) return;
    let active = true;
    const timer = setInterval(() => {
      api<Job>(`/speech-attempts/${job.id}/status/`)
        .then((data) => {
          if (active) setJob(data);
        })
        .catch((e) => {
          if (active) setError((e as Error).message);
        });
    }, 2000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [job?.id, job?.status]);
  return (
    <>
      <Recorder onSubmit={send} />
      {error && (
        <p role="alert" className="error">
          {error} Use typed practice while we reconnect.
        </p>
      )}
      {job && (
        <div className="note" role="status">
          <div>
            <strong>
              {job.result.simulated
                ? "Simulated test result"
                : job.status === "complete"
                  ? "Transcript ready"
                  : job.status === "failed"
                    ? "Please try again"
                    : job.status === "deleted"
                      ? "Speech data deleted"
                      : "Processing your recording…"}
            </strong>
            {job.transcript && <p>Transcript: {job.transcript}</p>}
            <p>{job.result.feedback}</p>
            {job.result.confidence && (
              <p>Pronunciation confidence: {job.result.confidence}</p>
            )}
            {!["queued", "processing", "deleted"].includes(job.status) && (
              <button
                type="button"
                className="secondary"
                onClick={async () => {
                  try {
                    await api(`/speech-attempts/${job.id}/status/`, {
                      method: "DELETE",
                    });
                    setJob(null);
                  } catch (e) {
                    setError((e as Error).message);
                  }
                }}
              >
                Delete speech result
              </button>
            )}
          </div>
        </div>
      )}
    </>
  );
}
