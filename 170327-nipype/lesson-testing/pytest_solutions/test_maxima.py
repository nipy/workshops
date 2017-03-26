from maxima import find_maxima

def test_maxima():
    inputs = [[1, 2, 1, 0], [-1, 2, 1, 3, 2], [4, 3, 4, 3], [1, 2, 3]]
    expected_maxima = [[1], [1, 3], [0, 2], [2]]
    for i in range(len(inputs)):
        assert find_maxima(inputs[i]) == expected_maxima[i]
