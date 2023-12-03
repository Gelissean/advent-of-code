class Config:
    input_filename = "2023/3/input"
    x_size = None
    y_size = None
    null_characters = ["."]
    masking_character = "x"


class Cell:
    pass


class Part:
    def __init__(self, cells: [Cell]) -> None:
        self.numbers = []
        self.positions = []
        self.valid = False
        self.cells = cells

    def assign_number(self, number: int, position: tuple) -> None:
        self.numbers.append(number)
        self.positions.append(position)

    def set_validity(self, validity: bool) -> None:
        self.valid = validity

    def get_value(self) -> int:
        return sum(self.numbers) * self.valid

    def __str__(self) -> str:
        return f"Part: {'valid' if self.valid else 'invalid'} | numbers : {self.numbers}, pos:{self.positions}"


class Cell:
    """Identifies whether a cell belongs to a part or not"""

    def __init__(self, character: str, position: [int]) -> None:
        self.character = character
        self.part = None
        self.x = position[0]
        self.y = position[1]
        self.surrounding = []

    def assign_surrounding(self, surrounding: [Cell]):
        self.surrounding = surrounding

    def assign_part(self, part: Part) -> None:
        self.part = part

    def __str__(self) -> str:
        return f"Cell: {self.character} - part of {self.part} at {self.x};{self.y}"


class Grid:
    """Data about the grid within the problem"""

    def __init__(self, grid_string: str) -> None:
        self.y_size = len(grid_string)
        self.x_size = len(grid_string[0].strip()) if self.y_size != 0 else 0
        if self.x_size == 0:
            raise Exception("Invalid input string")
        self._build_grid(grid_string)
        self.parts = []
        self._check_for_parts()

    def grid_map(self) -> str:
        table = []
        for row in self.grid:
            row_array = []
            for cell in row:
                row_array.append(
                    " "
                    if cell.part == None
                    else Config.masking_character
                    if not cell.part.valid
                    else cell.character
                )
            table.append("".join(row_array))
        return "\n".join(table)

    def _get_offsets(self, pos: int, size: int) -> [int]:
        if pos == 0:
            return [0, 1]
        elif pos == size - 1:
            return [-1, 0]
        return [-1, 0, 1]

    def _build_grid(self, grid_string: str) -> None:
        self.grid = [
            [
                Cell(grid_string[row_index][column_index], [column_index, row_index])
                for column_index in range(self.x_size)
            ]
            for row_index in range(self.y_size)
        ]
        for x in range(self.x_size):
            for y in range(self.y_size):
                x_offsets = self._get_offsets(x, self.x_size)
                y_offsets = self._get_offsets(y, self.y_size)
                cells = []
                for x_offset in x_offsets:
                    for y_offset in y_offsets:
                        if x_offset == 0 and y_offset == 0:
                            continue
                        cells.append(self.grid[y + y_offset][x + x_offset])
                self.grid[y][x].assign_surrounding(cells)

    def _check_for_parts(self) -> None:
        is_building_number = False
        building_part = None
        built_number = 0
        number_start_x_pos = None
        for row_index in range(self.y_size):
            # if building a number and go over the next row, end the number
            if is_building_number and building_part is not None:
                building_part.assign_number(
                    built_number, (number_start_x_pos, row_index - 1)
                )
                is_building_number = False
                building_part = None
                built_number = 0
                number_start_x_pos = None
            for column_index in range(self.x_size):
                cell = self.grid[row_index][column_index]
                c = cell.character  # character
                if (
                    c in Config.null_characters
                ):  # either do nothing or finish last built number and add it to the built part
                    if is_building_number and building_part is not None:
                        building_part.assign_number(
                            built_number, (number_start_x_pos, row_index)
                        )
                        is_building_number = False
                        building_part = None
                        built_number = 0
                        number_start_x_pos = None
                    continue
                # if its not empty its a part
                if cell.part == None:
                    cell.part = self._make_part(cell)
                    self.parts.append(cell.part)
                building_part = cell.part
                # check if its a number or a special symbol
                if c.isdigit():
                    # if it is a digit then we know we're building a number
                    if not is_building_number:
                        number_start_x_pos = column_index
                    is_building_number = True
                    built_number = 10 * built_number + ord(c) - ord("0")
                else:
                    # is special symbol
                    building_part.set_validity(True)
                    # if we have a special number and were building a number 12*34
                    if is_building_number and building_part is not None:
                        building_part.assign_number(
                            built_number, (number_start_x_pos, row_index)
                        )
                        is_building_number = False
                        building_part = None
                        built_number = 0
                        number_start_x_pos = None

    def _make_part(self, cell: Cell) -> Part:
        done = False
        last_surrounding_cells = None
        surrounding_cells = cell.surrounding
        part_cells = [cell]
        while not done:
            if surrounding_cells == last_surrounding_cells:
                done = True
                break
            last_surrounding_cells = [
                i for i in surrounding_cells if i not in part_cells
            ]
            for surrounding_cell in last_surrounding_cells:
                if surrounding_cell.character not in Config.null_characters:
                    part_cells.append(surrounding_cell)
                    surrounding_cells += surrounding_cell.surrounding
            surrounding_cells = [i for i in surrounding_cells if i not in part_cells]
        part = Part(part_cells)
        for cell in part_cells:
            cell.part = part
        return part


class Problem:
    """Contains data regarding the problem itself"""

    def __init__(self, grid_string: str) -> None:
        self.grid = Grid(grid_string)


def main():
    with open(Config.input_filename) as i:
        p = Problem(i.readlines())
        map = p.grid.grid_map()
        print(map)
        with open("output", "w") as o:
            o.write(map)
        print(f"Number of parts: {len(p.grid.parts)}")
        print("--------")
        print("Printing out parts:")
        for part in p.grid.parts:
            print(part)
        print("--------")
        legit_parts = []
        for part in p.grid.parts:
            legit_parts.append(part) if part.valid else None
        print(f"Legit parts: {len(legit_parts)}")
        part_values = [part.get_value() for part in p.grid.parts]
        print(sum(part_values))


if __name__ == "__main__":
    main()
