import random

# Paso 1: Definir la Clase Ship
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0

    def place_ship(self, board, start_row, start_col, direction):
        if direction == 'H':
            if start_col + self.size > len(board[0]):
                return False
            for i in range(self.size):
                if board[start_row][start_col + i] != ' ':
                    return False
            for i in range(self.size):
                board[start_row][start_col + i] = self.name[0]
                self.positions.append((start_row, start_col + i))
        elif direction == 'V':
            if start_row + self.size > len(board):
                return False
            for i in range(self.size):
                if board[start_row + i][start_col] != ' ':
                    return False
            for i in range(self.size):
                board[start_row + i][start_col] = self.name[0]
                self.positions.append((start_row + i, start_col))
        else:
            return False
        return True

    def hit(self):
        self.hits += 1
        return self.hits == self.size

# Paso 2: Definir Clases Específicas de Barcos
class Destroyer(Ship):
    def __init__(self):
        super().__init__("Destroyer", 2)

class Submarine(Ship):
    def __init__(self):
        super().__init__("Submarine", 3)

class Battleship(Ship):
    def __init__(self):
        super().__init__("Battleship", 4)

# Paso 3: Definir la Clase Player
class Player:
    def __init__(self, name):
        self.name = name
        self.board = [[' ' for _ in range(10)] for _ in range(10)]
        self.hits_board = [[' ' for _ in range(10)] for _ in range(10)]
        self.ships = []

    def place_ships(self):
        for ship_class in [Destroyer, Submarine, Battleship]:
            ship = ship_class()
            placed = False
            while not placed:
                try:
                    row = int(input(f"{self.name}, ingresa la fila para {ship.name} (0-9): "))
                    col = int(input(f"{self.name}, ingresa la columna para {ship.name} (0-9): "))
                    direction = input(f"{self.name}, ingresa la dirección (H/V): ").upper()
                    placed = ship.place_ship(self.board, row, col, direction)
                    if not placed:
                        print("No se pudo colocar el barco, intenta de nuevo.")
                except (ValueError, IndexError):
                    print("Entrada no válida, intenta de nuevo.")
            self.ships.append(ship)

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def attack(self, opponent, row, col):
        if opponent.board[row][col] != ' ':
            print(f"{self.name} impactó un barco en {row},{col}!")
            for ship in opponent.ships:
                if (row, col) in ship.positions:
                    ship.hit()
                    if ship.hits == ship.size:
                        print(f"{ship.name} ha sido hundido!")
            opponent.board[row][col] = 'X'  # Marca como impactado
            self.hits_board[row][col] = 'X'  # Marca en el tablero de impactos
            return True
        else:
            print(f"{self.name} falló el ataque en {row},{col}.")
            opponent.board[row][col] = 'O'  # Marca como agua
            self.hits_board[row][col] = 'O'  # Marca en el tablero de impactos
            return False

    def all_ships_sunk(self):
        return all(ship.hits == ship.size for ship in self.ships)

# Paso 4: Definir la Clase BattleshipGame
class BattleshipGame:
    def __init__(self):
        self.player1 = Player(input("Ingresa el nombre del Jugador 1: "))
        self.player2 = Player(input("Ingresa el nombre del Jugador 2: "))

    def play(self):
        for player in [self.player1, self.player2]:
            player.place_ships()
            player.print_board()

        current_player, opponent = self.player1, self.player2
        while True:
            print(f"Turno de {current_player.name}:")
            current_player.print_board()
            try:
                row = int(input("Fila a atacar (0-9): "))
                col = int(input("Columna a atacar (0-9): "))
                if 0 <= row < 10 and 0 <= col < 10:
                    current_player.attack(opponent, row, col)
                    if opponent.all_ships_sunk():
                        print(f"{current_player.name} ha ganado!")
                        break
                    current_player, opponent = opponent, current_player  # Cambia de turno
                else:
                    print("Posición fuera de rango, intenta de nuevo.")
            except ValueError:
                print("Entrada no válida, intenta de nuevo.")

# Paso 5: Ejecuta el Juego
if __name__ == "__main__":
    game = BattleshipGame()
    game.play()
