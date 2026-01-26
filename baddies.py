import random

class Baddies:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def attack(self, target):
        damage = random.randint(1, self.attack_power)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} takes {amount} damage. HP: {self.hp}/{self.max_hp}")

    def is_alive(self):
        return self.hp > 0
