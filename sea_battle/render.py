"""Render."""

from field import Field
from ship import Ship, DAMAGED, UNDAMAGED
from exceptions import SBUnknownStatus

FIELD_TEMPLATE = """
   │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 0 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 1 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 2 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 3 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 4 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 5 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 6 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 7 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 8 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼
 9 │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │ {} │
"""
ELIMINATED_MARKER = "F"
DAMAGED_MARKER = "X"
UNDAMAGED_MARKER = " "
MISSED_MARKER = "*"
CLEAN_MARKER = " "


def get_marker(field: Field, coord):
    target_ship = field.get_ship_intersection(coord)

    if target_ship:
        if target_ship.is_eliminated():
            return ELIMINATED_MARKER

        deck_index = target_ship.get_deck_index(coord)
        deck_status = target_ship.get_deck_status(deck_index)
        if deck_status == DAMAGED:
            return DAMAGED_MARKER
        if deck_status == UNDAMAGED:
            return UNDAMAGED_MARKER

    if coord in field.get_missed_bullets():
        return MISSED_MARKER
    return CLEAN_MARKER


def render(field: Field) -> None:
    x_len = field.get_x_len()
    y_len = field.get_y_len()
    markers = []
    for x in range(x_len):
        for y in range(y_len):
            marker = get_marker(field, (x, y))
            markers.append(marker)

    print(FIELD_TEMPLATE.format(*markers))


if __name__ == '__main__':
    f = Field()
    f.add_ship(
        Ship((1, 1)),
        Ship((2, 2), (2, 3)),
        Ship((3, 3), (3, 4), (3, 5))
    )

    bullets = [
        (0, 0),
        (1, 1),
        (2, 2),
        (2, 3),
        (3, 3),
        (5, 5)
    ]

    for bullet in bullets:
        f.receive_bullet(bullet)
    render(f)
