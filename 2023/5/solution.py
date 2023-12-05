class Config:
    input_filename = "2023/5/input"
    print_location_strings = True


class Almanac:
    subjects = {
        "seed-to-soil map:": "soil_map",
        "soil-to-fertilizer map:": "fertilizer_map",
        "fertilizer-to-water map:": "water_map",
        "water-to-light map:": "light_map",
        "light-to-temperature map:": "temperature_map",
        "temperature-to-humidity map:": "humidity_map",
        "humidity-to-location map:": "location_map",
    }
    is_printing = Config.print_location_strings

    def __init__(self, lines: [str]) -> None:
        self.seeds = []
        self.soil_map = {}
        self.fertilizer_map = {}
        self.water_map = {}
        self.light_map = {}
        self.temperature_map = {}
        self.humidity_map = {}
        self.location_map = {}
        self.highest_seed = 0
        self._evaluate(lines)

    def _evaluate(self, lines: [str]) -> None:
        line = lines.pop(0)
        self.seeds = [int(seed) for seed in line.split(":")[-1].strip().split(" ")]
        subject = None
        for line in lines:
            line = line.strip()
            if len(line) == 0:  # empty line or \n
                continue
            elif line in Almanac.subjects:
                subject = Almanac.subjects[line]
            elif subject is None:
                raise Exception(
                    f"Evaluation exception: can't assign to a subject: {line}"
                )
            else:
                self._mapping_function(subject, line)

    def _mapping_function(self, key: str, line: str) -> None:
        destination, source, size = [int(v) for v in line.split(" ")]
        for offset in range(size):
            if source + offset in self.__getattribute__(key):
                raise Exception(f"Value already pre-defined: {key} - {source + offset}")
            self.__getattribute__(key)[source + offset] = destination + offset
        return

    def find(self, seed: int) -> int:
        values = []
        for i in range(len(Almanac.subjects.keys())):
            subject = self.__getattribute__(
                Almanac.subjects[list(Almanac.subjects.keys())[i]]
            )
            if len(values) == 0:
                values.append(seed if seed not in subject else subject[seed])
            else:
                values.append(
                    values[-1] if values[-1] not in subject else subject[values[-1]]
                )
        print(self._format_output(seed, values)) if Almanac.is_printing else None
        return values[-1]

    def _format_output(self, seed: int, values: [int]) -> str:
        return f"Seed {seed}, soil {values[0]}, fertilizer {values[1]}, water {values[2]}, light {values[3]}, temperature {values[4]}, humidity {values[5]}, location {values[6]}"


class AlmanacCacheLess(Almanac):
    class Numbers:
        def __init__(self, numbers: [int]) -> None:
            self.destination, self.source, self.size = [
                int(number) for number in numbers.split(' ')
            ]

    def _mapping_function(self, key: str, line: str) -> None:
        subject = self.__getattribute__(key)
        subject[len(subject.keys())] = AlmanacCacheLess.Numbers(line)

    def find(self, seed: int) -> int:
        values = []
        for i in range(len(Almanac.subjects.keys())):
            subject = self.__getattribute__(
                Almanac.subjects[list(Almanac.subjects.keys())[i]]
            )
            if len(values) == 0:
                values.append(self._get_value(seed, subject))
            else:
                values.append(self._get_value(values[-1], subject))
        print(self._format_output(seed, values)) if Almanac.is_printing else None
        return values[-1]

    def _get_value(self, input_value: int, subject: dict) -> int:
        value = input_value
        for key in subject.keys():
            numbers: AlmanacCacheLess.Numbers = subject[key]
            offset = input_value - numbers.source
            if offset >= 0 and offset < numbers.size:
                return numbers.destination + offset
        return value


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        almanac = AlmanacCacheLess(lines)
        locations = []
        for seed in almanac.seeds:
            locations.append(almanac.find(seed))
        print(min(locations))


if __name__ == "__main__":
    main()
