from superheroes import Team, Superhero
from utils import SuperheroAPICaller
from typing import Tuple
from random import choice


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
    print(" ")
    team1.define_team_stats()
    team2.define_team_stats()
    
    return team1, team2


def simulate_battle(team1: Team, team2: Team) -> None:
    # Teams take turns to attack, team1 is always the first attacker
    # An attacker and a victim are chosen randomly from each team
    turn = "team1"
    while team1.members and team2.members:
        team1_member = choice(team1.members)
        team2_member = choice(team2.members)
        if turn == "team1":
            print("Team 1 turn")
            turn = "team2"
            simulate_fight(attacker=team1_member, defender=team2_member, defender_team=team2)
        elif turn == "team2":
            print("Team 2 turn")
            turn = "team1"
            simulate_fight(attacker=team2_member, defender=team1_member, defender_team=team1)
    
    print("Team 1 victory", team1) if team1.members else print("Team 2 victory", team2)


def simulate_fight(attacker: Superhero, defender: Superhero, defender_team: Team) -> None:
    attack = choice([attacker.mental, attacker.strong, attacker.fast])
    print(f"{attacker.name} attacks {defender.name} ({defender.hp} HP) dealing {attack} damage")
    defender.hp -= attack
    print(f"{defender.name} has ({defender.hp}) HP left")
    if defender.hp <= 0:
        print(f"{defender.name} is dead")
        defender_team.members.remove(defender)
    print(" ")


main()
