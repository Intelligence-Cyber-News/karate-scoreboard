from app.models import KumiteMatch, LogEntry
from app.repository import make_log_id


def _push_log(match: KumiteMatch, text: str) -> None:
    match.log.insert(0, LogEntry(id=make_log_id(), text=text))
    match.log = match.log[:20]


def check_end_conditions(match: KumiteMatch) -> None:
    if match.status == "ended":
        return

    gap = abs(match.pointsAka - match.pointsAo)
    if gap >= 8:
        match.status = "ended"
        match.endReason = "points"
        match.winner = "aka" if match.pointsAka > match.pointsAo else "ao"
        match.clockRunning = False
        _push_log(match, f"Match ends — 8-point gap. Winner: {match.winner.upper()}")
        return

    if match.penaltiesAka.c1 >= 4:
        match.status = "ended"
        match.endReason = "disqualification"
        match.winner = "ao"
        match.clockRunning = False
        _push_log(match, "AKA disqualified (4th category 1 penalty). Winner: AO")
        return

    if match.penaltiesAo.c1 >= 4:
        match.status = "ended"
        match.endReason = "disqualification"
        match.winner = "aka"
        match.clockRunning = False
        _push_log(match, "AO disqualified (4th category 1 penalty). Winner: AKA")


def award_point(match: KumiteMatch, side: str, points: int) -> None:
    if match.status == "ended":
        return

    if side == "aka":
        match.pointsAka += points
    else:
        match.pointsAo += points

    if match.senshu is None:
        match.senshu = side
        _push_log(match, f"Senshu awarded to {side.upper()}")

    suffix = "s" if points > 1 else ""
    _push_log(match, f"{side.upper()} scores {points} point{suffix}")
    check_end_conditions(match)


def award_penalty(match: KumiteMatch, side: str, category: str) -> None:
    if match.status == "ended":
        return

    penalties = match.penaltiesAka if side == "aka" else match.penaltiesAo
    if category == "c1":
        penalties.c1 += 1
    else:
        penalties.c2 += 1

    count = penalties.c1 if category == "c1" else penalties.c2
    _push_log(match, f"{side.upper()} receives {category.upper()} penalty ({count})")
    check_end_conditions(match)


def set_clock(match: KumiteMatch, running: bool | None, seconds: int | None) -> None:
    if running is not None:
        match.clockRunning = running
    if seconds is not None:
        match.clockSeconds = seconds

    if match.clockSeconds <= 0 and match.status != "ended":
        match.clockSeconds = 0
        match.clockRunning = False
        if match.pointsAka != match.pointsAo:
            match.status = "ended"
            match.endReason = "time"
            match.winner = "aka" if match.pointsAka > match.pointsAo else "ao"
            _push_log(match, f"Time. Winner: {match.winner.upper()}")
        else:
            _push_log(match, "Time. Scores level — awaiting Hantei decision.")


def record_hantei(match: KumiteMatch, side: str) -> None:
    match.status = "ended"
    match.endReason = "hantei"
    match.winner = side
    _push_log(match, f"Hantei decision: {side.upper()} wins")
