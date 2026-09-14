import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listDivisions, listKumiteMatches, listKataPerformances } from "../api/client";

export default function Home() {
  const [divisions, setDivisions] = useState([]);
  const [kumiteMatches, setKumiteMatches] = useState([]);
  const [kataPerformances, setKataPerformances] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listDivisions(), listKumiteMatches(), listKataPerformances()]).then(
      ([divs, km, kt]) => {
        setDivisions(divs);
        setKumiteMatches(km);
        setKataPerformances(kt);
        setLoading(false);
      }
    );
  }, []);

  if (loading) return <p className="muted">Loading…</p>;

  return (
    <div className="stack">
      <section className="card">
        <h2>Divisions</h2>
        <ul className="list">
          {divisions.map((d) => (
            <li key={d.id} className="list-row">
              <div>
                <strong>{d.name}</strong>
                <div className="muted small">
                  Mat {d.mat} · {d.discipline === "kumite" ? "Kumite" : "Kata"}
                </div>
              </div>
              <Link className="btn" to={`/bracket/${d.id}`}>
                View bracket
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Live Kumite matches</h2>
        <ul className="list">
          {kumiteMatches.map((m) => (
            <li key={m.id} className="list-row">
              <div>
                <strong>
                  {m.aka.name} vs {m.ao.name}
                </strong>
                <div className="muted small">
                  Mat {m.mat} · {m.round}
                </div>
              </div>
              <Link className="btn btn-primary" to={`/kumite/${m.id}`}>
                Score match
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Live Kata performances</h2>
        <ul className="list">
          {kataPerformances.map((p) => (
            <li key={p.id} className="list-row">
              <div>
                <strong>{p.competitor.name}</strong>
                <div className="muted small">
                  Mat {p.mat} · {p.round}
                </div>
              </div>
              <Link className="btn btn-primary" to={`/kata/${p.id}`}>
                Score performance
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Public display</h2>
        <p className="muted small">
          Open this on a second screen for spectators and coaches — read-only,
          updates as officials score.
        </p>
        <Link className="btn" to="/display" target="_blank" rel="noreferrer">
          Open public display ↗
        </Link>
      </section>
    </div>
  );
}
