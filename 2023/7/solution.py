class Config:
    input_filename = "2023/7/input"
    print_hands = False


class Hand:
    strengths = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    hand_strengths = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a kind",
        "Full house",
        "Four of a kind",
        "Five of a kind",
    ]

    def __init__(self, line) -> None:
        line_parts = line.strip().split(" ")
        self.bid = int(line_parts[-1])
        self.hand = None
        self.type = None
        self.hand_raw = line_parts[0]
        self.hand_array = []
        self.joker_value = 0
        self._assign_card_values(self.hand_raw)
        self._assign_hand_value()

    def _assign_card_values(self, hand: str) -> None:
        self.hand = {}
        for card in hand:
            if card in self.hand:
                self.hand[card] += 1
            else:
                self.hand[card] = 1
            self.hand_array.append(Hand.strengths.index(card))

    def _assign_hand_value(self) -> None:
        quantities = list(self.hand.values())
        quantities.sort(reverse=True)
        if len(quantities) == 0:  # all J
            quantities.append(5)
        else:
            quantities[0] += self.joker_value
        if quantities == [3, 2]:
            self.type = Hand.hand_strengths.index("Full house")
        elif quantities[0] == 5:
            self.type = Hand.hand_strengths.index("Five of a kind")
        elif quantities[0] == 4:
            self.type = Hand.hand_strengths.index("Four of a kind")
        elif quantities[0] == 3:
            self.type = Hand.hand_strengths.index("Three of a kind")
        elif quantities[0] == 2:
            if quantities[1] == 2:
                self.type = Hand.hand_strengths.index("Two Pair")
            else:
                self.type = Hand.hand_strengths.index("One Pair")
        else:
            self.type = Hand.hand_strengths.index("High Card")

    def __lt__(self, other):
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        if len(self.hand_array) != len(other.hand_array):
            raise Exception("Hands aren't equal size")
        for i in range(len(self.hand_array)):
            if self.hand_array[i] < other.hand_array[i]:
                return True
            if self.hand_array[i] > other.hand_array[i]:
                return False
        return False

    def __str__(self) -> str:
        return f"Hand: {self.hand_raw}, type strength: {self.type}"


class Hand2(Hand):
    strengths = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def _assign_card_values(self, hand: str) -> None:
        self.hand = {}
        for card in hand:
            if card == "J":
                self.joker_value += 1
            elif card in self.hand:
                self.hand[card] += 1
            else:
                self.hand[card] = 1
            self.hand_array.append(Hand2.strengths.index(card))


def main() -> None:
    with open(Config.input_filename) as i:
        lines = i.readlines()
        hands = [Hand(line) for line in lines]
        hands.sort()
        ranks = []
        for i in range(len(hands)):
           print(hands[i]) if Config.print_hands else None
           ranks.append((1 + i) * hands[i].bid)
        print(ranks) if Config.print_hands else None
        print(sum(ranks))
        hands2 = [Hand2(line) for line in lines]
        hands2.sort()
        ranks = []
        for i in range(len(hands2)):
            print(hands2[i]) if Config.print_hands else None
            ranks.append((1 + i) * hands2[i].bid)
        print(ranks) if Config.print_hands else None
        print(sum(ranks))


if __name__ == "__main__":
    main()
