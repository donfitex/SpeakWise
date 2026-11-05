type Cues = {
  target?: string;
  syllables?: { text: string; stress: boolean }[];
  tip?: string;
  mouth?: string;
  intonation?: string;
  pause_after?: string;
  review_status?: string;
};
export function PronunciationCues({ cues }: { cues: Cues }) {
  if (!cues.target) return null;
  return (
    <section
      aria-label="Pronunciation practice cues"
      className="note"
      style={{ display: "block" }}
    >
      <h3>{cues.target}</h3>
      {cues.review_status === "illustrative-unreviewed" && (
        <p className="small">
          Illustrative pilot cue · educator review pending. This is a practice
          aid, not a diagnosis.
        </p>
      )}
      {!!cues.syllables?.length && (
        <>
          <p
            className="row"
            aria-label={
              "Syllables: " +
              cues.syllables
                .map((s) => s.text + (s.stress ? " (stressed)" : ""))
                .join(", ")
            }
          >
            {cues.syllables.map((s, i) => (
              <span
                key={i}
                className="pill"
                style={{
                  background: s.stress ? "#dbe89d" : "white",
                  fontWeight: s.stress ? 800 : 400,
                }}
              >
                {s.stress ? "ˈ" : ""}
                {s.text}
              </span>
            ))}
          </p>
          <p className="small">
            Highlighted syllable: a little more emphasis, not extra force.
          </p>
        </>
      )}
      {cues.mouth === "closed-lips" && (
        <svg
          role="img"
          aria-labelledby="mouth-title mouth-desc"
          viewBox="0 0 220 90"
          width="220"
          height="90"
        >
          <title id="mouth-title">Closed lips for the /m/ sound</title>
          <desc id="mouth-desc">
            A simplified front view: the upper and lower lips meet gently. Hum
            comfortably with your lips closed.
          </desc>
          <path
            d="M25 45 Q65 5 110 30 Q155 5 195 45 Q155 90 110 70 Q65 90 25 45Z"
            fill="#d6b9a4"
            stroke="#173b35"
            strokeWidth="2"
          />
          <path
            d="M25 45 Q65 50 110 43 Q155 50 195 45"
            fill="none"
            stroke="#173b35"
            strokeWidth="3"
          />
        </svg>
      )}
      <p>{cues.tip}</p>
      {cues.pause_after && (
        <p>
          <strong>
            Alex <span aria-label="brief pause">|</span> I am learning English.
          </strong>
        </p>
      )}
      <p>
        <span aria-hidden="true">↘ </span>
        {cues.intonation}
      </p>
    </section>
  );
}
