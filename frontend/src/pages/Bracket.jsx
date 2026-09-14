import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getBracket, listDivisions } from "../api/client";

export default function Bracket() {
  const { divisionId } = useParams();
  const [bracket, setBracket] = useState(null);
  const [division, setDivision] = useState(null);

  useEffect(() => {
    getBracket(divisionId).then(setBracket);
    listDivisions().then((divs) => setDivision(divs.find((d) => d.id === divisionId)));
  }, [divisionId]);

  if (!bracket || !division) return <p className="muted">Loading…</p>;

  return (
    <div className="stack">
      <Link to="/" className="back-link">
        ← Back
      </Link>

      <div className="card">
        <h2>{division.name}</h2>
        <div className="muted small">Mat {division.mat}</div>
      </div>

      <div className="card">
        <h3>Pool standings</h3>
        <table className="pool-table">
          <thead>
            <tr>
              <th>Competitor</th>
              <th>Wins</th>
              <th>Losses</th>
            </tr>
          </thead>
          <tbody>
            {bracket.pool
              .slice()
              .sort((a, b) => b.wins - a.wins)
              .map((row) => (
                <tr key={row.competitor}>
                  <td>{row.competitor}</td>
                  <td>{row.wins}</td>
                  <td>{row.losses}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Elimination bracket</h3>
        <div className="bracket-rounds">
          {bracket.elimination.map((round) => (
            <div key={round.round} className="bracket-round">
              <h4>{round.round}</h4>
              {round.matches.map((m, i) => (
                <div key={i} className="bracket-match">
                  <div className={m.winner === m.a ? "bracket-winner" : ""}>{m.a}</div>
                  <div className={m.winner === m.b ? "bracket-winner" : ""}>{m.b}</div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
