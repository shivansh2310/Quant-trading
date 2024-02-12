class Animal():
    def __init__(self, name):
        self.name = name
    
    def say_my_name(self):
        print("my name is", self.name)

class Monkey(Animal):
    
    def __init__(self, name):
        self.name = name

    def say_my_name(self):
        print("my monkey name is", self.name)

monkey = Monkey(name="moka")
monkey.say_my_name()

class Monkey(Ape):

    def __init__(self, name, species):
        self.name = name
        self.species = species

monkey = Monkey(name="Moka", species="Chimp")
monkey.say_my_name()