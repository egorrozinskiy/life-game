# life-game

import itertools

# возвращает список списков, в котором лежат координаты живых клеток (помечены единицами), нулями помечены мертвые
def get_board(size, alive_coords):
    return [[1 if (i, j) in alive_coords else 0
             for j in range(size)]
            for i in range(size)]

# по координате клетки ищем ее соседей
def get_neighbors(coord):
    x, y = coord
    neighbors = [(x + i, y + j)
                 for i in range(-1, 2) # соседей ищем в данной окрестности
                 for j in range(-1, 2)
                 if not i == j == 0]
    return neighbors

# у данной клетки считаем количество живых соседей
def calculate_alive_neighbors(coord, alive_coords):
    return len(list(filter(lambda x: x in alive_coords,
                      get_neighbors(coord))))

# проверяет, жива ли будет клетка с данными координатами на следующем ходу (второй параметр это доска)
def is_alive_coord(coord, alive_coords):
    alive_neighbors = calculate_alive_neighbors(coord, alive_coords)
    if (alive_neighbors == 3 or
            (alive_neighbors == 2 and coord in alive_coords)):
        return True
    return False

# преобразует клетки доски к новому(следующему) состоянию
def new_step(alive_coords):
    board = itertools.chain(*map(get_neighbors, alive_coords)) # тут применяем функцию get_neighbors к каждому элементу списка живых клеток и записываем это в формате координат клеток для доски
    new_board = set([coord                                      # тут у нас новая доска
                     for coord in board                         # она образуется с помощью функции создания множества (set) из координат клеток
                     if is_alive_coord(coord, alive_coords)])   # которые отбираются по правилу: берем все живые координаты клеток на доске
    return list(new_board)

# проверяет корректность координат клетки (должны укладываться в размер доски)
def is_correct_coord(size, coord):
    x, y = coord
    return all(0 <= coord <= size - 1 for coord in [x, y])

# отбрасываем все некорректные координаты клетки
def correct_coords(size, coords):
    return list(filter(lambda x: is_correct_coord(size, x), coords))

#функция для печати доски
def print_board(board):
    for line in board:
        print(line)
    print()


def main():
    board = []
    # считываем из файла начальное состояние поля
    with open('board.txt', 'r') as f:
        size = int(f.readline())
        for line in f:
            board.append(tuple(map(int, line.split())))

    print_board(get_board(size, board)) # выводим на экран начальную доску
    for _ in range(5): #выводим только 5 шагов игры!
        board = correct_coords(size, new_step(board))
        print_board(get_board(size, board))


if __name__ == '__main__':
    main()
