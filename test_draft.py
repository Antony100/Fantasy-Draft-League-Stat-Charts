import pytest
import draft

@pytest.mark.parametrize(
    "test, result",
    [
        ([1, 2, 3, 4], 2),
        ([10, 500, 12, 44, 0, 1, -1], 80),
        ([10], 10),
        ([], 0)

    ]
)
def test_point_average(test, result):
    assert draft.point_average(test) == result

