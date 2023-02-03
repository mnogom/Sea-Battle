"""Ship class."""

DAMAGED = "damaged"
UNDAMAGED = "undamaged"


class Ship:
    def __init__(self, *coords: tuple[int, int]) -> None:
        self._coords = coords
        self._deck_statuses = [UNDAMAGED] * len(coords)

    def get_coords(self) -> tuple:
        return self._coords

    def get_safe_area(self, x_max: int, y_max: int) -> set:
        safe_area = set()
        deck_coords = self.get_coords()

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for (x, y) in deck_coords:
                    safe_x = x + dx
                    safe_y = y + dy
                    if 0 <= safe_x <= x_max and 0 <= safe_y <= y_max:
                        safe_area.add((safe_x, safe_y))
        safe_area = safe_area.difference(set(deck_coords))
        return safe_area

    def get_decks_statuses(self) -> list:
        return self._deck_statuses

    def get_deck_index(self, coord: tuple[int, int]) -> int:
        coords = self.get_coords()
        deck_index = coords.index(coord)
        return deck_index

    def get_deck_status(self, deck_index):
        return self.get_decks_statuses()[deck_index]

    def set_deck_status(self, deck_index: int, status: str) -> None:
        self._deck_statuses[deck_index] = status

    def is_eliminated(self) -> bool:
        return all([deck_status == DAMAGED
                    for deck_status in self.get_decks_statuses()])

    def receive_damage(self, bullet_coord: tuple[int, int]) -> None:
        coord = self.get_coords()
        deck_index = coord.index(bullet_coord)
        self.set_deck_status(deck_index, DAMAGED)
