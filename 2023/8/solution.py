class Config:
    input_filename = "2023/8/input"
    print_hands = False


class LoopElement:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def set_next_element(self, next_element) -> None:
        self.next = next_element


class Loop:
    def __init__(self, line: [str]) -> None:
        self.elements = []
        last_element: LoopElement = None
        for char in line.strip():
            if char not in ["L", "R"]:
                raise Exception(f"Invalid move: {char}")
            new_element = LoopElement(char)
            self.elements.append(new_element)
            last_element.set_next_element(
                new_element
            ) if last_element is not None else None
            new_element.set_next_element(self.elements[0])
            last_element = new_element
        self.pointer: LoopElement = self.elements[0] if len(self.elements) > 0 else None

    def get_move(self) -> str:
        value = self.pointer.value
        self.pointer = self.pointer.next
        return value


class MapTreeNode:
    left = 0
    right = 1
    def convert_direction(char:str)->int:
        if char == 'L':
            return MapTreeNode.left
        elif char == 'R':
            return MapTreeNode.right
        raise Exception(f'Invalid direction to translate: {char}')

    def __init__(self, index: str, left_node=None, right_node=None) -> None:
        self.index: str = index
        self.left_node = left_node
        self.right_node = right_node

    def assign(self, direction: int, tree_node) -> None:
        if direction == MapTreeNode.left:
            self.left_node = tree_node
        elif direction == MapTreeNode.right:
            self.right_node = tree_node
        else:
            raise Exception(f"Invalid direction: {direction}")

    def get_node(self, direction: int):
        if direction == MapTreeNode.left:
            return self.left_node
        elif direction == MapTreeNode.right:
            return self.right_node
        else:
            raise Exception(f"Invalid direction: {direction}")


class MapTree:
    def __init__(self) -> None:
        pass  # TODO tree creation


class CamelMap:
    def __init__(self, lines: [str]) -> None:
        self.movement = Loop(lines[0].strip())
        # self.map = MapTree(lines[2:])
        self.map = {}
        self.path = None
        for line in lines[2:]:
            parts = line.split("=")
            key = parts[0].strip()
            parts = parts[1].replace("(", "").replace(")", "").strip().split(",")
            self.map[key] = MapTreeNode(key, parts[0].strip(), parts[1].strip())
        # TODO traversal

    def get_path(self) -> [str]:
        if self.path == None:
            self._calculate_path()
        return self.path

    def _calculate_path(self, start='AAA', end='ZZZ') -> None:
        path = []
        location = start
        while location != end:
            direction = self.movement.get_move()
            path.append(direction)
            location = self.map[location].get_node(MapTreeNode.convert_direction(direction))
        self.path = path


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        camel_map = CamelMap(lines)
        print(camel_map.get_path())
        print(len(camel_map.get_path()))


if __name__ == "__main__":
    main()
