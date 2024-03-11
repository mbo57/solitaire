from term_printer import Color, cprint
import random


class Card():
    def __init__(self, mark, number, is_show=False):
        self.mark = mark
        self.number = number
        self.is_show = is_show

    def getMark(self):
        return self.mark

    def getNumber(self):
        return self.number

    def isShow(self):
        return self.is_show

    def getColor(self):
        if self.mark in {"Heart", "Diamond"}:
            return Color.RED
        elif self.mark in {"Club", "Spade"}:
            return Color.WHITE

    def getDisplayNum(self):
        if self.number == 1:
            return "A"
        elif self.number == 11:
            return "J"
        elif self.number == 12:
            return "Q"
        elif self.number == 13:
            return "K"
        else:
            return self.number

    def descCard(self):
        if self.isShow():
            cprint("{:>3s}".format(
                self.getMark()[0]+str(self.getDisplayNum())),
                attrs=[self.getColor()],
                end=""
            )
        else:
            cprint("XXX", attrs=[Color.BLUE], end="")


class Game():
    def __init__(self):
        self.deck = self.makeDeck()
        self.stack = {"Heart": [], "Diamond": [],
                      "Club": [], "Spade": []}

    def makeDeck(self):
        allcard = []
        for mark in ["Heart", "Diamond", "Club", "Spade"]:
            for num in range(13):
                allcard.append(Card(mark, num+1))
        random.shuffle(allcard)

        deck = [[] for i in range(8)]
        for i in range(8):
            for j in range(i + 3):
                card = allcard.pop()
                if j >= i:
                    card.is_show = True
                deck[i].append(card)
        return deck

    def makeDeckSort(self):
        allcard = []
        for mark in ["Heart", "Diamond", "Club", "Spade"]:
            for num in range(13):
                allcard.append(Card(mark, num+1))

        deck = [[] for i in range(8)]
        for i in range(8):
            for j in range(i + 3):
                card = allcard.pop()
                if j >= i:
                    card.is_show = True
                deck[i].append(card)
        return deck

    def describe(self):
        for cards in self.stack.values():
            if cards == []:
                print(end="   ")
            else:
                cards[-1].descCard()
            print(end=" ")
        print()

        max_length = max([len(i) for i in self.deck])
        for j in range(max_length+1):
            if j == 0:
                print(end="   ")
            else:
                print("{:>2d}".format(j-1), end=" ")
            for i in range(8):
                try:
                    if j == 0:
                        print("{:3d}".format(i), end="")
                    else:
                        card = self.deck[i][j-1]
                        card.descCard()
                    print(end=" ")
                except IndexError:
                    print("   ", end=" ")
            if j == 0:
                print(end="  ")
            else:
                print(j-1, end=" ")
            print()

    def move(self, from_point, to_point):
        if from_point[0] in {"Diamond", "Heart", "Spade", "Club"}:
            from_join_card = self.stack[from_point[0]].pop()
            self.deck[to_point].append(from_join_card)
            return
        if to_point == -1:
            card = self.deck[from_point[0]].pop()
            self.stack[card.getMark()].append(card)
            self.cardOpen(from_point[0])
            return
        from_remain_array = self.deck[from_point[0]][:from_point[1]]
        from_move_array = self.deck[from_point[0]][from_point[1]:]
        self.deck[from_point[0]] = from_remain_array
        self.deck[to_point] = self.deck[to_point] + from_move_array
        self.cardOpen(from_point[0])

    def cardOpen(self, from_col):
        try:
            end_card = self.deck[from_col][-1]
        except IndexError:
            return
        end_card.is_show = True

    def canMove(self, from_point, to_point):
        print(from_point, to_point)
        if from_point[0] in {"Diamond", "Heart", "Spade", "Club"}:
            from_join_card = self.stack[from_point[0]][-1]
        else:
            from_join_card = self.deck[from_point[0]][from_point[1]]
        if not from_join_card.isShow():
            return False

        if to_point == -1:
            if from_join_card != self.deck[from_point[0]][-1]:
                return False
            try:
                stack_card = self.stack[from_join_card.getMark()][-1]
            except IndexError:
                stack_card = None
            if stack_card is None \
                    or (stack_card.getMark() == from_join_card.getMark()
                        and stack_card.getNumber() + 1 == from_join_card.getNumber()):
                return True

        if self.deck[to_point] == [] and from_join_card.number == 13:
            return True

        to_join_card = self.deck[to_point][-1]
        if to_join_card.getColor() == from_join_card.getColor():
            return False
        if to_join_card.getNumber() - 1 == from_join_card.getNumber():
            return True
        return False

    def input(self):
        user_input = input(
            "Please Enter move point. ex) from_col from_row to_col:")
        split_ui = list(user_input.split())
        if len(split_ui) != 3:
            print("invalid input")
            return self.input()
        if split_ui[0] in {
            "D", "d", "Diamond",
            "H", "h", "Heart",
            "S", "s", "Spade",
            "C", "c", "Club"
        } and split_ui[1] == "-1" and self.isnum(split_ui[2]):
            mark = ""
            if split_ui[0] in {"D", "d", "Diamond"}:
                mark = "Diamond"
            elif split_ui[0] in {"H", "h", "Heart"}:
                mark = "Heart"
            elif split_ui[0] in {"S", "s", "Spade"}:
                mark = "Spade"
            elif split_ui[0] in {"C", "c", "Club"}:
                mark = "Club"
            return (mark, -1), int(split_ui[2])

        if not (self.isnum(split_ui[0])
                and self.isnum(split_ui[1])
                and self.isnum(split_ui[2])):
            print("invalid input: not number")
            return self.input()
        from_col = int(split_ui[0])
        from_row = int(split_ui[1])
        to_col = int(split_ui[2])
        if not (0 <= from_col < 8 and -1 <= to_col < 8):
            print("invalid input", from_col, to_col)
            return self.input()
        if self.deck[from_col] == [] \
                and not 0 <= from_row < len(self.deck[from_col]) - 1:
            print("invalid input")
            return self.input()
        return (from_col, from_row), to_col

    def isnum(self, a):
        try:
            int(a)
        except ValueError:
            return False
        return True

    def getStackEnd(self, mark):
        try:
            card = self.stack[mark][-1]
        except IndexError:
            card = None
        return card

    def endCheck(self):
        if self.getStackEnd("Heart") is not None\
                and self.getStackEnd("Club") is not None \
                and self.getStackEnd("Diamond") is not None \
                and self.getStackEnd("Spade") is not None \
                and self.getStackEnd("Heart").getNumber() == 13 \
                and self.getStackEnd("Club").getNumber() == 13 \
                and self.getStackEnd("Diamond").getNumber() == 13 \
                and self.getStackEnd("Spade").getNumber() == 13:
            return True
        else:
            return None

    def start(self):
        self.describe()
        while True:
            from_point, to_point = self.input()
            while not self.canMove(from_point, to_point):
                print("can not move")
                from_point, to_point = self.input()
            self.move(from_point, to_point)
            self.describe()
            if self.endCheck():
                print("Success")
                break


game = Game()
game.start()
