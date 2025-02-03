import copy
import random

# Global variables
global current_player
global computer_revealed

current_player = None
computer_revealed = False

# Initialize grid
rows = 10
cols = 10
grid = [[False for _ in range(cols)] for _ in range(rows)]
num_mines = 25
mine_positions = random.sample(range(rows * cols), num_mines)

# Set mines in grid
for pos in mine_positions:
    row = pos // cols
    col = pos % cols
    grid[row][col] = True

# Create game data
data = {
    'rows': rows,
    'cols': cols,
    'grid': grid,
    'mine_positions': mine_positions,
    'total_cells': rows * cols
}

new_data = copy.deepcopy(data)
new_data['grid'] = [[False for _ in range(cols)] for _ in range(rows)]

current_game = {
    'data': new_data,
    'mine_positions': mine_positions,
    'revealed_cells': 0,
    'current_player': None,
    'is_mine_revealed': False
}

# Define directions for movement
directions = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),            (0, 1),
              (1, -1),          (1, 0),  (1, 1)]


def check_mine_loss():
    """Check if a mine has been revealed."""
    for row in data['grid']:
        for cell in row:
            if cell:  # True means it's a mine
                return True
    return False


def switch_player():
    """Switch between player and computer."""
    global current_player, computer_revealed
    if current_player is None:
        current_player = 'player'
        computer_revealed = False
    else:
        current_player = 'computer' if not computer_revealed else 'player'


def main():
    global current_game

    while True:
        # Process Computer Move
        if current_game['current_player'] == 'computer':
            move = random.choice(directions)
            row = current_game['revealed_cells'] + move[0]
            col = current_game['revealed_cells'] + move[1]

            if 0 <= row < data['rows'] and 0 <= col < data['cols']:
                cell = grid[row][col]
                if not cell:
                    current_game['revealed_cells'] += 1
                    current_game['current_player'] = 'computer'
        else:  # Player's Turn
            row = current_game['revealed_cells']
            col = current_game['revealed_cells']

        # Check for Mine Loss on Current Move
        if check_mine_loss():
            print("Computer wins!")
            return

        # Process Player's Turn
        neighbors = directions
        for dr, dc in neighbors:
            r = row + dr
            c = col + dc
            if 0 <= r < data['rows'] and 0 <= c < data['cols']:
                neighbor = grid[r][c]
                if not neighbor:
                    print(f"My turn: I moved into cell {r},{c}")
                    computer_revealed = True
                    current_game['revealed_cells'] += 1

        # Check for Mine Loss on Player Move
        if check_mine_loss():
            print("Player loses!")
            return

        # Switch players
        switch_player()


if __name__ == "__main__":
    main()