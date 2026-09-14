# Karate Tournament Scoreboard — Scope (v1)

## Overview
A scoreboard and tournament management tool for karate competitions, covering both Kumite (sparring) and Kata (forms), used by officials to score matches in real time and by spectators/coaches to follow live results.

## Scope decisions

### Sport
- Karate — both **Kumite** (sparring) and **Kata** (forms).

### Users
- **Scorekeeper/official**: inputs scores and manages matches.
- **Spectators/coaches**: view-only, via a public-facing display.

### Kumite scoring
- Implements the **full WKF competition ruleset**:
  - 1/2/3-point strikes
  - Category 1 and Category 2 (C1/C2) penalties
  - Senshu (priority point)
  - Hantei (judge decision at time/point limit)
- Points are awarded by a **single scorekeeper/referee**, entered in **real time** as strikes land.
- No multi-judge majority-vote logic — the scorekeeper's call is final.

### Kata scoring
- Fixed at **7 judges**.
- The tool **auto-calculates the final score**: drops the highest and lowest scores, then averages the remaining 5.

### Tournament structure
- **Pool play** followed by a **single-elimination bracket**.

### Multi-mat support
- Supports **multiple mats/courts** running matches **simultaneously**, with scheduling across them.

### Divisions
- Competitors are grouped into brackets by:
  - Age group
  - Weight class
  - Gender

### Public-facing display
- A live-updating view of scores and brackets for spectators and coaches, separate from the official's input screen.

## v1 summary flow
1. Competitors are registered and assigned to divisions (age group, weight class, gender).
2. Pool play matches are scheduled across multiple mats.
3. For each Kumite match, the scorekeeper enters points/penalties in real time under full WKF rules; senshu/hantei resolve ties.
4. For each Kata performance, 7 judges' scores are entered and the tool auto-calculates the final score (drop high/low, average).
5. Pool results feed into a single-elimination bracket.
6. A public-facing display shows live scores and bracket progress throughout.

## Open / next steps (not yet scoped)
- Data model for competitors, divisions, pools, brackets, mats, and matches.
- UI/UX for real-time point entry (Kumite) and multi-judge score entry (Kata).
- Tie-breaking and seeding rules for pool-to-bracket advancement.
- Device/hardware assumptions for the scorekeeper's input screen and the public display.
- Authentication/access control for officials vs. public display.
