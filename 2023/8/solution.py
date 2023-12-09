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
    
    def reset(self)->None:
        self.pointer = self.elements[0] if len(self.elements) > 0 else None


class MapTreeNode:
    left = 0
    right = 1

    def convert_direction(char: str) -> int:
        if char == "L":
            return MapTreeNode.left
        elif char == "R":
            return MapTreeNode.right
        raise Exception(f"Invalid direction to translate: {char}")

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

    def get_path(self, start="AAA", end="ZZZ") -> [str]:
        if self.path == None:
            self._calculate_path(start, end)
        return self.path

    def _calculate_path(self, start="AAA", end="ZZZ") -> None:
        if start not in self.map:
            raise Exception(f"Invalid start location: {start}")
        path = []
        location = start
        while location != end:
            direction = self.movement.get_move()
            path.append(direction)
            location = self.map[location].get_node(
                MapTreeNode.convert_direction(direction)
            )
            if len(path) > 50000:
                raise Exception("impossible to get there")
        self.path = path

    def get_cyclic_path(self, start="AAA", end="ZZZ") -> [str]:
        if start not in self.map:
            raise Exception(f"Invalid start location: {start}")
        self.movement.reset()
        location = start
        steps = []
        step_counter = 0
        while len(steps) != 10:
            if location == end:
                steps.append(step_counter)
            direction = self.movement.get_move()
            location = self.map[location].get_node(
                MapTreeNode.convert_direction(direction)
            )
            if step_counter > 50000 + (steps[-1] if len(steps) > 0 else 0):
                if len(steps) == 0:
                    raise Exception("impossible to get there")
                else:
                    return steps
            step_counter += 1
        return steps


class CamelMap2(CamelMap):
    def _calculate_path(self, start="A", end="Z") -> None:
        paths = []
        for location in self.map.keys():
            if location[-1] == start:
                paths.append(location)
        step_count = 0
        while 1:
            if step_count > 100000:
                raise Exception("Too many steps")
            direction = self.movement.get_move()
            finished = True
            for i in range(len(paths)):
                if paths[i][-1] != end and finished:
                    finished = False
                    break
            if finished:
                break
            step_count += 1
            for i in range(len(paths)):
                paths[i] = self.map[paths[i]].get_node(
                    MapTreeNode.convert_direction(direction)
                )
        self.path = step_count


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        try:
            camel_map = CamelMap(lines)
            # print(camel_map.get_path())
            print(len(camel_map.get_path()))
        except:
            pass

        # camel_map2 = CamelMap2(lines)
        # print(camel_map2.get_path())

class SolverElement():
    def __init__(self, offset, loop_size, index=0) -> None:
        self.offset = offset
        self.loop_size = loop_size
        self.multiplicative = index

    def increase(self)->None:
        self.multiplicative += 1

    def get_value(self):
        return self.offset + self.loop_size*self.multiplicative

def prod(list:[int])->int:
    result = 1
    for value in list:
        result *= value
    return result

def main2() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        camel_map = CamelMap(lines)
        starts = []
        ends = []
        for key in camel_map.map.keys():
            starts.append(key) if key[-1] == "A" else None
            ends.append(key) if key[-1] == "Z" else None
        lengths = []
        for i in range(len(starts)):
            for j in range(len(ends)):
                camel_map.path = None
                try:
                    lengths.append(camel_map.get_cyclic_path(starts[i], ends[j]))
                    print(f"{starts[i]}>{ends[j]}: {lengths[-1]}")
                except:
                    pass  # print(f"{starts[i]}>{ends[j]}: impossible")
        loop_sizes = []
        offsets = []
        for route in lengths:
            offsets.append(route[0])
            loop_sizes.append(route[1] - route[0])
            if loop_sizes[-1] != route[2] - route[1]:
                raise Exception("Not a cyclic loop")
        print(offsets)
        print(loop_sizes)
        maths = ' = '.join([f"{offsets[i]} + {loop_sizes[i]}*{chr(ord('a')+i)}" for i in range(len(offsets))])
        steps = 0
        result = None
        routes = [SolverElement(offsets[i], loop_sizes[i]) for i in range(len(offsets))]
        number_of_routes = len(routes)
        if False not in [offsets[i] == loop_sizes[i] for i in range(number_of_routes)]:
            primes = []
            for number in offsets:
                for i in range(2, number):
                    if number % i == 0:
                        number = number // i
                        if i not in primes:
                            primes.append(i)
            print(prod(primes))
            return

        counter = 0
        while steps < 100000000:
            # first check if they are equal
            solved = True
            for i in range(number_of_routes-1):
                if routes[i].get_value() != routes[i+1].get_value():
                    solved=False
                    break
            if solved:
                result = routes[0].get_value()
                break
            # increase first number and adjust rest
            routes[0].increase()
            target_value = routes[0].get_value()
            for i in range(1, number_of_routes):
                while routes[i].get_value() < target_value:
                    routes[i].increase()
            steps += 1
            # 
        print([route.get_value() for route in routes])
        if result == None:
            raise Exception("unsolvable")
        print(result)



if __name__ == "__main__":
    main()
    main2()
