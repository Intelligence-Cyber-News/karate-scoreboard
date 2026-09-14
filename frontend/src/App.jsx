import { Routes, Route, Link, useLocation } from "react-router-dom";
import Home from "./pages/Home";
import KumiteMatch from "./pages/KumiteMatch";
import KataMatch from "./pages/KataMatch";
import Bracket from "./pages/Bracket";
import PublicDisplay from "./pages/PublicDisplay";

function App() {
  const location = useLocation();
  const isDisplay = location.pathname === "/display";

  if (isDisplay) {
    return (
      <Routes>
        <Route path="/display" element={<PublicDisplay />} />
      </Routes>
    );
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/" className="app-title">
          🥋 Karate Scoreboard
        </Link>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/kumite/:id" element={<KumiteMatch />} />
          <Route path="/kata/:id" element={<KataMatch />} />
          <Route path="/bracket/:divisionId" element={<Bracket />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
