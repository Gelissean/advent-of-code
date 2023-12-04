input_file = "2023/4/input"

def power(number:int, rank:int)->int:
    retval = 1
    for i in range(rank):
        retval *= number
    return retval

with open(input_file, 'r') as i:
    values = []
    for line in i.readlines():
        score = 0
        strings = line.replace(':', '|').split('|')
        winning_list = [int(s.strip()) for s in strings[1].strip().replace('  ', ' ').split(' ')]
        numbers = [int(s.strip()) for s in strings[2].replace('  ', ' ').strip().split(' ')]
        count = 0
        for win in winning_list:
            if win in numbers:
                count += 1
        score = 1 if count == 1 else power(2, count-1) if count > 1 else 0
        values.append(score)
    print(sum(values))
