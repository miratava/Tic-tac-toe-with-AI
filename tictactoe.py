import enum
import random


class Status(enum.Enum):
    ok = 1
    draw = 2
    impossible = 3
    x_wins = 4
    o_wins = 5
    not_finished = 6
    error = 7


class Cell:
    is_occupied = "This cell is occupied! Choose another one!"

    def __init__(self, x, y):
        self.state = " "
        self.x = x
        self.y = y

    def get_state(self):
        return self.state

    def set_state(self, state):
        if self.state == " ":
            self.state = state
            return Status.ok, None
        return Status.error, self.is_occupied


class GameSystem:
    x_win = ["X", "X", "X"]
    o_win = ["O", "O", "O"]
    size = 3
    enter_numbers = "You should enter numbers!"
    incorrect_coordinates = "Coordinates should be from 1 to 3!"
    coordinates_not_entered = "Coordinates are not entered"
    message_move_level_easy = 'Making move level "easy"'

    def __init__(self):
        self.input_coordinates = " "
        self.available_cells = [(i % self.size + 1, self.size - i // self.size) for i in range(self.size ** 2)]
        self.cells = []
        for i in range(self.size ** 2):
            self.cells.append(Cell(i % self.size + 1, self.size - i // self.size))

    def draw_row(self, row):
        row_str = ""
        space = " "
        for i in range(self.size):
            row_str += row[i].get_state()
            if i == self.size - 1:
                break
            row_str += space
        print("|", row_str, "|")

    def create_rows(self):
        rows = [3, 2, 1]
        for row in rows:
            yield [cell for cell in self.cells if cell.y == row]

    def create_columns(self):
        columns = [1, 2, 3]
        for column in columns:
            yield [cell for cell in self.cells if cell.x == column]

    def draw_cells(self):
        size = 9
        line = size * "-"
        print(line)
        for row in self.create_rows():
            self.draw_row(row)
        print(line)

    def get_coordinates(self):
        x_index = 0
        y_index = -1
        x = self.input_coordinates[x_index]
        y = self.input_coordinates[y_index]
        return x, y

    def validate_input_x_y(self):
        x, y = self.get_coordinates()
        if not x.isdigit() or not y.isdigit():
            return Status.error, self.enter_numbers
        if int(x) > self.size or int(y) > self.size:
            return Status.error, self.incorrect_coordinates
        return Status.ok, (int(x), int(y))

    def find_cell(self, x, y):
        cells = [cell for cell in self.cells if cell.x == x and cell.y == y]
        return cells[0]

    def is_input_coordinates_empty(self):
        if self.input_coordinates == "":
            return True
        return False

    def get_group_status(self, group, count):
        amount_moves = 2
        player = "O"
        cells = [cell.get_state() for cell in group]
        if cells == self.x_win:
            return Status.x_wins, None
        # if cells == self.o_win:
        #     return Status.o_wins, None
        if cells.count(player) == amount_moves:
            if " " in cells:
                return Status.error, (cells.index(" ") + 1, count)
        return Status.ok, None

    def rows_status(self):
        count = 1
        for row in self.create_rows():
            status, value = self.get_group_status(row, count)
            if status is Status.error:
                return status, value
            count += 1
        return Status.ok, None

    def columns_status(self):
        count = 1
        for column in self.create_columns():
            status, value = self.get_group_status(column, count)
            if status is Status.error:
                return status, value
            count += 1
        return Status.ok, None

    def diagonals_status(self):
        diagonal_designator = self.size + 1
        diagonal1 = [cell.get_state() for cell in self.cells if cell.x == cell.y]
        diagonal2 = [cell.get_state() for cell in self.cells if cell.x == diagonal_designator - cell.y]
        player = "O"
        number_of_move = 2
        if diagonal1 == self.x_win or diagonal2 == self.x_win:
            return Status.x_wins, None
        # if diagonal1 == self.o_win or diagonal2 == self.o_win:
        #     return Status.o_wins, None
        if diagonal1.count(player) == number_of_move:
            if " " in diagonal1:
                x = diagonal1.index(" ") + 1
                return Status.error, (x, x)
        if diagonal2.count(player) == number_of_move:
            if " " in diagonal2:
                x = diagonal2.index(" ") + 1
                return Status.error, (x, x - 1)
        return Status.ok, None

    def get_status_draw(self):
        states = []
        for cell in self.cells:
            states.append(cell.get_state())
        if " " not in states:
            return Status.draw
        return Status.ok

    def get_status(self):
        status, value = self.rows_status()
        if status is Status.x_wins:
            return Status.x_wins, "X wins"
        status, value = self.columns_status()
        if status is Status.x_wins:
            return Status.x_wins, "X wins"
        status, value = self.diagonals_status()
        if status is Status.x_wins:
            return Status.x_wins, "X wins"
        if self.get_status_draw() is Status.draw:
            return Status.draw, "Draw"
        return Status.ok, None

    def get_available_cells(self):
        free_cells = [(cell.x, cell.y) for cell in self.cells if cell.get_state() == " "]
        status, value = self.rows_status()
        if status is Status.error and value in free_cells:
            free_cells.remove(value)
        status, value = self.columns_status()
        if status is Status.error and value in free_cells:
            free_cells.remove(value)
        status, value = self.diagonals_status()
        if status is Status.error and value in free_cells:
            free_cells.remove(value)
        return free_cells

    @staticmethod
    def print_message_about_player_level_easy():
        print('Making move level "easy"')

    def make_move_user(self):
        player = "X"
        status, value = self.validate_input_x_y()
        if status is Status.ok:
            x, y = value
            cell = self.find_cell(x, y)
            status, value = cell.set_state(player)
            if status is Status.ok:
                self.draw_cells()
        return status, value

    @staticmethod
    def get_coordinates_level_easy(free_cells):
        index = random.randint(0, len(free_cells) - 1)
        coordinates = free_cells[index]
        if len(free_cells) == 1:
            coordinates = free_cells[0]
        return coordinates

    def make_move_easy_level(self):
        player = "O"
        free_cells = self.get_available_cells()
        x, y = self.get_coordinates_level_easy(free_cells)
        cell = self.find_cell(x, y)
        cell.set_state(player)
        self.draw_cells()
        return Status.ok, None

    def play_game(self, coordinates):
        self.input_coordinates = coordinates.strip()
        if self.is_input_coordinates_empty():
            return Status.error, self.coordinates_not_entered
        status, value = self.make_move_user()
        if status is not Status.ok:
            return status, value
        status, value = self.get_status()
        if status is Status.x_wins or status is Status.draw:
            return status, value
        self.print_message_about_player_level_easy()
        self.make_move_easy_level()
        status, value = self.get_status()
        if status is Status.x_wins:
            return status, value
        return Status.ok, None


def main():
    game = GameSystem()
    print()
    game.draw_cells()
    status = Status.error
    while status:
        coordinates = input("Enter the coordinates: ")
        status, value = game.play_game(coordinates)
        if status is Status.x_wins or status is Status.draw:
            print(value)
            break
        if value is not None:
            print(value)
            continue


main()
