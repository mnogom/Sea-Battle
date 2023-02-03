"""Field."""

from sea_battle.ship import Ship


class Field:
    def __init__(self, x_len: int = 10, y_len: int = 10) -> None:
        self._x_len = x_len
        self._y_len = y_len
        self._ships = []
        self._hited_cells = set()

    def get_ships(self) -> list[Ship]:
        return self._ships

    def add_ship(self, *ships: Ship) -> None:
        self._ships.extend([*ships])

    def get_x_len(self) -> int:
        return self._x_len

    def get_y_len(self) -> int:
        return self._y_len

    def add_hited_cell(self, *bullet_coord: tuple[int, int]) -> None:
        self._hited_cells = self._hited_cells.union(set(bullet_coord))

    def get_hited_cells(self) -> set[tuple[int, int]]:
        return self._hited_cells

    def get_ship_intersection(self, coord: tuple[int, int]) -> Ship | None:
        ships = self.get_ships()
        for ship in ships:
            if any(deck_coord == coord for deck_coord in ship.get_coords()):
                return ship
        return None

    def receive_bullet(self, bullet_coord: tuple[int, int]) -> None:
        self.add_hited_cell(bullet_coord)
        target_ship = self.get_ship_intersection(bullet_coord)
        if target_ship:
            target_ship.receive_damage(bullet_coord)
            if target_ship.is_eliminated():
                x_max = self.get_x_len() - 1
                y_max = self.get_y_len() - 1
                safe_area = target_ship.get_safe_area(x_max, y_max)
                self.add_hited_cell(*safe_area)

    def can_shoot(self):
        ships = self.get_ships()
        return not all(ship.is_eliminated() for ship in ships)
