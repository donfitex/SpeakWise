import { useEffect, useState } from "react";
export function ModelVoice({ text }: { text: string }) {
  const supported =
    typeof window !== "undefined" && "speechSynthesis" in window;
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]),
    [voice, setVoice] = useState(""),
    [rate, setRate] = useState("1"),
    [remote, setRemote] = useState(false),
    [error, setError] = useState(""),
    [speaking, setSpeaking] = useState(false);
  useEffect(() => {
    if (!supported) return;
    const update = () =>
      setVoices(
        window.speechSynthesis
          .getVoices()
          .filter((v) => v.lang.startsWith("en")),
      );
    update();
    window.speechSynthesis.addEventListener("voiceschanged", update);
    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", update);
      window.speechSynthesis.cancel();
    };
  }, [supported]);
  const available = voices.filter((v) => v.localService || remote);
  function play() {
    setError("");
    const selected =
      available.find((v) => v.voiceURI === voice) || available[0];
    if (!selected) {
      setError(
        "No permitted English voice is available. Read the caption instead.",
      );
      return;
    }
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.voice = selected;
    u.lang = selected.lang;
    u.rate = Number(rate);
    u.onend = () => setSpeaking(false);
    u.onerror = () => {
      setSpeaking(false);
      setError("Playback is unavailable. The full caption is below.");
    };
    setSpeaking(true);
    window.speechSynthesis.speak(u);
  }
  return (
    <section aria-label="Model pronunciation">
      <p>
        <strong>Model caption:</strong> {text}
      </p>
      {supported ? (
        <>
          <div className="row">
            <label>
              Voice
              <select value={voice} onChange={(e) => setVoice(e.target.value)}>
                <option value="">First available local voice</option>
                {available.map((v) => (
                  <option key={v.voiceURI} value={v.voiceURI}>
                    {v.name} ({v.lang}){v.localService ? "" : " · online"}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Speed
              <select value={rate} onChange={(e) => setRate(e.target.value)}>
                <option value="1">Normal</option>
                <option value="0.75">Slow</option>
              </select>
            </label>
            <button type="button" className="secondary" onClick={play}>
              Listen to model
            </button>
            {speaking && (
              <button
                type="button"
                className="secondary"
                onClick={() => {
                  window.speechSynthesis.cancel();
                  setSpeaking(false);
                }}
              >
                Stop playback
              </button>
            )}
          </div>
          <details>
            <summary>Online voice permission</summary>
            <p className="small">
              Local voices are preferred. Online voices may send this model
              phrase to your browser vendor. No learner recording is sent by
              this control.
            </p>
            <label className="row">
              <input
                style={{ width: "auto" }}
                type="checkbox"
                checked={remote}
                onChange={(e) => setRemote(e.target.checked)}
              />
              Allow online browser voices for this model.
            </label>
          </details>
        </>
      ) : (
        <p className="small">
          Model speech is unsupported in this browser. Use the caption.
        </p>
      )}
      {error && <p role="status">{error}</p>}
    </section>
  );
}
