import { useEffect, useState } from "react";
import { getPublicBoard } from "../api/client";

function formatClock(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function PublicDisplay() {
  const [board, setBoard] = useState(null);

  useEffect(() => {
    const load = () => getPublicBoard().then(setBoard);
    load();
    const interval = setInterval(load, 1000);
    return () => clearInterval(interval);
  }, []);

  if (!board) return <p className="muted">Loading…</p>;

  return (
    <div className="display-root">
      <h1 className="display-title">Live Scoreboard</h1>

      <div className="display-grid">
        {board.kumite.map((m) => (
          <div key={m.id} className="display-card">
            <div className="display-mat">Mat {m.mat} · Kumite</div>
            <div className="display-round">{m.round}</div>
            <div className="display-scoreline">
              <div className="display-side display-aka">
                <div className="display-name">{m.aka}</div>
                <div className="display-score">{m.pointsAka}</div>
              </div>
              <div className="display-clock">{formatClock(m.clockSeconds)}</div>
              <div className="display-side display-ao">
                <div className="display-name">{m.ao}</div>
                <div className="display-score">{m.pointsAo}</div>
              </div>
            </div>
            {m.status === "ended" && (
              <div className="display-result">Winner: {m.winner === "aka" ? m.aka : m.ao}</div>
            )}
          </div>
        ))}

        {board.kata.map((p) => (
          <div key={p.id} className="display-card">
            <div className="display-mat">Mat {p.mat} · Kata</div>
            <div className="display-round">{p.round}</div>
            <div className="display-kata-name">{p.competitor}</div>
            <div className="display-score">
              {p.finalScore === null ? "Scoring…" : p.finalScore.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
