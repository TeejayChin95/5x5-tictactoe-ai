"""
5x5 Tic-Tac-Toe - Initial State and State Space

This file defines the game as a formal search problem for the AI project.

Game type: two player, zero sum, deterministic, fully observable,
turn based, adversarial.

STATE REPRESENTATION
A state is (board, player_to_move).

board is a dict that maps (row, col) to 'X' or 'O'. Only filled cells
are stored, so an empty board is just an empty dict. I used coordinate
tuples instead of numbering cells 1 to 25 because a flat number can get
mistaken for a value the algorithm should maximize, when really it is
just a label for a position.

Rows and columns go from 1 to 5. (1,1) is top left, (5,5) is bottom
right.

WHY heapq
Python's heapq compares tuples in order, so (1,1) < (1,2) < (2,1) and so
on. That gives a consistent order for generating moves (row by row, left
to right) without turning a coordinate into a single number. This also
gives a fixed order to build on later for move ordering in minimax or
MCTS.

NOTE ON DIRECTIONS
Wins can happen diagonally too, not just up/down/left/right. So instead
of checking N, S, E, W separately, the code below checks 4 axis lines
(horizontal, vertical, and both diagonals) in both directions from a
cell. That covers all 8 directions using only 4 vectors.
"""

import heapq
from typing import Dict, List, Tuple, Optional

Coordinate = Tuple[int, int]
Board = Dict[Coordinate, str]
State = Tuple[Board, str]

BOARD_SIZE = 5
K = 5  # how many in a row wins. confirm 4 or 5 with the team
PLAYERS = ('X', 'O')

# 4 line directions to check from a filled cell.
# checking both signs of each one covers all 8 directions.
AXES: List[Coordinate] = [
    (0, 1),   # horizontal
    (1, 0),   # vertical
    (1, 1),   # diagonal, top left to bottom right
    (1, -1),  # diagonal, top right to bottom left
]


def initial_state() -> State:
    """Empty 5x5 board, X moves first."""
    empty_board: Board = {}
    return (empty_board, 'X')


def in_bounds(coord: Coordinate) -> bool:
    r, c = coord
    return 1 <= r <= BOARD_SIZE and 1 <= c <= BOARD_SIZE


def get_legal_moves(state: State) -> List[Coordinate]:
    """
    Returns every empty cell as a legal move. Kept in heap order
    (row by row) instead of sorted by any kind of score.
    """
    board, _ = state
    occupied = set(board.keys())
    all_cells = [(r, c) for r in range(1, BOARD_SIZE + 1) for c in range(1, BOARD_SIZE + 1)]
    legal = [cell for cell in all_cells if cell not in occupied]
    heapq.heapify(legal)
    return legal


def other_player(player: str) -> str:
    return 'O' if player == 'X' else 'X'


def apply_move(state: State, action: Coordinate) -> State:
    """
    Places the current player's mark and switches turns.
    Returns a new state instead of changing the old one, since the
    search tree needs to keep old states around to branch from.
    """
    board, player = state
    if action in board:
        raise ValueError(f"{action} is already taken.")
    if not in_bounds(action):
        raise ValueError(f"{action} is off the board.")

    new_board = dict(board)
    new_board[action] = player
    return (new_board, other_player(player))


def check_winner(state: State) -> Optional[str]:
    """
    Looks at every filled cell and checks all 4 axis lines through it.
    Counts how far the same mark goes in both directions along that
    line. If it hits K or more, that mark wins.
    """
    board, _ = state
    for (r, c), mark in board.items():
        for dr, dc in AXES:
            count = 1
            step = 1
            while board.get((r + dr * step, c + dc * step)) == mark:
                count += 1
                step += 1
            step = 1
            while board.get((r - dr * step, c - dc * step)) == mark:
                count += 1
                step += 1
            if count >= K:
                return mark
    return None


def is_draw(state: State) -> bool:
    """Board is full and nobody won."""
    board, _ = state
    return len(board) == BOARD_SIZE * BOARD_SIZE and check_winner(state) is None


def is_terminal(state: State) -> bool:
    return check_winner(state) is not None or is_draw(state)


def reward(state: State, agent: str) -> int:
    """+1 if agent won, -1 if agent lost, 0 for draw or game not over."""
    winner = check_winner(state)
    if winner is None:
        return 0
    return 1 if winner == agent else -1


def print_board(state: State) -> None:
    """Prints the board so you can see it while testing."""
    board, player = state
    print(f"  {' '.join(str(c) for c in range(1, BOARD_SIZE + 1))}")
    for r in range(1, BOARD_SIZE + 1):
        row_str = ' '.join(board.get((r, c), '.') for c in range(1, BOARD_SIZE + 1))
        print(f"{r} {row_str}")
    print(f"Next to move: {player}\n")


if __name__ == "__main__":
    state = initial_state()
    print("Initial state:")
    print_board(state)

    moves = get_legal_moves(state)
    print(f"Legal moves from the start: {len(moves)}")
    print(f"First 5 in order: {sorted(moves)[:5]}\n")

    # play a few moves to test the win check
    demo_moves = [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4), (1, 5)]
    for mv in demo_moves:
        state = apply_move(state, mv)

    print("After X gets 5 in a row on row 1:")
    print_board(state)
    print(f"Winner: {check_winner(state)}")
    print(f"Game over: {is_terminal(state)}")
