from math import floor
from random import randint
from typing import Type


class Superhero:

    def __init__(self, superhero_info: dict) -> None:
        self.intelligence: int = superhero_info["powerstats"]["intelligence"]
        self.strength: int = superhero_info["powerstats"]["strength"]
        self.speed: int = superhero_info["powerstats"]["speed"]
        self.durability: int = superhero_info["powerstats"]["durability"]
        self.power: int = superhero_info["powerstats"]["power"]
        self.combat: int = superhero_info["powerstats"]["combat"]
        self.name: str = superhero_info["name"]
        self.alignment: str = superhero_info["biography"]["alignment"]

    def define_stats(self, team_alignment: str):
        actual_stamina = randint(0, 10)
        fb = 1 + randint(0, 9) if self.alignment == team_alignment else (1 + randint(0, 9))**-1

        intelligence = floor((2*self.intelligence + actual_stamina)/1.1 * fb)
        strength = floor((2*self.strength + actual_stamina)/1.1 * fb)
        speed = floor((2*self.speed + actual_stamina)/1.1 * fb)
        durability = floor((2*self.durability + actual_stamina)/1.1 * fb)
        power = floor((2*self.power + actual_stamina)/1.1 * fb)
        combat = floor((2*self.combat + actual_stamina)/1.1 * fb)

        self.hp = floor((strength*0.8 + durability*0.7 + power)/2 * (1 + actual_stamina/10)) + 100
        self.mental = (intelligence*0.7 + speed*0.2 + combat*0.1) * fb
        self.strong = (strength*0.6 + power*0.2 + combat*0.2) * fb
        self.fast = (speed*0.55 + durability*0.25 + strength*0.2) * fb


class Team:

    def __init__(self) -> None:
        self.good_alignment = 0
        self.bad_alignment = 0
        self.alignment = "good"
        self.members = []
    
    def add_superhero(self, superhero: Type[Superhero]) -> None:
        self.members.append(superhero)
        if superhero.alignment == "good":
            self.good_alignment += 1
        else:
            self.bad_alignment += 1
        self.alignment = "good" if self.good_alignment >= self.bad_alignment else "bad"
    
    def define_team_stats(self) -> None:
        for member in self.members:
            member.define_stats(team_alignment=self.alignment)
    
    def __str__(self):
        return f"{[member.name for member in self.members]}"
