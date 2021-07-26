class Animal:
    def zoo_break(self):
        print('Run Away!')


class Fish(Animal):
    def swim(self):
        print('I\'m swimming.')


class Salmon(Fish):
    def having_scale(self):
        print('I have scales.')


class Shark(Fish):
    def smell_blood(self):
        print('There is a smell of blood nearby.')


class Bird(Animal):
    def wing(self):
        print('I\'m winging.')


class Crow(Bird):
    def fly(self):
        print('i\'m flying')


class Hen(Bird):
    def hatch(self):
        print('Now we have a new egg :)')


class Amphibious(Animal):
    def live_in_land_and_water(self):
        print('I can live in both land and water.')


class Reptile(Animal):
    def crawl(self):
        print('I\'m crawling.')


class Snake(Reptile):
    def sting(self):
        print('You are delicious =)')


class Lizard(Reptile):
    def breed_new_tail(self):
        print('New tail !!!')


class Mammal(Animal):
    def lactate(self):
        print('My child is not hungry anymore.')


class Cow(Mammal):
    def ma_ma(self):
        print('Maaa Maaa')


class Sheep(Mammal):
    def ba_ba(self):
        print('Baaa Baaa')


print('a Salmon:')
a1 = Salmon()
a1.zoo_break()
a1.swim()
a1.having_scale()

print('\na Shark:')
a2 = Shark()
a2.zoo_break()
a2.swim()
a2.smell_blood()

print('\na Crow:')
a3 = Crow()
a3.zoo_break()
a3.wing()
a3.fly()

print('\na Hen')
a4 = Hen()
a4.zoo_break()
a4.wing()
a4.hatch()

print('\nan Amphibious')
a5 = Amphibious()
a5.zoo_break()
a5.live_in_land_and_water()

print('\na Snake:')
a6 = Snake()
a6.zoo_break()
a6.crawl()
a6.sting()

print('\na Lizard:')
a7 = Lizard()
a7.zoo_break()
a7.crawl()
a7.breed_new_tail()

print('\na Cow:')
a8 = Cow()
a8.zoo_break()
a8.lactate()
a8.ma_ma()

print('\na Sheep:')
a9 = Sheep()
a9.zoo_break()
a9.lactate()
a9.ba_ba()