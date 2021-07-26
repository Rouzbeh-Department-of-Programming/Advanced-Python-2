class Car:
    def __init__(self, name, company, year, price):
        self.price = price
        self.name = name
        self.company = company
        self.year = year
        self.owner = None

    def print_details(self):
        print('name: ' + self.name + '\tyear: ' + str(self.year) + '\tprice: ' + str(self.price))


class Person:
    def __init__(self, name, age, money):
        self.money = money
        self.name = name
        self.age = age
        self.cars = []

    def buy(self, car):
        if self.age < 18:
            print('You are not old enough.')
        elif self.money < car.price:
            print('You don\'t have enough money :(')
        else:
            if car.owner is not None:
                car.owner.money += car.price
                car.owner.cars.remove(car)
            else:
                car.company.earnings += car.price
                car.company.store.remove(car)

            self.money -= car.price
            self.cars.append(car)
            car.owner = self

    def show_cars(self):
        print(self.name + ':')
        for i in self.cars:
            i.print_details()


class Company:
    def __init__(self, name):
        self.name = name
        self.store = []
        self.products = []
        self.earnings = 0

    def add_car_to_products(self, car):
        self.products.append(car)

    def advance(self):
        for i in self.products:
            self.store.append(Car(i.name, self, i.year, i.price))

    def show_store(self):
        print('Store:')
        for i in self.store:
            i.print_details()

    def report_income(self):
        print('We have gained about ' + str(self.earnings) + ' =)))')


hyundai = Company('Hyundai')
hyundai.add_car_to_products(Car('Accent', hyundai, 2019, 200))
hyundai.add_car_to_products(Car('Elantra', hyundai, 2021, 300))

for i in range(5):
    hyundai.advance()
hyundai.show_store()

p1 = Person('Taha', 20, 500)
p1.buy(hyundai.store[1])
p1.buy(hyundai.store[2])
# اینجا طاها برای ماشین دوم باید پولش کم بیاد و پیغام مناسب براش چاپ بشه

p2 = Person('Amirhossein', 15, 1000)
p2.buy(hyundai.store[0])
# اینجا امیرحسین بابت سن کمش نمیتونه ماشین بخره و باید براش پیغام مناسب چاپ بشه

p3 = Person('Peyman', 40, 2000)
p3.buy(hyundai.store[0])
p3.buy(hyundai.store[0])
p3.buy(hyundai.store[0])
p3.buy(hyundai.store[0])
p3.buy(hyundai.store[0])

p1.show_cars()
p3.show_cars()

p1.buy(p3.cars[0])
p1.buy(p3.cars[0])

p1.show_cars()
p3.show_cars()
# توی 6 خط کد بالا، طاها سعی کرد دو تا از ماشین های پیمان رو بخره، که پولش به یکی ازونا فقط میرسه.
# با استفاده از متود های show_cars میتوانیم تبادل ماشین میان دو نفر را ببینیم.

hyundai.report_income()
