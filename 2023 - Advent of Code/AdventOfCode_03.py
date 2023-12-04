'''
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
'''

schematic = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


def clean_schematic(text):
    filtered_schematic = text.replace(" ", "").replace("\n", "")
    return filtered_schematic


def build_schematic_list(text,row_width):
    clean_text = clean_schematic(text)
    schematic_list = [clean_text[i:i+row_width] for i in range(0, len(clean_text), row_width)]
    return schematic_list

def is_valid_position(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def get_adjacent_numbers(schematic, row, col):
    rows, cols = len(schematic), len(schematic[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    adjacent_numbers = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(new_row, new_col, rows, cols) and schematic[new_row][new_col].isdigit():
            adjacent_numbers.append(int(schematic[new_row][new_col]))

    return adjacent_numbers

def sum_of_adjacent_numbers(schematic):
    rows, cols = len(schematic), len(schematic[0])
    total_sum = 0

    for row in range(rows):
        for col in range(cols):
            if schematic[row][col].isdigit():
                adjacent_numbers = get_adjacent_numbers(schematic, row, col)
                total_sum += int(schematic[row][col]) + sum(adjacent_numbers)

    return total_sum


result = sum_of_adjacent_numbers(build_schematic_list(schematic,10))
print(result)