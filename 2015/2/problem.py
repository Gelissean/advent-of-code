class Config:
    input_filename='2015/2/input'

def prod(list:[int]) -> int:
    retval = 1
    for element in list:
        retval *= element
    return retval

def main():
    areas = []
    ribbons = []
    with open(Config.input_filename, 'r') as i:
        for line in i.readlines():
            dimensions = line.split('x')
            l, w, h = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
            sides = [l, w, h]
            sides.sort()
            sides = sides
            area_array = [l*w, w*h, h*l]
            areas.append(sum([2*area for area in area_array]) + min(area_array))
            ribbons.append(prod(sides)+2*sum(sides[:-1]))
    print(sum(areas))
    print(sum(ribbons))


if __name__ == '__main__':
    main()