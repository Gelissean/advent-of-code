class Config:
    input_filename = "2023/6/input"

def get_list(line:str)->[int]:
    values = []
    built_number = 0
    for c in line:
        if c.isdigit():
            built_number = built_number * 10 + int(c)
        else:
            if built_number > 0:
                values.append(built_number)
            built_number = 0
    if built_number > 0:
        values.append(built_number)
    return values

def solve(times, distance):
    runs = []
    for i in range(len(times)):
        possibilities = []
        for j in range(1, times[i]):
            if j * (times[i] - j) > distance[i] :
                possibilities.append(j)
        runs.append(possibilities)
    prod = 1
    for run in runs:
        prod *= len(run)
    return prod


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        times = get_list(lines[0].split(':')[-1])
        distance = get_list(lines[1].split(':')[-1])
        print(solve(times, distance))
        times = get_list(lines[0].split(':')[-1].replace(' ', ''))
        distance = get_list(lines[1].split(':')[-1].replace(' ', ''))
        print(solve(times, distance))



if __name__ == "__main__":
    main()
