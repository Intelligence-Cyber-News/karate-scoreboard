import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getKataPerformance, submitKataJudgeScore, resetKataScores } from "../api/client";

export default function KataMatch() {
  const { id } = useParams();
  const [performance, setPerformance] = useState(null);
  const [draftScore, setDraftScore] = useState("");

  useEffect(() => {
    getKataPerformance(id).then(setPerformance);
  }, [id]);

  if (!performance) return <p className="muted">Loading…</p>;

  const nextJudgeIndex = performance.judgeScores.findIndex((s) => s === null);

  const submitScore = () => {
    const value = Number(draftScore);
    if (Number.isNaN(value) || value < 0 || value > 10) return;
    submitKataJudgeScore(id, nextJudgeIndex, value).then((updated) => {
      setPerformance(updated);
      setDraftScore("");
    });
  };

  const reset = () => resetKataScores(id).then(setPerformance);

  const sorted = performance.judgeScores.filter((s) => s !== null).slice().sort((a, b) => a - b);
  const isComplete = performance.status === "scored";

  return (
    <div className="stack">
      <Link to="/" className="back-link">
        ← Back
      </Link>

      <div className="card">
        <h2>{performance.competitor.name}</h2>
        <div className="muted small">
          Mat {performance.mat} · {performance.round}
        </div>
      </div>

      <div className="card">
        <h3>Judge scores (7 judges, 0–10)</h3>
        <div className="judge-grid">
          {performance.judgeScores.map((score, index) => (
            <div
              key={index}
              className={`judge-cell ${score === null ? "judge-pending" : "judge-filled"} ${
                index === nextJudgeIndex ? "judge-current" : ""
              }`}
            >
              <div className="muted small">Judge {index + 1}</div>
              <div className="judge-score">{score === null ? "—" : score.toFixed(1)}</div>
            </div>
          ))}
        </div>

        {!isComplete && (
          <div className="judge-input-row">
            <input
              type="number"
              min="0"
              max="10"
              step="0.1"
              value={draftScore}
              placeholder={`Score for judge ${nextJudgeIndex + 1}`}
              onChange={(e) => setDraftScore(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && submitScore()}
            />
            <button className="btn btn-primary" onClick={submitScore}>
              Submit
            </button>
          </div>
        )}

        {isComplete && (
          <div className="banner banner-success">
            <div>
              Dropped highest ({Math.max(...performance.judgeScores).toFixed(1)}) and lowest (
              {Math.min(...performance.judgeScores).toFixed(1)}), averaged the rest:{" "}
              {sorted.slice(1, -1).map((s) => s.toFixed(1)).join(", ")}
            </div>
            <div className="final-score">Final score: {performance.finalScore.toFixed(2)}</div>
          </div>
        )}

        <button className="btn" onClick={reset} style={{ marginTop: "1rem" }}>
          Reset scores
        </button>
      </div>
    </div>
  );
}
