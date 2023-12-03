class Config:
    input_filename='2015/2/input'

def main():
    areas = []
    with open(Config.input_filename, 'r') as i:
        for line in i.readlines():
            dimensions = line.split('x')
            l, w, h = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
            area_array = [l*w, w*h, h*l]
            areas.append(sum([2*area for area in area_array]) + min(area_array))
    print(sum(areas))


if __name__ == '__main__':
    main()