import { useEffect, useRef, useState } from "react";
import { api } from "./api";
const MAX_SECONDS = 30;
export function Recorder({
  onSubmit,
}: {
  onSubmit?: (blob: Blob) => Promise<void>;
}) {
  const [state, setState] = useState<
      "idle" | "requesting" | "recording" | "review" | "sending"
    >("idle"),
    [error, setError] = useState(""),
    [url, setUrl] = useState(""),
    [consent, setConsent] = useState(false),
    [seconds, setSeconds] = useState(0),
    [devices, setDevices] = useState<MediaDeviceInfo[]>([]),
    [device, setDevice] = useState("");
  const recorder = useRef<MediaRecorder | null>(null),
    stream = useRef<MediaStream | null>(null),
    blob = useRef<Blob | null>(null),
    timer = useRef<ReturnType<typeof setInterval> | null>(null),
    mounted = useRef(true),
    objectUrl = useRef(""),
    cancelled = useRef(false);
  function cleanup() {
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = null;
    }
    stream.current?.getTracks().forEach((t) => t.stop());
    stream.current = null;
  }
  function revoke() {
    if (objectUrl.current) URL.revokeObjectURL(objectUrl.current);
    objectUrl.current = "";
  }
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      cancelled.current = true;
      if (recorder.current?.state === "recording") recorder.current.stop();
      cleanup();
      revoke();
    };
  }, []);
  const supported =
    typeof MediaRecorder !== "undefined" &&
    !!navigator.mediaDevices?.getUserMedia;
  async function start() {
    if (!consent) return;
    setError("");
    setState("requesting");
    cancelled.current = false;
    try {
      await api("/learners/me/consent/", {
        method: "POST",
        body: JSON.stringify({ granted: true }),
      });
      const media = await navigator.mediaDevices.getUserMedia({
        audio: device ? { deviceId: { exact: device } } : true,
      });
      if (!mounted.current || cancelled.current) {
        media.getTracks().forEach((t) => t.stop());
        return;
      }
      stream.current = media;
      setDevices(
        (await navigator.mediaDevices.enumerateDevices()).filter(
          (d) => d.kind === "audioinput",
        ),
      );
      const type = [
        "audio/webm;codecs=opus",
        "audio/ogg;codecs=opus",
        "audio/mp4",
      ].find((t) => MediaRecorder.isTypeSupported(t));
      const r = new MediaRecorder(media, type ? { mimeType: type } : undefined);
      recorder.current = r;
      const chunks: BlobPart[] = [];
      r.ondataavailable = (e) => {
        if (e.data.size) chunks.push(e.data);
      };
      r.onerror = () => {
        cleanup();
        if (mounted.current) {
          setError("Recording failed. Please retry or type your answer.");
          setState("idle");
        }
      };
      r.onstop = () => {
        cleanup();
        if (!mounted.current || cancelled.current) return;
        const recorded = new Blob(chunks, { type: r.mimeType });
        if (!recorded.size) {
          setError("No audio was captured. Try again or type your answer.");
          setState("idle");
          return;
        }
        blob.current = recorded;
        revoke();
        objectUrl.current = URL.createObjectURL(recorded);
        setUrl(objectUrl.current);
        setState("review");
      };
      r.start();
      setSeconds(0);
      setState("recording");
      const began = Date.now();
      timer.current = setInterval(() => {
        const elapsed = Math.floor((Date.now() - began) / 1000);
        setSeconds(Math.min(elapsed, MAX_SECONDS));
        if (elapsed >= MAX_SECONDS && r.state === "recording") r.stop();
      }, 250);
    } catch (e) {
      cleanup();
      if (mounted.current) {
        setState("idle");
        setError(
          e instanceof DOMException && e.name === "NotAllowedError"
            ? "Microphone permission was denied. Enable it in browser settings or use the typed answer."
            : e instanceof DOMException && e.name === "NotFoundError"
              ? "No microphone was found. Connect one or use the typed answer."
              : (e as Error).message,
        );
      }
    }
  }
  function discard() {
    cancelled.current = true;
    if (recorder.current?.state === "recording") recorder.current.stop();
    cleanup();
    revoke();
    blob.current = null;
    setUrl("");
    setState("idle");
    setError("");
  }
  async function send() {
    if (!blob.current || !onSubmit) return;
    setState("sending");
    setError("");
    try {
      await onSubmit(blob.current);
      discard();
    } catch (e) {
      setError((e as Error).message);
      setState("review");
    }
  }
  return (
    <section aria-label="Optional microphone practice" className="stack">
      <h3>Prefer to speak?</h3>
      <p className="small">
        Record up to 30 seconds. Preview stays on this device until you choose
        to submit. Processing audio is deleted after evaluation; raw recordings
        are not retained for history. You can always type instead.
      </p>
      {!supported ? (
        <p role="status">
          Recording is unavailable in this browser. Use the typed answer.
        </p>
      ) : (
        <>
          <label className="row">
            <input
              type="checkbox"
              style={{ width: "auto", margin: 0 }}
              checked={consent}
              disabled={state !== "idle"}
              onChange={(e) => setConsent(e.target.checked)}
            />
            I consent to microphone capture and optional processing (audio
            policy v1).
          </label>
          {devices.length > 1 && (
            <label>
              Microphone
              <select
                value={device}
                disabled={state !== "idle"}
                onChange={(e) => setDevice(e.target.value)}
              >
                <option value="">Default device</option>
                {devices.map((d) => (
                  <option key={d.deviceId} value={d.deviceId}>
                    {d.label || "Microphone"}
                  </option>
                ))}
              </select>
            </label>
          )}
          <div className="row">
            {state === "idle" && (
              <button
                className="secondary"
                type="button"
                onClick={start}
                disabled={!consent}
              >
                Start recording
              </button>
            )}
            {state === "requesting" && (
              <>
                <p role="status">Waiting for microphone permission…</p>
                <button type="button" onClick={discard}>
                  Cancel
                </button>
              </>
            )}
            {state === "recording" && (
              <>
                <p role="status">
                  ● Recording · {seconds}/{MAX_SECONDS}s
                </p>
                <button type="button" onClick={() => recorder.current?.stop()}>
                  Stop recording
                </button>
                <button type="button" className="secondary" onClick={discard}>
                  Cancel recording
                </button>
              </>
            )}
            {(state === "review" || state === "sending") && (
              <>
                <audio controls src={url} aria-label="Your recording preview" />
                <button
                  type="button"
                  className="secondary"
                  disabled={state === "sending"}
                  onClick={discard}
                >
                  Discard and retry
                </button>
                {onSubmit && (
                  <button
                    type="button"
                    disabled={state === "sending"}
                    onClick={send}
                  >
                    {state === "sending" ? "Submitting…" : "Submit recording"}
                  </button>
                )}
              </>
            )}
          </div>
        </>
      )}
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
    </section>
  );
}
