class Config:
    input_filename = "2023/2/input"
    red_max = 12
    green_max = 13
    blue_max = 14
    print_games = False


class Round:
    """Information about a single round of a game, initialized via part of an input line:\
        0 red, 0 blue, 0 green"""

    def __init__(self, line: str) -> None:
        self.red_dice = 0
        self.green_dice = 0
        self.blue_dice = 0
        self._parse_line(line.strip())

    def _parse_line(self, line: str) -> None:
        for setting in line.split(","):
            setting_parts = setting.strip().split(" ")
            value = int(setting_parts[0])
            color = setting_parts[-1].strip()
            if color == "red":
                self.red_dice = value
            elif color == "green":
                self.green_dice = value
            elif color == "blue":
                self.blue_dice = value
            else:
                raise Exception("invalid color")

    def __str__(self) -> str:
        return f"Round: {self.red_dice}R, {self.green_dice}G, {self.blue_dice}B"


class Game:
    """Object holding game data, initialize using line from input: \
    Game 0: 0 green, 0 red, 0 blue; 0 red; ..."""

    def __init__(self, line: str) -> None:
        parts = line.split(":")
        self.index = int(
            parts[0].split(" ")[-1].strip()
        )  # Game 123 split into ['Game','123'] and '123'>123
        self.legit = None
        # split remaining string into separate rounds
        self.rounds = [Round(part.strip()) for part in parts[-1].split(";")]
        self.r_req = 0
        self.g_req = 0
        self.b_req = 0
        self.power = 0
        self._validate()
        self._set_power()

    def _validate(self) -> None:
        """If any round of a game is not possible set legit to false"""
        for round in self.rounds:
            if (
                round.red_dice > Config.red_max
                or round.green_dice > Config.green_max
                or round.blue_dice > Config.blue_max
            ):
                self.legit = False
                return
        self.legit = True

    def _set_power(self) -> None:
        """Find minimal amount of dice to make game possible and multiply them"""
        for round in self.rounds:
            self.r_req = max(self.r_req, round.red_dice)
            self.g_req = max(self.g_req, round.green_dice)
            self.b_req = max(self.b_req, round.blue_dice)
        self.power = self.r_req * self.g_req * self.b_req

    def __str__(self) -> str:
        rounds = "".join([f"\n\t{round}" for round in self.rounds])
        return f"Game: {self.index} possible: {self.legit} power: {self.power} rounds: {rounds}"


def check_game(game: Game) -> bool:
    print(game) if Config.print_games else None
    return game.index if game.legit else 0, game.power


def parse_lines(lines: [str]) -> [bool]:
    games = [Game(line) for line in lines]
    index_legit, sets_of_power = [], []
    for game in games:
        i, p = check_game(game)
        index_legit.append(i)
        sets_of_power.append(p)
    return index_legit, sets_of_power


def main():
    with open(Config.input_filename, "r") as i:
        games, sets_power = parse_lines(i.readlines())
        print(games) if Config.print_games else None
        print(sum(games))
        print(sets_power) if Config.print_games else None
        print(sum(sets_power))


if __name__ == "__main__":
    main()
