def test_list_divisions_returns_seed_data(client):
    response = client.get("/divisions")
    assert response.status_code == 200
    divisions = response.json()
    assert len(divisions) == 2
    kumite_division = next(d for d in divisions if d["discipline"] == "kumite")
    assert kumite_division["name"] == "Cadet Male -63kg Kumite"
    assert kumite_division["mat"] == 1


def test_get_bracket_for_known_division(client):
    response = client.get("/divisions/div-kumite-1/bracket")
    assert response.status_code == 200
    bracket = response.json()
    assert len(bracket["pool"]) == 3
    assert len(bracket["elimination"]) == 2


def test_get_bracket_for_unknown_division_is_404(client):
    response = client.get("/divisions/does-not-exist/bracket")
    assert response.status_code == 404
