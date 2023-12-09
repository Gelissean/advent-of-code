class Config:
    input_filename = "2023/9/input"


def main() -> None:
    lines = None
    with open(Config.input_filename) as i:
        lines = i.readlines()
    
    days = []
    for line in lines:
        history = [int(a) for a in line.strip().split()]
        days.append(history)
    results = []
    for i in range(len(days)):
        history = days[i]
        calc = [history]
        while 1:
            done = True
            row = calc[-1]
            for value in row:
                if value != 0:
                    done = False
            if done:break
            calc.append([row[j+1] - row[j] for j in range(len(row)-1)])
        result = 0
        print(calc)
        for row in calc[::-1]:
            result += row[-1]

        results.append(result)
    print(results)
    print(sum(results))



if __name__ == "__main__":
    main()
