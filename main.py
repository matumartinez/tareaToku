from superheroes import Team, Superhero
from utils import SuperheroAPICaller
from typing import Tuple


TEAM_SIZE = 5  # variable should be > 0 and < 731

def main() -> None:
    team1, team2 = setup_teams()
    simulate_battle(team1, team2)


def setup_teams() -> Tuple[Team]:
    print("Assembling teams")
    print(" ")
    api_caller = SuperheroAPICaller()
    team1 = Team()
    team2 = Team()

    for i in range(TEAM_SIZE):
        team1_member_info = api_caller.get_superhero()
        team1.add_superhero(Superhero(superhero_info=team1_member_info))

        team2_member_info = api_caller.get_superhero()
        team2.add_superhero(Superhero(superhero_info=team2_member_info))
    
    print("The battle is about to begin")
    print(f"Team 1: {team1}, alignment: {team1.alignment}")
    print(f"Team 2: {team2}, alignment: {team2.alignment}")
    team1.define_team_stats()
    team2.define_team_stats()
    
    return team1, team2


def simulate_battle(team1: Team, team2: Team) -> None:
    turn = 0
    #while team1.members and team2.members:


main()
