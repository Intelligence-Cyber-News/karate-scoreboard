def test_get_unknown_performance_is_404(client):
    response = client.get("/kata-performances/does-not-exist")
    assert response.status_code == 404


def test_list_performances_includes_seed_performance(client):
    response = client.get("/kata-performances")
    assert response.status_code == 200
    performances = response.json()
    assert any(p["id"] == "kt-1" for p in performances)


def test_submitting_fewer_than_seven_scores_leaves_it_scoring(client):
    response = client.post(
        "/kata-performances/kt-1/scores", json={"judgeIndex": 0, "score": 8.0}
    )
    performance = response.json()
    assert performance["status"] == "scoring"
    assert performance["finalScore"] is None
    assert performance["judgeScores"][0] == 8.0


def test_seventh_score_computes_drop_high_low_average(client):
    scores = [8.0, 8.5, 9.0, 7.5, 8.2, 5.0, 10.0]  # low=5.0, high=10.0, dropped
    for index, score in enumerate(scores):
        response = client.post(
            "/kata-performances/kt-1/scores", json={"judgeIndex": index, "score": score}
        )

    performance = response.json()
    assert performance["status"] == "scored"
    remaining = sorted(scores)[1:-1]
    expected = round(sum(remaining) / len(remaining), 2)
    assert performance["finalScore"] == expected


def test_reset_clears_scores(client):
    for index in range(7):
        client.post("/kata-performances/kt-1/scores", json={"judgeIndex": index, "score": 8.0})

    response = client.post("/kata-performances/kt-1/reset")
    performance = response.json()
    assert performance["status"] == "scoring"
    assert performance["finalScore"] is None
    assert all(s is None for s in performance["judgeScores"])


def test_score_out_of_range_is_rejected(client):
    response = client.post(
        "/kata-performances/kt-1/scores", json={"judgeIndex": 0, "score": 15}
    )
    assert response.status_code == 422
