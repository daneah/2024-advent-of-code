#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# ///
INITIAL_STATE = "^"
STATES = {
    "^": {
        "vector": (0, -1),
        "next": ">",
    },
    ">": {
        "vector": (1, 0),
        "next": "v",
    },
    "v": {
        "vector": (0, 1),
        "next": "<",
    },
    "<": {
        "vector": (-1, 0),
        "next": "^",
    },
}


def _get_data() -> str:
    with open("data.txt") as f:
        return f.read().strip()


def _get_initial_position(grid: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item == INITIAL_STATE:
                return x, y
    raise ValueError("Initial position not found")


def _get_path_string_from_grid(grid: list[list[str]]) -> str:
    return "\n".join(["".join(row) for row in grid])


def _print_grid(grid: list[list[str]]) -> None:
    print(_get_path_string_from_grid(grid))


def _get_grid_from_path_string(path: str) -> list[list[str]]:
    return [list(row) for row in path.split("\n")]


def _in_bounds(grid: list[list[str]], x: int, y: int) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def _get_next_state(current_state: dict | None, is_blocked: bool) -> dict:
    if not current_state:
        return STATES[INITIAL_STATE]
    return STATES[current_state["next"]] if is_blocked else current_state


def _get_next_position(current_x: int, current_y: int, current_state: dict) -> tuple[int, int]:
    dx, dy = current_state["vector"]
    return current_x + dx, current_y + dy


def _map_guard_path(grid: list[list[str]]) -> tuple[str, bool]:
    mapped_grid = [row.copy() for row in grid]

    current_state = _get_next_state(None, False)
    current_x, current_y = _get_initial_position(mapped_grid)

    has_cycled = False

    while _in_bounds(mapped_grid, current_x, current_y):
        next_x, next_y = _get_next_position(current_x, current_y, current_state)
        already_visited = mapped_grid[current_y][current_x] == "X"
        mapped_grid[current_y][current_x] = "X"

        if not _in_bounds(mapped_grid, next_x, next_y):
            break

        is_blocked = mapped_grid[next_y][next_x] in {"#", "O"}

        if is_blocked and already_visited:
            if not has_cycled:
                has_cycled = True
            else:
                return _get_path_string_from_grid(mapped_grid), True

        current_state = _get_next_state(current_state, is_blocked)
        next_x, next_y = _get_next_position(current_x, current_y, current_state)
        current_x, current_y = next_x, next_y

    return _get_path_string_from_grid(mapped_grid), False


def _count_guard_positions(initial_path: str) -> int:
    grid = _get_grid_from_path_string(initial_path)
    return _map_guard_path(grid)[0].count("X")


def _count_obstacle_positions(initial_path: str) -> int:
    obstacle_positions = 0
    initial_grid = _get_grid_from_path_string(initial_path)
    initial_x, initial_y = _get_initial_position(initial_grid)
    initial_path, _ = _map_guard_path(initial_grid)
    grid = _get_grid_from_path_string(initial_path)

    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item == "X" and (x != initial_x or y != initial_y):
                new_grid = [row.copy() for row in initial_grid]
                new_grid[y][x] = "O"
                _, has_cycle = _map_guard_path(new_grid)
                if has_cycle:
                    obstacle_positions += 1
    return obstacle_positions


if __name__ == "__main__":
    assert _map_guard_path(_get_grid_from_path_string("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""))[0] == """....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X.."""

    assert _count_guard_positions("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""") == 41

    assert _count_obstacle_positions("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""") == 6

    # Part one
    print(_count_guard_positions(_get_data()))

    # Part two
    print(_count_obstacle_positions(_get_data()))
