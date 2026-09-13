# 5x5 Tic-Tac-Toe AI

AI project comparing search and game-playing methods on a 5x5 tic-tac-toe board.

## Problem Type

This project is framed as a contingency problem: since the opponent's next action cannot be predicted with certainty, the agent must plan a conditional strategy rather than a single fixed sequence of moves. This is handled through adversarial search (minimax, alpha-beta pruning), with Monte Carlo Tree Search (MCTS) planned as a comparison method.

## Game Type

Two player, zero sum, deterministic, fully observable, turn based, adversarial.

## State Representation (initial_state.py)

- **State**: (board, player_to_move)
- **Board**: dict mapping (row, col) coordinates to 'X' or 'O'. Empty cells are simply not in the dict.
- **Initial state**: empty board, X moves first.
- **Action space**: every empty cell, returned in row-major order using heapq (get_legal_actions).
- **Transition model**: placing a mark updates the board and switches the active player (apply_action).
- **Terminal test / reward**: win = 4 in a row (row, column, or diagonal); +1 win, -1 loss, 0 draw.

## How to Run

```
python3 initial_state.py
```

This runs a quick demo: prints the empty board, lists legal opening actions, plays a scripted win, and confirms it's detected correctly.

## Status

- [x] Initial state, action space, transition model, terminal test/reward
- [ ] Random baseline agent
- [ ] Minimax + alpha-beta pruning + heuristic evaluation
- [ ] Monte Carlo Tree Search (MCTS)
- [ ] Experiment harness (win rate, timing, comparisons)
- [ ] UI (terminal first, GUI optional later)

## Requirements

Python 3.11+
## Requirements

Python 3.11+
