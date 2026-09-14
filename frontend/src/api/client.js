// Centralized mock backend.
//
// Every network call the UI makes goes through the functions exported here.
// Right now they just read/write an in-memory store and resolve after a
// short delay, to feel like real network calls. When a real backend exists,
// only this file needs to change to real `fetch` calls — no UI code should
// talk to a server directly.

const LATENCY_MS = 150;

function delay(value) {
  return new Promise((resolve) => setTimeout(() => resolve(value), LATENCY_MS));
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function makeId(prefix) {
  return `${prefix}-${Math.random().toString(36).slice(2, 9)}`;
}

// ---- Seed data -------------------------------------------------------

const db = {
  divisions: [
    {
      id: "div-kumite-1",
      name: "Cadet Male -63kg Kumite",
      discipline: "kumite",
      ageGroup: "Cadet",
      weightClass: "-63kg",
      gender: "Male",
      mat: 1,
    },
    {
      id: "div-kata-1",
      name: "Junior Female Kata",
      discipline: "kata",
      ageGroup: "Junior",
      weightClass: null,
      gender: "Female",
      mat: 2,
    },
  ],

  kumiteMatches: [
    {
      id: "km-1",
      divisionId: "div-kumite-1",
      mat: 1,
      round: "Pool - Match 3",
      aka: { name: "Yuki Tanaka" },
      ao: { name: "Marco Rossi" },
      pointsAka: 0,
      pointsAo: 0,
      penaltiesAka: { c1: 0, c2: 0 },
      penaltiesAo: { c1: 0, c2: 0 },
      senshu: null, // "aka" | "ao" | null
      clockSeconds: 120,
      clockRunning: false,
      status: "in_progress", // in_progress | ended
      winner: null, // "aka" | "ao" | null
      endReason: null, // "points" | "time" | "hantei" | "disqualification" | null
      log: [],
    },
  ],

  kataPerformances: [
    {
      id: "kt-1",
      divisionId: "div-kata-1",
      mat: 2,
      round: "Pool - Performance 2",
      competitor: { name: "Aiko Sato" },
      judgeScores: [null, null, null, null, null, null, null],
      finalScore: null,
      status: "scoring", // scoring | scored
    },
  ],

  // Pool standings + elimination bracket, pre-populated with a few
  // already-decided results so the bracket view has something to show.
  bracket: {
    "div-kumite-1": {
      pool: [
        { competitor: "Yuki Tanaka", wins: 2, losses: 0 },
        { competitor: "Marco Rossi", wins: 1, losses: 1 },
        { competitor: "Ben Carter", wins: 0, losses: 2 },
      ],
      elimination: [
        {
          round: "Semifinal",
          matches: [
            { a: "Yuki Tanaka", b: "Ben Carter", winner: "Yuki Tanaka" },
            { a: "Marco Rossi", b: "TBD", winner: null },
          ],
        },
        {
          round: "Final",
          matches: [{ a: "Yuki Tanaka", b: "TBD", winner: null }],
        },
      ],
    },
    "div-kata-1": {
      pool: [
        { competitor: "Aiko Sato", wins: 0, losses: 0 },
        { competitor: "Lena Novak", wins: 0, losses: 0 },
      ],
      elimination: [
        {
          round: "Final",
          matches: [{ a: "Aiko Sato", b: "Lena Novak", winner: null }],
        },
      ],
    },
  },
};

// ---- Divisions ---------------------------------------------------------

export function listDivisions() {
  return delay(clone(db.divisions));
}

// ---- Kumite --------------------------------------------------------------

export function getKumiteMatch(matchId) {
  const match = db.kumiteMatches.find((m) => m.id === matchId);
  return delay(match ? clone(match) : null);
}

export function listKumiteMatches() {
  return delay(clone(db.kumiteMatches));
}

function pushLog(match, text) {
  match.log = [{ id: makeId("log"), text }, ...match.log].slice(0, 20);
}

function checkKumiteEndConditions(match) {
  const gap = Math.abs(match.pointsAka - match.pointsAo);
  if (gap >= 8) {
    match.status = "ended";
    match.endReason = "points";
    match.winner = match.pointsAka > match.pointsAo ? "aka" : "ao";
    match.clockRunning = false;
    pushLog(match, `Match ends — 8-point gap. Winner: ${match.winner.toUpperCase()}`);
    return;
  }
  if (match.penaltiesAka.c1 >= 4) {
    match.status = "ended";
    match.endReason = "disqualification";
    match.winner = "ao";
    match.clockRunning = false;
    pushLog(match, "AKA disqualified (4th category 1 penalty). Winner: AO");
    return;
  }
  if (match.penaltiesAo.c1 >= 4) {
    match.status = "ended";
    match.endReason = "disqualification";
    match.winner = "aka";
    match.clockRunning = false;
    pushLog(match, "AO disqualified (4th category 1 penalty). Winner: AKA");
  }
}

export function awardKumitePoint(matchId, side, points) {
  const match = db.kumiteMatches.find((m) => m.id === matchId);
  if (!match || match.status === "ended") return delay(match ? clone(match) : null);

  if (side === "aka") match.pointsAka += points;
  else match.pointsAo += points;

  if (!match.senshu) {
    match.senshu = side;
    pushLog(match, `Senshu awarded to ${side.toUpperCase()}`);
  }

  pushLog(match, `${side.toUpperCase()} scores ${points} point${points > 1 ? "s" : ""}`);
  checkKumiteEndConditions(match);
  return delay(clone(match));
}

export function awardKumitePenalty(matchId, side, category) {
  const match = db.kumiteMatches.find((m) => m.id === matchId);
  if (!match || match.status === "ended") return delay(match ? clone(match) : null);

  const penalties = side === "aka" ? match.penaltiesAka : match.penaltiesAo;
  penalties[category] += 1;
  pushLog(match, `${side.toUpperCase()} receives ${category.toUpperCase()} penalty (${penalties[category]})`);
  checkKumiteEndConditions(match);
  return delay(clone(match));
}

export function setKumiteClock(matchId, { running, seconds }) {
  const match = db.kumiteMatches.find((m) => m.id === matchId);
  if (!match) return delay(null);
  if (typeof running === "boolean") match.clockRunning = running;
  if (typeof seconds === "number") match.clockSeconds = seconds;

  if (match.clockSeconds <= 0 && match.status !== "ended") {
    match.clockSeconds = 0;
    match.clockRunning = false;
    if (match.pointsAka !== match.pointsAo) {
      match.status = "ended";
      match.endReason = "time";
      match.winner = match.pointsAka > match.pointsAo ? "aka" : "ao";
      pushLog(match, `Time. Winner: ${match.winner.toUpperCase()}`);
    } else {
      pushLog(match, "Time. Scores level — awaiting Hantei decision.");
    }
  }
  return delay(clone(match));
}

export function recordHantei(matchId, side) {
  const match = db.kumiteMatches.find((m) => m.id === matchId);
  if (!match) return delay(null);
  match.status = "ended";
  match.endReason = "hantei";
  match.winner = side;
  pushLog(match, `Hantei decision: ${side.toUpperCase()} wins`);
  return delay(clone(match));
}

// ---- Kata ----------------------------------------------------------------

export function getKataPerformance(performanceId) {
  const performance = db.kataPerformances.find((p) => p.id === performanceId);
  return delay(performance ? clone(performance) : null);
}

export function listKataPerformances() {
  return delay(clone(db.kataPerformances));
}

export function submitKataJudgeScore(performanceId, judgeIndex, score) {
  const performance = db.kataPerformances.find((p) => p.id === performanceId);
  if (!performance) return delay(null);
  performance.judgeScores[judgeIndex] = score;

  const allIn = performance.judgeScores.every((s) => s !== null);
  if (allIn) {
    const sorted = [...performance.judgeScores].sort((a, b) => a - b);
    const trimmed = sorted.slice(1, sorted.length - 1);
    const sum = trimmed.reduce((a, b) => a + b, 0);
    performance.finalScore = Number((sum / trimmed.length).toFixed(2));
    performance.status = "scored";
  }
  return delay(clone(performance));
}

export function resetKataScores(performanceId) {
  const performance = db.kataPerformances.find((p) => p.id === performanceId);
  if (!performance) return delay(null);
  performance.judgeScores = performance.judgeScores.map(() => null);
  performance.finalScore = null;
  performance.status = "scoring";
  return delay(clone(performance));
}

// ---- Bracket ---------------------------------------------------------

export function getBracket(divisionId) {
  return delay(clone(db.bracket[divisionId] ?? null));
}

// ---- Public display -----------------------------------------------------

export function getPublicBoard() {
  const kumite = db.kumiteMatches.map((m) => ({
    id: m.id,
    mat: m.mat,
    round: m.round,
    aka: m.aka.name,
    ao: m.ao.name,
    pointsAka: m.pointsAka,
    pointsAo: m.pointsAo,
    clockSeconds: m.clockSeconds,
    status: m.status,
    winner: m.winner,
  }));
  const kata = db.kataPerformances.map((p) => ({
    id: p.id,
    mat: p.mat,
    round: p.round,
    competitor: p.competitor.name,
    finalScore: p.finalScore,
    status: p.status,
  }));
  return delay({ kumite: clone(kumite), kata: clone(kata) });
}
