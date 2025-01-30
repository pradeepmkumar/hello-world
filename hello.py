
import random
from tkinter import Tk, Button, Frame, Entry, messagebox, LEFT, SOLID, TOP, BOTTOM

class Minesweeper:
    def __init__(self):
        self.root = Tk()
        self.root.title("Minesweeper")

        # Grid dimensions and number of mines
        self.rows = 10
        self.cols = 10
        self.mines = 20

        # Initialize grid
        self.grid = []
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False

    def create_grid(self):
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if random.random() < self.mines / (self.rows * self.cols):
                    row.append(('*', random.randint(1, 5)))
                else:
                    row.append((0, 0))
            self.grid.append(row)

        # Calculate adjacent mines
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j][0] == 0 and self.grid[i][j][1] != '*':
                    count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            x = i + dx
                            y = j + dy
                            if 0 <= x < self.rows and 0 <= y < self.cols:
                                if self.grid[x][y][0] == '*':
                                    count += 1
                    self.grid[i][j] = (count, False)
                else:
                    self.grid[i][j] = (self.grid[i][j][0], True)

    def place_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.revealed[i][j] and random.random() < self.mines / (self.rows * self.cols):
                    if self.grid[i][j][1] == False:
                        self.grid[i][j] = ('*', True)
                        self.revealed[i][j] = True

    def reveal_cell(self, i, j):
        if self.revealed[i][j]:
            return
        if self.grid[i][j][0] == '*':
            self.game_over = True
            self.root.destroy()
            messagebox.showerror("Game Over")
            return
        self.revealed[i][j] = True

    def reveal_number(self, i, j):
        if self.revealed[i][j]:
            return
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x = i + dx
                y = j + dy
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    if not self.revealed[x][y]:
                        self.reveal_number(x, y)

    def right_click(self, i, j):
        self.revealed[i][j] = True

    def is_game_over(self):
        return self.game_over

    def win_condition(self):
        for row in self.grid:
            for cell in row:
                if not cell[1]:
                    return False
        return True

def main():
    game = Minesweeper()
    game.create_grid()
    game.place_mines()

    for i in range(game.rows):
        for j in range(game.cols):
            if game.revealed[i][j]:
                continue
            row = Frame(game.root, width=game.cols*30+1)
            row.pack(side=LEFT, padx=5, pady=2)
            col = Frame(row, width=30, borderwidth=1, relief=SOLID)
            for j in range(game.cols):
                button = Button(col, command=lambda i=i, j=j: game.reveal_number(i, j))
                if not game.revealed[i][j]:
                    if game.grid[i][j][0] == '*':
                        col.pack(side=TOP, padx=5)
                        button.config(background="#CD4F32", foreground="white")
                        button.bind("<Button-1>", lambda i=i,j=j: game.right_click(i,j))
                    else:
                        col.pack(side=TOP, padx=5)
                        button.config(background="#98FB98", foreground="black")
                else:
                    if j % 2 == 0 and (game.grid[i][j][0] != '*'):
                        col.pack(side=BOTTOM, padx=5)
            row.pack()

    game.root.mainloop()

if __name__ == "__main__":
    main()
