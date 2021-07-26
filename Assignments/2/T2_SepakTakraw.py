class Player:
    def __init__(self, name, cost, overall):
        self.name = name
        self.cost = cost
        self.overall = overall
        self.club = None


class Club:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.players = []
        self.score = 0

    def buy_player(self, player):
        if self.budget < player.cost:
            print('There is not enough budget.')
        else:
            if player.club is not None:
                player.club.budget += player.cost
                player.club.players.remove(player)
            player.club = self
            self.budget -= player.cost
            self.players.append(player)

    def get_average_overall(self):
        sum = 0
        for i in self.players:
            sum += i.overall
        return sum / len(self.players)

    def get_score(self):
        return self.score


class League:
    def __init__(self):
        self.clubs = []

    def add_club(self, club):
        self.clubs.append(club)

    def hold_match(self, club1, club2):
        if club1.get_average_overall() > club2.get_average_overall():
            print(club1.name + ' defeated ' + club2.name)
            club1.score += 3
        elif club1.get_average_overall() < club2.get_average_overall():
            print(club2.name + ' defeated ' + club1.name)
            club2.score += 3
        else:
            print(club1.name + ' and ' + club2.name + ' had a draw match.')
            club1.score += 1
            club2.score += 1

    def auto_hold_matches(self):
        for i in range(len(self.clubs) - 1):
            for j in range(i + 1, len(self.clubs)):
                self.hold_match(self.clubs[i], self.clubs[j])

    def show_scoreboard(self):
        self.clubs.sort(key=Club.get_score, reverse=True)
        for i in range(len(self.clubs)):
            print(str(i + 1) + '- ' + self.clubs[i].name + ' with ' + str(self.clubs[i].score) + ' points')


p1 = Player('Messi', 120, 99)
p2 = Player('Ronaldo', 70, 90)
p3 = Player('Dybala', 50, 85)
p4 = Player('Nadal', 150, 67)
p5 = Player('James', 180, 95)
p6 = Player('Federer', 120, 100)
p7 = Player('Bolt', 60, 88)

c1 = Club('Barcelona', 250)
c2 = Club('Lakers', 200)
c3 = Club('Zenit', 400)

c1.buy_player(p1)
c1.buy_player(p2)
c1.buy_player(p4)  # اینجا باید بودجش کم بیاد

c2.buy_player(p3)
c2.buy_player(p4)

c3.buy_player(p5)
c3.buy_player(p6)
c3.buy_player(p7)

print('Budget of c3: ' + str(c3.budget))
c1.buy_player(p7)
print('Budget of c3: ' + str(c3.budget))

l1 = League()
l1.add_club(c1)
l1.add_club(c2)
l1.add_club(c3)

l1.auto_hold_matches()
l1.show_scoreboard()
