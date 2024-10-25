from Chapter2 import generic_search

def test(x):
    print(x)
    return [x + 1, x * 2, x / 2]

def test2(x):
    if x > 100:
        return x - 100
    else:
        return 100 - x


n: generic_search.Node = generic_search.astar(
    test, lambda x: x == 100, -50, test2)

a: list[int] = generic_search.node_to_path(n)
print(a)

