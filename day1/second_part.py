input_file = "day1/input"


def replace_words(line: str) -> str:
    strings = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    for i in range(len(strings)):
        done = False
        while not done:
            value = line.find(strings[i])
            if value == -1:
                done = True
            else:
                # place new character after first character to break the digit string,
                # while letting first character of digit be the last of previous
                line = line[: value + 1] + str(i) + line[value + 1 :]
    return line


def get_first_last_in_line(line: str):
    line = replace_words(line)
    first_set = False
    first = None
    last = None
    for c in line:
        if c in [str(digit) for digit in range(10)]:
            if not first_set:
                first = ord(c) - ord("0")
                first_set = True
            last = ord(c) - ord("0")
    return first, last


def get_first_last(lines: [str]) -> []:
    values = []
    for line in lines:
        first, last = get_first_last_in_line(line)
        values.append(first * 10 + last)
    return values


with open(input_file, "r") as i:
    values = get_first_last(i.readlines())
    print(sum(values))

