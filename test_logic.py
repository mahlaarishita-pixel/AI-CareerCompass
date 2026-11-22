from app import analyse

def test_basic_match():
    r = analyse("Python SQL data analysis academic project", "Data science intern Python SQL machine learning")
    assert r["score"] >= 0
    assert "python" in r["matched"]

def test_short_inputs_rejected():
    try:
        analyse("too short", "also short")
        assert False
    except ValueError:
        assert True
