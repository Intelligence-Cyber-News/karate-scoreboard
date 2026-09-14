def test_get_unknown_match_is_404(client):
    response = client.get("/kumite-matches/does-not-exist")
    assert response.status_code == 404


def test_list_matches_includes_seed_match(client):
    response = client.get("/kumite-matches")
    assert response.status_code == 200
    matches = response.json()
    assert any(m["id"] == "km-1" for m in matches)


def test_award_point_increments_score(client):
    response = client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 2})
    assert response.status_code == 200
    match = response.json()
    assert match["pointsAka"] == 2
    assert match["pointsAo"] == 0


def test_first_point_awards_senshu(client):
    response = client.post("/kumite-matches/km-1/points", json={"side": "ao", "points": 1})
    match = response.json()
    assert match["senshu"] == "ao"

    # senshu does not change once awarded, even if the other side scores next
    response = client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 3})
    match = response.json()
    assert match["senshu"] == "ao"


def test_eight_point_gap_ends_the_match(client):
    client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 3})
    client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 3})
    response = client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 2})
    match = response.json()
    assert match["status"] == "ended"
    assert match["endReason"] == "points"
    assert match["winner"] == "aka"


def test_fourth_c1_penalty_disqualifies_opponent_wins(client):
    for _ in range(3):
        client.post("/kumite-matches/km-1/penalties", json={"side": "aka", "category": "c1"})
    response = client.post("/kumite-matches/km-1/penalties", json={"side": "aka", "category": "c1"})
    match = response.json()
    assert match["status"] == "ended"
    assert match["endReason"] == "disqualification"
    assert match["winner"] == "ao"


def test_points_and_penalties_are_rejected_after_match_ends(client):
    for _ in range(4):
        client.post("/kumite-matches/km-1/penalties", json={"side": "aka", "category": "c1"})
    before = client.get("/kumite-matches/km-1").json()

    client.post("/kumite-matches/km-1/points", json={"side": "ao", "points": 1})
    after = client.get("/kumite-matches/km-1").json()

    assert after["pointsAo"] == before["pointsAo"]


def test_clock_reaching_zero_with_unequal_score_ends_match_by_time(client):
    client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 1})
    response = client.patch("/kumite-matches/km-1/clock", json={"seconds": 0})
    match = response.json()
    assert match["status"] == "ended"
    assert match["endReason"] == "time"
    assert match["winner"] == "aka"


def test_clock_reaching_zero_tied_requires_hantei(client):
    response = client.patch("/kumite-matches/km-1/clock", json={"seconds": 0})
    match = response.json()
    assert match["status"] == "in_progress"
    assert match["clockSeconds"] == 0


def test_hantei_decides_a_tied_match(client):
    client.patch("/kumite-matches/km-1/clock", json={"seconds": 0})
    response = client.post("/kumite-matches/km-1/hantei", json={"side": "ao"})
    match = response.json()
    assert match["status"] == "ended"
    assert match["endReason"] == "hantei"
    assert match["winner"] == "ao"


def test_actions_on_unknown_match_are_404(client):
    response = client.post("/kumite-matches/does-not-exist/points", json={"side": "aka", "points": 1})
    assert response.status_code == 404
