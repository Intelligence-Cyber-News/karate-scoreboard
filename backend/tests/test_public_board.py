def test_public_board_reflects_live_state(client):
    client.post("/kumite-matches/km-1/points", json={"side": "aka", "points": 2})

    response = client.get("/public-board")
    assert response.status_code == 200
    board = response.json()

    kumite_entry = next(m for m in board["kumite"] if m["id"] == "km-1")
    assert kumite_entry["pointsAka"] == 2
    assert kumite_entry["aka"] == "Yuki Tanaka"

    assert any(p["id"] == "kt-1" for p in board["kata"])
