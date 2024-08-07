from typing import List, Tuple


def merge_straight_lines(xys: List[Tuple[float, float]]) -> List[Tuple[float, float]]:  # noqa: C901
    points: List[Tuple[float, float]] = []

    skip_next = False
    for i in range(len(xys) - 1):
        if skip_next:
            skip_next = False
            continue

        if i == 0:
            points.append(xys[i])
            continue

        x0, y0 = points[-1]
        x1, y1 = xys[i]
        x2, y2 = xys[i + 1]
        if x1 - x0 == 0:
            if x2 - x1 == 0:
                points.append(xys[i + 1])
                skip_next = True
                continue
            else:
                points.append(xys[i])
                if i == len(xys) - 2:
                    points.append(xys[i + 1])
                continue

        if x2 - x1 == 0:
            points.append(xys[i])
            if i == len(xys) - 2:
                points.append(xys[i + 1])
            continue

        m1 = (y1 - y0) / (x1 - x0)
        m2 = (y2 - y1) / (x2 - x1)
        if m1 == m2:
            skip_next = True
            points.append(xys[i + 1])
        else:
            points.append(xys[i])
            if i == len(xys) - 2:
                points.append(xys[i + 1])

    return points


def test():
    print(merge_straight_lines([(1, 1), (2, 2), (3, 3), (4, 2), (5, 1)]))
    assert merge_straight_lines([
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 2),
        (5, 1),
    ]) == [(1, 1), (3, 3), (5, 1)]
    print(merge_straight_lines([(1, 1), (1, 2), (1, 3), (2, 3), (2, 2), (2, 1)]))
    assert merge_straight_lines([
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 2),
        (2, 1),
    ]) == [
        (1, 1),
        (1, 3),
        (2, 3),
        (2, 1),
    ]
