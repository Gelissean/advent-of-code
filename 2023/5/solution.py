class Config:
    input_filename = "2023/5/input"
    print_location_strings = False
    print_progress = True


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
        self._get_seeds(line.split(":")[-1].strip())
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

    def _get_seeds(self, seed_line: str) -> None:
        self.seeds = [int(seed) for seed in seed_line.split(" ")]

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
            self.destination, self.source, self.size = numbers

    def _mapping_function(self, key: str, line: str) -> None:
        subject = self.__getattribute__(key)
        subject[len(subject.keys())] = AlmanacCacheLess.Numbers([int(number) for number in line.split(' ')])

    def find(self, seed: int) -> int:
        values = []
        for i in range(len(AlmanacCacheLess.subjects.keys())):
            subject = self.__getattribute__(
                AlmanacCacheLess.subjects[list(AlmanacCacheLess.subjects.keys())[i]]
            )
            if len(values) == 0:
                values.append(self._get_value(seed, subject))
            else:
                values.append(self._get_value(values[-1], subject))
        print(
            self._format_output(seed, values)
        ) if AlmanacCacheLess.is_printing else None
        return values[-1]

    def _get_value(self, input_value: int, subject: dict) -> int:
        value = input_value
        for key in subject.keys():
            numbers: AlmanacCacheLess.Numbers = subject[key]
            offset = input_value - numbers.source
            if offset >= 0 and offset < numbers.size:
                return numbers.destination + offset
        return value


class AlmanacCacheLessSeedRange(AlmanacCacheLess):
    is_printing_progress = Config.print_progress

    class SeedRange:
        def __init__(self, seed_source, seed_size) -> None:
            self.source = seed_source
            self.size = seed_size

    def _get_seeds(self, seed_line: str) -> None:
        seed_line_parts = seed_line.split(" ")
        while len(seed_line_parts) >= 2:
            source, size = int(seed_line_parts.pop(0)), int(seed_line_parts.pop(0))
            self.seeds.append(AlmanacCacheLessSeedRange.SeedRange(source, size))

    def get_closest_seed(self) -> int:
        min_loc = 999999999
        for seed in self.seeds:
            min_loc = min(min_loc, self.find(seed))
        return min_loc

    def __init__(self, lines: [str]) -> None:
        super().__init__(lines)
        self._intersect_ranges()

    def _intersect_ranges(self) -> None: # TODO
        subjects = ["seeds"] + [
            AlmanacCacheLessSeedRange.subjects[key]
            for key in AlmanacCacheLessSeedRange.subjects.keys()
        ]
        subjects = subjects[::-1]
        previous_subject: dict = None
        actual_subject: dict = None
        for subject in subjects:
            # seeds is a list, not a dict, has to be converted
            if subject == 'seeds':
                actual_subject = {}
                for i in range(len(self.__getattribute__(subject))):
                    s_r:AlmanacCacheLessSeedRange.SeedRange = self.__getattribute__(subject)[i]
                    actual_subject[i] = AlmanacCacheLessSeedRange.Numbers([s_r.source, s_r.source, s_r.size])
            else:
                actual_subject = self.__getattribute__(subject)
            if previous_subject != None:
                # do the intersection
                # 15 - 51 cuts into 50 - 97 and splits it into 50 - 51 and 52 - 97
                # 52 - 53 doesnt cut into 50 - 97 / 52-97
                for prev_key in previous_subject.keys():
                    prev_range: AlmanacCacheLessSeedRange.Numbers = previous_subject[
                        prev_key
                    ]
                    new_ranges = []
                    pop_ranges = []
                    for actual_key in actual_subject.keys():
                        actual_range: AlmanacCacheLessSeedRange.Numbers = (
                            actual_subject[actual_key]
                        )
                        # 5-10 to 7-12 intersects
                        # 5-12 to 7-12 covers (ignore)
                        # 7-15 to 7-12 covers (ignore)
                        # 7-12 to 7-12 covers (ignore)
                        # 10-15 to 7-12 intersects but can be ignored,
                        # only lower number from interval needs to be checked
                        if (
                            prev_range.source < actual_range.destination
                            and prev_range.source + prev_range.size - 1
                            >= actual_range.destination
                            and prev_range.source + prev_range.size - 1
                            < actual_range.destination + actual_range.size - 1
                        ):
                            pivot_point = prev_range.source + prev_range.size
                            smaller_size = pivot_point - actual_range.source
                            smaller_range = AlmanacCacheLessSeedRange.Numbers(
                                [
                                    actual_range.destination,
                                    actual_range.source,
                                    smaller_size,
                                ]
                            )
                            larger_range = AlmanacCacheLessSeedRange.Numbers(
                                [
                                    actual_range.destination + smaller_size,
                                    actual_range.source + smaller_size,
                                    actual_range.size - smaller_size,
                                ]
                            )
                            pop_ranges.append(actual_key)
                            last_index = list(actual_subject.keys())[-1]
                            new_ranges.append([last_index + 1, smaller_range])
                            new_ranges.append([last_index + 2, larger_range])
                    for new_range in new_ranges:
                        index, number_range = new_range
                        actual_subject[index] = number_range
                    for index in pop_ranges:
                        actual_subject.pop(index)
            previous_subject = actual_subject
        self.seeds = [actual_subject[key].source for key in actual_subject.keys()]
        print(subjects)
        print(self.seeds)


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        almanac = AlmanacCacheLess(lines.copy())
        locations = []
        for seed in almanac.seeds:
            locations.append(almanac.find(seed))
        print(min(locations))

        almanac2 = AlmanacCacheLessSeedRange(lines)
        # print(almanac2.get_closest_seed())


if __name__ == "__main__":
    main()
