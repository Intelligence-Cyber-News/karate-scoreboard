// Backend client.
//
// Every network call the UI makes goes through the functions exported here.
// This talks to the real FastAPI backend (see backend/app). No UI code
// should call `fetch` directly — everything goes through this file, so a
// future change to the backend only needs updating here.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request to ${path} failed with ${response.status}`);
  }

  return response.json();
}

// ---- Divisions -------------------------------------------------------

export function listDivisions() {
  return request("/divisions");
}

// ---- Kumite --------------------------------------------------------------

export function getKumiteMatch(matchId) {
  return request(`/kumite-matches/${matchId}`);
}

export function listKumiteMatches() {
  return request("/kumite-matches");
}

export function awardKumitePoint(matchId, side, points) {
  return request(`/kumite-matches/${matchId}/points`, {
    method: "POST",
    body: JSON.stringify({ side, points }),
  });
}

export function awardKumitePenalty(matchId, side, category) {
  return request(`/kumite-matches/${matchId}/penalties`, {
    method: "POST",
    body: JSON.stringify({ side, category }),
  });
}

export function setKumiteClock(matchId, { running, seconds }) {
  const body = {};
  if (typeof running === "boolean") body.running = running;
  if (typeof seconds === "number") body.seconds = seconds;
  return request(`/kumite-matches/${matchId}/clock`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function recordHantei(matchId, side) {
  return request(`/kumite-matches/${matchId}/hantei`, {
    method: "POST",
    body: JSON.stringify({ side }),
  });
}

// ---- Kata ----------------------------------------------------------------

export function getKataPerformance(performanceId) {
  return request(`/kata-performances/${performanceId}`);
}

export function listKataPerformances() {
  return request("/kata-performances");
}

export function submitKataJudgeScore(performanceId, judgeIndex, score) {
  return request(`/kata-performances/${performanceId}/scores`, {
    method: "POST",
    body: JSON.stringify({ judgeIndex, score }),
  });
}

export function resetKataScores(performanceId) {
  return request(`/kata-performances/${performanceId}/reset`, {
    method: "POST",
  });
}

// ---- Bracket ---------------------------------------------------------

export function getBracket(divisionId) {
  return request(`/divisions/${divisionId}/bracket`);
}

// ---- Public display -----------------------------------------------------

export function getPublicBoard() {
  return request("/public-board");
}
