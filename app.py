import random


class Utilities:
    @staticmethod
    def sanitize_yn(question):
        ch = input(question + " (y/n): ").lower()
        while ch not in ["y", "n"]:
            ch = input(
                "Please input 'y' or 'n'. " +
                question +
                " (y/n): ").lower()
        return ch

    @staticmethod
    def sanitize_number(question, border):
        am = input(question + " ")
        while not am.isdigit():
            am = input("Not a number. " + question + " ")
        am = int(am)
        while am > border or am < 0:
            if am > border:
                am = input("Too much! " + question + " ")
            else:
                am = input("Must be a non-negative integer! " + question + " ")
            while not am.isdigit():
                am = input("Not a number. " + question + " ")
            am = int(am)
        return am


class Game:
    cur_year = 0
    money = 20000
    nation = 1000
    grain = 4000
    land = 150
    distempter = 2
    grown_last_year = 0

    @staticmethod
    def year_pass():
        Game.cur_year += 1
        Game.print_data(True)
        #==========Constant events==========#
        if Game.cur_year != 1:
            Game.collect()
        Game.buy_or_sell_grain()
        Game.seed()
        Game.giveaway()
        Game.propaganda()
        #==========Random events==========#
        Game.epidemic()
        Game.rats()
        Game.thieves()
        Game.heritage()
        Game.demographic_boom()
        #==========Half random events==========#
        Game.war()
        Game.expedition()

    #==========Utility funcs==========#

    @staticmethod
    def print_data(print_year=False):
        if print_year:
            print(f"Year {Game.cur_year} has come! Happy new year!")
            print("You have the following amount of resources:")
        else:
            print("You have this much resources left:")
        print(f"Money: {Game.money}")
        print(f"Nation: {Game.nation}")
        print(f"Grain: {Game.grain}")
        print(f"Land: {Game.land}")
        print(f"Distempter: {Game.distempter}%")

    @staticmethod
    def check_lose():
        if Game.distempter == 100:
            exit(0)
            print("You lost due to a rebel.")
        elif Game.nation == 0:
            exit(0)
            print("All the people died so you lost.")
        elif Game.land == 0:
            exit(0)
            print("You have no land left. You lost.")

    #==========Controlled events==========#

    @staticmethod
    def buy_or_sell_grain():
        if Game.grain == 0:
            print("You have no grain.")
            ch = "n"
        else:
            ch = Utilities.sanitize_yn("Do you want to sell your grain?")
        if ch == "y":
            price = random.randint(1, 10)
            print(f"The price is {price}")
            amount = Utilities.sanitize_number(
                "How much do you want to sell?", Game.grain)
            print("Aa-a-a-and sold!")
            Game.money += price * amount
            Game.grain -= amount
            Game.print_data()
        elif Game.money != 0:
            ch = Utilities.sanitize_yn("Do want to buy some grain?")
            if ch == "y":
                price = random.randint(3, 15)
                print(f"The price is {price}")
                amount = Utilities.sanitize_number(
                    "How much do you want to buy?", Game.money / price)
                print("Congrats on your purchase!")
                Game.money -= price * amount
                Game.grain += amount
                Game.print_data()
        
        Game.check_lose()

    @staticmethod
    def giveaway():
        if Game.grain == 0:
            ch = "n"
            print("You have no grain, so you are not able to give anything away.")
        else:
            ch = Utilities.sanitize_yn(
                "Do you want to give away some of your grain?")
        if ch == "y":
            amount = Utilities.sanitize_number(
                "How much do you want to give away?", Game.grain)
            if amount < Game.nation:
                to_rise = (1 - amount / Game.nation) * 40
                print(f"""You gave away too little!
The distempter has risen by {min(to_rise, 100 - Game.distempter)}%!
{Game.nation * to_rise // 100} people have starved to death!""")
                Game.nation *= (1 - to_rise // 100)

                Game.distempter += min(to_rise, 100 - Game.distempter)
            elif amount == Game.nation:
                print(f"""You gave away just enough. The people are satisfied.
The distempter has dropped by {min(5, Game.distempter)}%""")
                Game.distempter -= min(5, Game.distempter)
        Game.print_data()
            else:
                to_drop = (amount / Game.nation - 1) * 40
                to_be_born = int(Game.nation * to_drop // 100)
                print(f"""You gave away very much. The people are very happy!
The distempter has dropped by {min(to_drop, Game.distempter)}%!
{to_be_born} people have been born due to abundance of food!""")
                Game.distempter -= min(to_drop, Game.distempter)
                Game.nation *= (1 + to_drop // 100)
            Game.grain -= amount
        else:
            print(f"The people are furious!")
            to_rise = min(40, 100 - Game.distempter)
            print(f"The distempter has risen by {to_rise}%!")
            Game.distempter += to_rise
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def propaganda():
        if Game.money == 0:
            print("You have no money, so you cannot invest into propaganda.")
            return
        ch = Utilities.sanitize_yn(
            "Do you want to invest some money into propaganda?")
        if ch == "y":
            amount = Utilities.sanitize_number(
                "How much do you want to invest?", Game.money)
            to_drop = min(int(amount / 1000), Game.distempter)
            print(f"Good job! The distempter has dropped by {to_drop}%!")
            Game.distempter -= to_drop
            Game.money -= amount
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def seed():
        if Game.grain == 0:
            ch = "n"
            print("You have no grain, so you cannot seed anything.")
        else:
            ch = Utilities.sanitize_yn(
                "Do you want to seed some of your grain?")
        if ch == "y":
            amount = Utilities.sanitize_number("How much do you want to seed?",
                                               min(Game.grain, Game.land * 5))
            to_collect = round(random.random(), 1) + 1.5
            Game.grown_last_year = to_collect * amount
            Game.grain -= amount
            Game.print_data()
        else:
            Game.grown_last_year = 0
        
        Game.check_lose()

    @staticmethod
    def collect():
        Game.grain += Game.grown_last_year
        if Game.grown_last_year > 0:
            print(
                f"You collected {Game.grown_last_year} grain from last year's seeding!")
            Game.print_data()
        Game.check_lose()

    #==========Random events==========#

    @staticmethod
    def epidemic():
        x = Game.nation / 10000
        chance = 1 - 1 / ((x + 1) ** x)
        if random.random() <= chance:
            print("There was an epidemic! 10% of your population has died!")
            Game.nation = int(0.9 * Game.nation)
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def rats():
        if random.random() <= 0.2:
            print("Rats have eaten 30% of your grain!")
            Game.grain = int(Game.grain * 0.7)
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def thieves():
        x = Game.distempter / 100
        if random.random() <= x ** 3:
            print("Thieves have stolen 20% of your money!")
            Game.money = int(Game.money * 0.8)
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def heritage():
        if random.random() <= 0.07:
            to_earn = random.randint(1, 5) * 10000
            print(
                f"One of your relatives has recently passed away. You have inherited {to_earn} gold!")
            Game.money += to_earn
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def demographic_boom():
        x = Game.distempter / 100
        if random.random() <= (0.7 - 0.7 * (x ** (x + 1.2))):
            print("There was a demographic boom! Your population has increased by 15%!")
            Game.nation = int(Game.nation * 1.15)
            Game.print_data()
        Game.check_lose()

    #==========Half random events==========#

    @staticmethod
    def war(msg="A neighboring kingdom has declared war on you!"):
        if random.random() <= 0.07:
            print(msg)
            ch = Utilities.sanitize_yn("Do you want to surrender immediately?")
            if ch == "y":
                to_lose = random.randint(30, 70)
                print(
                    f"You have lost {min(to_lose, Game.land)} units of land.")
                Game.land -= min(Game.land, to_lose)
            else:
                army = Utilities.sanitize_number(
                    "How much army do you want to hire (1 unit = 1000 gold)?", Game.money / 1000)
                if random.random() <= 1 - 1 / ((0.1 * army + 1) ** (army / 2)):
                    print("You have won the war!")
                    to_earn_money = (round(random.random(), 2)
                                     * 2.2 + 1.8) * army * 1000
                    to_earn_land = random.randint(40, 90)
                    print(
                        f"You have earned {to_earn_money} gold and {to_earn_land} units of land!")
                    print(
                        f"The distempter has dropped by {min(Game.distempter, 5)}%!")
                    Game.distempter -= min(Game.distempter, 5)
                    Game.money += to_earn_money
                    Game.land += to_earn_land
                else:
                    print("You have lost the war.")
                    to_lose_money = min((round(random.random(), 2) * 2.2 + 1.8)
                                        * army * 1000, Game.money)
                    to_lose_land = min(random.randint(40, 90), Game.land)
                    to_raise_distempter = min(100 - Game.distempter, 5)
                    print(
                        f"You have lost {to_lose_money} gold and {to_lose_land} units of land.")
                    print(
                        f"The distempter has raised by {to_raise_distempter}%.")
                    Game.distempter += to_raise_distempter
                    Game.money -= to_lose_money
                    Game.land -= to_lose_land
            Game.print_data()
        Game.check_lose()

    @staticmethod
    def expedition():
        if random.random() <= 0.15:
            ch = Utilities.sanitize_yn(
                """Your people have gathered an expedition to explore new lands!
Do you want to invest in it?""")
            if ch == "y":
                amount = Utilities.sanitize_number(
                    "How much do you want to pay?", Game.money)
                x = amount / 2000
                if random.random() <= 1 - 1 / ((0.1 * x + 1) ** (x / 2)):
                    to_earn_grain = random.randint(40, 100) * 10
                    to_earn_land = random.randint(10, 25)
                    to_earn_nation = random.randint(8, 20) * 10
                    print(
                        f"""Your expedition has discovered new populated lands!
The settlements turned out to be peaceful and gave the explorers some grain!
You have earned {to_earn_grain} grain, {to_earn_land} units of land and {to_earn_nation} population!""")
                    Game.nation += to_earn_nation
                    Game.land += to_earn_land
                    Game.grain += to_earn_grain
                else:
                    print("The expedition was lost in the wilds.")
            Game.print_data()
        Game.check_lose()


if __name__ == "__main__":
    print("""Welcome to Kingdom simulator!
In this game you have to make decisions to rule as long as you can.
If your nation, land goes to zero or distempter raises to 100% you lose.
You can buy and sell grain.
You can plant 5 units of grain on 1 unit of land.
You can give your grain away.
You can invest money into propaganda.
Also there are random events that you will discover throughout the game.
..........Starting the game..........


""")
    while(True):
        Game.year_pass()
