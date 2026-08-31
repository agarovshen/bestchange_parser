from logic import generate_pairs_list

def test_generate_pairs_list():
    currency_ids = [1,2,3,4]
    assert len(currency_ids) == len(set(currency_ids))
    assert all(type(c) == int and c > 0 for c in currency_ids)
    assert len(currency_ids) > 1
    result = generate_pairs_list(currency_ids)
    expected_len = len(currency_ids) * (len(currency_ids) - 1)
    assert len(result) == expected_len
    for i in range(0, len(result), 2):
        d = result[i].split("-")
        r = result[i+1].split("-")
        assert d[0] == r[1] and d[1] == r[0]
        assert d[0] != d[1]
    assert result == [
            "1-2",
            "2-1",
            "1-3",
            "3-1",
            "2-3",
            "3-2"
        ]