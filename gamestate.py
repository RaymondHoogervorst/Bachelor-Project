from random import randint, choice
import sys

SIZE = 6

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def get_bit(value, bit):
    return (value>>bit) & 1 == 1

def horizontal_range(i):
    return range(SIZE * i, SIZE * i + SIZE, 1)

def vertical_range(i):
    return range(i, SIZE * SIZE, SIZE)

def mask_to_str(value):
    res = ""
    for i in range(SIZE):
        for bit in range(SIZE * i, SIZE * i + SIZE, 1):
            bit = '1' if (get_bit(value, bit)) else '.'
            res += str(bit)
        res += '\n'

    return res

class GameCluster:
    def __init__(self, horizontal, vertical):
        self.horizontal_types = horizontal
        self.vertical_types = vertical

class GameState:

    @property
    def code(self):

        str = ['o'] * 36
        char = 'A'

        def add_line(range, linetype, bitmask):
            nonlocal char
            curr_size = 0
            j = 0
            for pos in range:
                if not get_bit(bitmask, pos):
                    continue
                str[pos] = char
                curr_size += 1
                if curr_size == linetype[j]:
                    j += 1
                    char = chr(ord(char) + 1)
                    curr_size = 0



        for i in range(SIZE):
            add_line(horizontal_range(i), self.cluster.horizontal_types[i], self.horizontal_bitmask)

        for i in range(SIZE):
            add_line(vertical_range(i), self.cluster.vertical_types[i], self.vertical_bitmask)

        return ''.join(str)

    def __init__(self, cluster, horizontal, vertical):
        self.cluster = cluster
        self.horizontal_bitmask = horizontal
        self.vertical_bitmask = vertical

    def __str__(self):
        code = self.code
        return '\n'.join(code[i:i + SIZE] for i in range(0, len(code), SIZE))

    @classmethod
    def __parse_line(cls, string, value, positions):
        last_char = None
        streak_positions = []
        line_type = []

        def set_bits(value):
            if len(streak_positions) <= 1 or last_char == 'o':
                return value
            line_type.append(len(streak_positions))
            for bit in streak_positions:
                value = set_bit(value, bit)
            return value

        for pos in positions:
            char = string[pos]

            if char == last_char:
                streak_positions.append(pos)
            else:
                value = set_bits(value)
                streak_positions = [pos]
                last_char = char
        value = set_bits(value)

        return (line_type, value)   

    @classmethod
    def parse(cls, string):
        horizontal_types = []
        vertical_types = []

        horizontal_bitmask = 0
        vertical_bitmask = 0

        for i in range(SIZE):
            # horiziontal
            (type, horizontal_bitmask) = cls.__parse_line(string, horizontal_bitmask, horizontal_range(i))
            horizontal_types.append(type)

            # vertical
            (type, vertical_bitmask) = cls.__parse_line(string, vertical_bitmask, vertical_range(i))
            vertical_types.append(type)
        
        return GameState(GameCluster(horizontal_types, vertical_types), horizontal_bitmask, vertical_bitmask)

    def get_next_line_moves(self, i, ver_not_hor = False):
        positions = list(horizontal_range(i) if ver_not_hor else vertical_range(i))

        if ver_not_hor:
            positions = vertical_range(i)
            main_axis = self.vertical_bitmask
            cross_axis = self.horizontal_bitmask
            type = self.cluster.vertical_types[i]
            get_move = lambda new_main_axis : GameState(self.cluster, cross_axis, new_main_axis)
        else:
            positions = horizontal_range(i)
            main_axis = self.horizontal_bitmask
            cross_axis = self.vertical_bitmask
            type = self.cluster.horizontal_types[i]
            get_move = lambda new_main_axis :  GameState(self.cluster, new_main_axis, cross_axis)

        positions = list(positions)
        next_moves = []
        last_wall_i = -1
        i = 0
        length_i = 0

        while i < SIZE:
            if length_i == len(type):
                break

            pos = positions[i]
            cross_bit = get_bit(cross_axis, pos)
            main_bit = get_bit(main_axis, pos)

            if cross_bit:
                last_wall_i = i
            if not main_bit or cross_bit:
                i += 1
                continue

            length = type[length_i]
            length_i += 1

            base = main_axis
            for j in range(i, i + length):
                base = clear_bit(base, positions[j])

            place_i = last_wall_i + 1
            while(place_i < SIZE - length + 1 and not get_bit(base | cross_axis, positions[place_i + length - 1])):
                if place_i == i:
                    place_i += 1
                    continue
                pos = positions[place_i]
                move = base
                for j in range(place_i, place_i + length):
                    move = set_bit(move, positions[j])
                next_moves.append(move)
                place_i += 1

            last_wall_i = i + length - 1

            i = last_wall_i + 1

        return map(get_move, next_moves)

    def get_next_moves(self):
        moves = []
        for i in range(SIZE):
            moves += self.get_next_line_moves(i, True)
            moves += self.get_next_line_moves(i, False)
        return moves

    def get_random_next_move(self, seen = set()):
        def get_line_at_index(index):
            return self.get_next_line_moves(index // 2, index % 2)

        modulo = SIZE * 2
        begin_i = randint(0, SIZE * 2 - 1)
        for offset in range(12):
            curr_i = (begin_i + offset) % modulo
            moves = list(filter(lambda state : state.hash not in seen, get_line_at_index(curr_i)))
            try:
                return choice(moves)
            except IndexError:
                curr_i = (curr_i + 1) % modulo
        return None
    
    def __gt__(self, other):
        return self.score > other.score

    @property
    def won(self):
        return get_bit(self.horizontal_bitmask, 17)
    
    @property
    def hash(self):
        return (self.horizontal_bitmask, self.vertical_bitmask)

# string = \
# "oooooB" \
# "oooooB" \
# "AAoooB" \
# "oooDoo" \
# "oooDoo" \
# "oooDCC"

# state = GameState.parse(string)

# def heuristic_input(state):
#     print(state)
#     score = int(input("Enter a score for this game state: "))
#     return score

def n_blocking_base(state):
    score = 0
    for i in horizontal_range(2)[::-1]:
        if get_bit(state.horizontal_bitmask, i):
            break
        score += get_bit(state.vertical_bitmask, i)
    # print((state, score))
    return score

def n_blocking_recursive(state):
    def inner(line, seen, blocked):
        if get_bit(seen, line):
            return 1
        
        seen = set_bit(seen, line)

        ver_not_hor = line & 1
        index = line // 2

        line_type = (state.cluster.vertical_types if ver_not_hor else state.cluster.horizontal_types)[index]

        main_axis = state.vertical_bitmask if ver_not_hor else state.horizontal_bitmask
        cross_axis = state.horizontal_bitmask if ver_not_hor else state.vertical_bitmask
        range = (vertical_range if ver_not_hor else horizontal_range)(index)

        car_i = 0
        car_c = 0
        for i in range[:blocked + 1]:
            if car_c == line_type[car_i]:
                car_i += 1
                car_c = 0
            car_c += get_bit(main_axis, i)

        car_len = line_type[car_i]
        pos_move = car_c
        neg_move = car_len - car_c + 1

        neg_sum = 0
        pos_sum = 0

        i = blocked
        while neg_move and i:
            i -= 1
            bit = range[i]
            main = get_bit(main_axis, bit)
            cross = get_bit(cross_axis, bit)
            if cross:
                cost = inner(2 * i + 1 - ver_not_hor, seen, index)
                if cost == None:
                    neg_sum = None
                    break
                neg_sum += cost

            neg_move -= (not main)
        if neg_move:
            neg_sum = None

        i = blocked
        while pos_move and i < SIZE - 1:
            i += 1
            bit = range[i]
            main = get_bit(main_axis, bit)
            cross = get_bit(cross_axis, bit)
            if cross:
                cost = inner(2 * i + 1 - ver_not_hor, seen, index)
                if cost == None:
                    pos_sum = None
                    break
                pos_sum += cost

            pos_move -= (not main)
        if pos_move:
            pos_sum = None



        if neg_sum == None:
            min_sum = pos_sum
        elif pos_sum == None:
            min_sum = neg_sum
        else:
            min_sum = min(pos_sum, neg_sum)

        return 1 + min_sum if min_sum != None else None

    blocking = []
    for index, i in enumerate(horizontal_range(2)[::-1]):
        if get_bit(state.horizontal_bitmask, i):
            break
        if get_bit(state.vertical_bitmask, i):
            blocking.append(2 * (SIZE - index) - 1)

    sum = 1
    for col in blocking:
        score = inner(col, 1 << 4, 2)
        if not score:
            return sys.maxsize
        sum += score

    return sum
    


# final = beam_search_curry(40, n_blocking_base)(state)
# print(final)
