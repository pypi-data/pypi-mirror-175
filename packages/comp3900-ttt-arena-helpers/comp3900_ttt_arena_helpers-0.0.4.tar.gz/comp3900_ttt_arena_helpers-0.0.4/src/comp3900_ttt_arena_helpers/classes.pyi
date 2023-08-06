class AgentMove:
    row: int
    col: int
    def __init__(self, row, col) -> None: ...

class GameState:
    rows: int
    cols: int
    k: int
    current_move: str
    grid: list[list[str]]
    def __init__(self, rows, cols, k, current_move, grid) -> None: ...
