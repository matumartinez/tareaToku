from math import floor
from random import randint
from typing import Type, Union, List


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

    def define_stats(self, team_alignment: str) -> None:
        actual_stamina = randint(0, 10)
        fb = 1 + randint(0, 9) if self.alignment == team_alignment else (1 + randint(0, 9))**-1

        intelligence = floor((2*self.intelligence + actual_stamina)/1.1 * fb)
        strength = floor((2*self.strength + actual_stamina)/1.1 * fb)
        speed = floor((2*self.speed + actual_stamina)/1.1 * fb)
        durability = floor((2*self.durability + actual_stamina)/1.1 * fb)
        power = floor((2*self.power + actual_stamina)/1.1 * fb)
        combat = floor((2*self.combat + actual_stamina)/1.1 * fb)

        self.__original_hp = floor((strength*0.8 + durability*0.7 + power)/2 * (1 + actual_stamina/10)) + 100
        self.__hp = floor((strength*0.8 + durability*0.7 + power)/2 * (1 + actual_stamina/10)) + 100
        self.__mental = (intelligence*0.7 + speed*0.2 + combat*0.1) * fb
        self.__strong = (strength*0.6 + power*0.2 + combat*0.2) * fb
        self.__fast = (speed*0.55 + durability*0.25 + strength*0.2) * fb
    
    def restore_hp_points(self) -> None:
        self.__hp = self.__original_hp

    @property
    def hp(self) -> Union[int, float]:
        return self.__hp
    
    @hp.setter
    def hp(self, new_value: Union[int, float]) -> None:
        self.__hp = new_value
    
    @property
    def mental(self) -> Union[int, float]:
        return self.__mental
    
    @property
    def strong(self) -> Union[int, float]:
        return self.__strong
    
    @property
    def fast(self) -> Union[int, float]:
        return self.__fast


class Team:

    def __init__(self) -> None:
        self.__good_alignment = 0
        self.__bad_alignment = 0
        self.__alignment = "good"
        self.__members = []
    
    def add_superhero(self, superhero: Type[Superhero]) -> None:
        self.__members.append(superhero)
        if superhero.alignment == "good":
            self.__good_alignment += 1
        else:
            self.__bad_alignment += 1
        self.__alignment = "good" if self.__good_alignment >= self.__bad_alignment else "bad"
    
    def define_team_stats(self) -> None:
        for member in self.members:
            member.define_stats(team_alignment=self.alignment)

    @property
    def members(self) -> List[Type[Superhero]]:
        return self.__members
    
    @property
    def alignment(self) -> str:
        return self.__alignment
    
    def remove_member(self, member: Type[Superhero]) -> None:
        self.__members.remove(member)
    
    def __str__(self) -> str:
        return f"{[member.name for member in self.members]}"
