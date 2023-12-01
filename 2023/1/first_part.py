input_file = "2023/1/input"

with open(input_file, 'r') as i:
    values = []
    for line in i.readlines():
        first_set = False
        first = None
        last = None
        for c in line:
            if c in [str(digit) for digit in range(10)]:
                if not first_set:
                    first = ord(c) - ord('0')
                    first_set = True
                last = ord(c) - ord('0')
        values.append(first*10 + last)
    print(sum(values))
