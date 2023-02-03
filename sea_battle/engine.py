"""Engine."""

import random

from sea_battle.field import Field
from sea_battle.ship import Ship
from sea_battle.renders import render_fields
from sea_battle.exceptions import SBReHitCell

SHIPS_RULE = [
    {"deck_count": 4, "count": 1},
    {"deck_count": 3, "count": 2},
    {"deck_count": 2, "count": 3},
    {"deck_count": 1, "count": 4},
]

DIRECTIONS = (
    (1, 0),
    (0, 1),
)

PLAYER_TURN = "player"
AI_TURN = "turn"


def _create_field(x_len: int = 10, y_len: int = 10) -> Field:
    """Create empty field."""

    return Field(x_len, y_len)


def _auto_place_ships(field: Field) -> Field:
    """Place ships in random positions."""
    if len(field.get_ships()) != 0:
        return field

    x_len = field.get_x_len()
    y_len = field.get_y_len()
    field_coords = set((x, y) for y in range(y_len) for x in range(x_len))

    safe_zones = []
    occupied_coords = set()
    for ship_rule in SHIPS_RULE:
        deck_count = ship_rule["deck_count"]
        ships_count = ship_rule["count"]

        for _ in range(ships_count):
            # Get direction of ship
            direction_x, direction_y = random.choice(DIRECTIONS)

            # Get forbidden area near border
            x_min = x_len - deck_count if direction_x == 1 else 0
            y_min = y_len - deck_count if direction_y == 1 else 0
            forbidden_area = set(
                (x, y)
                for x in range(x_min, x_len)
                for y in range(y_min, y_len))

            # Get forbidden area near safe zones
            safe_zones_offsets = set()
            for safe_zone in safe_zones:
                # Top left corner
                x_min, y_min = min(safe_zone)
                # Bottom right corner
                x_max, y_max = max(safe_zone)
                x_min = x_min - deck_count if direction_x == 1 else x_min
                y_min = y_min - deck_count if direction_y == 1 else y_min

                safe_zones_offsets = safe_zones_offsets.union(set(
                    (x, y)
                    for x in range(x_min, x_max + 1)
                    for y in range(y_min, y_max + 1)
                ))

            # Get possible coordinates without forbidden areas
            possible_coords = field_coords.difference(forbidden_area)
            possible_coords = possible_coords.difference(safe_zones_offsets)
            possible_coords = possible_coords.difference(occupied_coords)

            ship_coords = [random.choice(list(possible_coords))]
            for _ in range(deck_count - 1):
                last_x, last_y = ship_coords[-1]
                ship_coords.append(
                    (last_x + direction_x, last_y + direction_y))

            occupied_coords = occupied_coords.union(ship_coords)
            ship = Ship(*ship_coords)
            safe_zones.append(ship.get_safe_area(x_len - 1, y_len - 1))

            field.add_ship(ship)

    return field


def _make_shoot(field: Field, bullet_coord: tuple[int, int]) -> Field:
    """Send bullet to the field."""

    if bullet_coord in field.get_hited_cells():
        raise SBReHitCell
    field.receive_bullet(bullet_coord)
    return field


def _init_game() -> tuple[Field, Field]:
    """Init game. Create field and place ships."""

    player_field = _create_field()
    ai_field = _create_field()

    player_field = _auto_place_ships(player_field)
    ai_field = _auto_place_ships(ai_field)
    return player_field, ai_field


def play() -> None:
    """Start game and iterate steps."""

    player_field, ai_field = _init_game()
    render_fields(player_field, ai_field)
    turn = PLAYER_TURN

    x_len = player_field.get_x_len()
    y_len = player_field.get_y_len()
    coords = set((x, y) for x in range(x_len) for y in range(y_len))

    while player_field.can_shoot() and ai_field.can_shoot():
        if turn == PLAYER_TURN:
            bullet_coord = input(" >> (row column) > ")
            x, y = bullet_coord.split(" ")
            x = int(x)
            y = int(y)
            try:
                ai_field = _make_shoot(ai_field, (x, y))
            except SBReHitCell:
                print("Already hit there. Try again")
                continue

            render_fields(player_field, ai_field)
            turn = AI_TURN
        else:
            hited_cells = player_field.get_hited_cells()
            coords_to_shoot = coords.difference(hited_cells)
            bullet_coord = random.choice(list(coords_to_shoot))

            player_field = _make_shoot(player_field, bullet_coord)
            turn = PLAYER_TURN
            render_fields(player_field, ai_field)

    if player_field.can_shoot():
        print("Congratulations! You win!")
    if ai_field.can_shoot():
        print("Nice try! Try again.")
