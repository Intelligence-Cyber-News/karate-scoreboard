import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  getKumiteMatch,
  awardKumitePoint,
  awardKumitePenalty,
  setKumiteClock,
  recordHantei,
} from "../api/client";

function formatClock(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function KumiteMatch() {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const intervalRef = useRef(null);

  const refresh = useCallback(() => {
    getKumiteMatch(id).then(setMatch);
  }, [id]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  // Local ticking clock, synced to the mock backend once a second.
  useEffect(() => {
    if (!match || !match.clockRunning) {
      clearInterval(intervalRef.current);
      return;
    }
    intervalRef.current = setInterval(() => {
      setKumiteClock(id, { seconds: Math.max(0, match.clockSeconds - 1) }).then(setMatch);
    }, 1000);
    return () => clearInterval(intervalRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [match?.clockRunning, match?.clockSeconds, id]);

  if (!match) return <p className="muted">Loading…</p>;

  const point = (side, points) => awardKumitePoint(id, side, points).then(setMatch);
  const penalty = (side, category) => awardKumitePenalty(id, side, category).then(setMatch);
  const toggleClock = () => setKumiteClock(id, { running: !match.clockRunning }).then(setMatch);
  const resetClock = () => setKumiteClock(id, { running: false, seconds: 120 }).then(setMatch);
  const hantei = (side) => recordHantei(id, side).then(setMatch);

  const needsHantei =
    match.status === "in_progress" &&
    match.clockSeconds === 0 &&
    match.pointsAka === match.pointsAo;

  return (
    <div className="stack">
      <Link to="/" className="back-link">
        ← Back
      </Link>

      <div className="card kumite-header">
        <div>
          <h2>
            {match.aka.name} <span className="muted">vs</span> {match.ao.name}
          </h2>
          <div className="muted small">
            Mat {match.mat} · {match.round}
          </div>
        </div>
        <div className="clock">
          <span className={match.clockRunning ? "clock-running" : ""}>
            {formatClock(match.clockSeconds)}
          </span>
          <div className="clock-controls">
            <button className="btn" onClick={toggleClock} disabled={match.status === "ended"}>
              {match.clockRunning ? "Pause" : "Start"}
            </button>
            <button className="btn" onClick={resetClock} disabled={match.status === "ended"}>
              Reset
            </button>
          </div>
        </div>
      </div>

      {match.status === "ended" && (
        <div className="banner banner-success">
          Match ended ({match.endReason}). Winner:{" "}
          <strong>{match.winner === "aka" ? match.aka.name : match.ao.name}</strong> (
          {match.winner?.toUpperCase()})
        </div>
      )}

      {needsHantei && (
        <div className="banner banner-warning">
          Time — scores level. Referee decision (Hantei) required.
          <div className="hantei-buttons">
            <button className="btn btn-aka" onClick={() => hantei("aka")}>
              AKA wins
            </button>
            <button className="btn btn-ao" onClick={() => hantei("ao")}>
              AO wins
            </button>
          </div>
        </div>
      )}

      <div className="fighters">
        <CompetitorPanel
          side="aka"
          label="AKA (Red)"
          name={match.aka.name}
          points={match.pointsAka}
          penalties={match.penaltiesAka}
          senshu={match.senshu === "aka"}
          disabled={match.status === "ended"}
          onPoint={(pts) => point("aka", pts)}
          onPenalty={(cat) => penalty("aka", cat)}
        />
        <CompetitorPanel
          side="ao"
          label="AO (Blue)"
          name={match.ao.name}
          points={match.pointsAo}
          penalties={match.penaltiesAo}
          senshu={match.senshu === "ao"}
          disabled={match.status === "ended"}
          onPoint={(pts) => point("ao", pts)}
          onPenalty={(cat) => penalty("ao", cat)}
        />
      </div>

      <div className="card">
        <h3>Match log</h3>
        <ul className="log">
          {match.log.length === 0 && <li className="muted small">No events yet.</li>}
          {match.log.map((entry) => (
            <li key={entry.id}>{entry.text}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function CompetitorPanel({ side, label, name, points, penalties, senshu, disabled, onPoint, onPenalty }) {
  return (
    <div className={`card competitor-panel competitor-${side}`}>
      <div className="competitor-heading">
        <h3>{label}</h3>
        {senshu && <span className="senshu-badge">SENSHU</span>}
      </div>
      <div className="competitor-name">{name}</div>
      <div className="score-display">{points}</div>

      <div className="button-row">
        <button className={`btn btn-${side}`} disabled={disabled} onClick={() => onPoint(1)}>
          +1 (Yuko)
        </button>
        <button className={`btn btn-${side}`} disabled={disabled} onClick={() => onPoint(2)}>
          +2 (Waza-ari)
        </button>
        <button className={`btn btn-${side}`} disabled={disabled} onClick={() => onPoint(3)}>
          +3 (Ippon)
        </button>
      </div>

      <div className="button-row">
        <button className="btn btn-penalty" disabled={disabled} onClick={() => onPenalty("c1")}>
          C1 penalty ({penalties.c1})
        </button>
        <button className="btn btn-penalty" disabled={disabled} onClick={() => onPenalty("c2")}>
          C2 penalty ({penalties.c2})
        </button>
      </div>
    </div>
  );
}
