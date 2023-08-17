from random import choice, randint
from requests import get
from os import getenv


class SuperheroAPICaller:
    
    id_list = [num for num in range(1, 732)]
    token = getenv('TOKEN')

    def __init__(self) -> None:
        if not self.token:
            raise Exception("Please setup TOKEN env variable")

    def get_superhero(self) -> dict:
        id = choice(self.id_list)
        self.id_list.remove(id)
        response = get(f"https://superheroapi.com/api/{self.token}/{id}")
        superhero_info = response.json()

        i = superhero_info["powerstats"]["intelligence"]
        superhero_info["powerstats"]["intelligence"] = int(i) if i != "null" else randint(1, 100)

        s = superhero_info["powerstats"]["strength"]
        superhero_info["powerstats"]["strength"] = int(s) if s != "null" else randint(1, 100)

        sp = superhero_info["powerstats"]["speed"]
        superhero_info["powerstats"]["speed"] = int(sp) if sp != "null" else randint(1, 100)

        d = superhero_info["powerstats"]["durability"]
        superhero_info["powerstats"]["durability"] = int(d) if d != "null" else randint(1, 100)
        
        p = superhero_info["powerstats"]["power"]
        superhero_info["powerstats"]["power"] = int(p) if p != "null" else randint(1, 100)

        c = superhero_info["powerstats"]["combat"]
        superhero_info["powerstats"]["combat"] = int(c) if c != "null" else randint(1, 100)

        return superhero_info
