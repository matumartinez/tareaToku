from superheroes import Team, Superhero
from utils import SuperheroAPICaller, EmailString
from typing import Tuple, Dict
from random import choice
from requests import post
from os import getenv


html = EmailString()
TEAM_SIZE = 5  # variable should be > 0 and < 365
EMAIL = getenv("EMAIL")


def main() -> None:
    html.open_string()
    team1, team2 = setup_teams()
    simulate_battle(team1, team2)
    if EMAIL:
        send_email()


def setup_teams() -> Tuple[Team]:
    html.concatenate("Assembling teams")
    html.concatenate(" ")
    api_caller = SuperheroAPICaller()
    team1 = Team()
    team2 = Team()

    for i in range(TEAM_SIZE):
        team1_member_info = api_caller.get_superhero()
        team1.add_superhero(Superhero(superhero_info=team1_member_info))

        team2_member_info = api_caller.get_superhero()
        team2.add_superhero(Superhero(superhero_info=team2_member_info))
    
    html.concatenate("The battle is about to begin")
    html.concatenate(f"Team 1: {team1}, alignment: {team1.alignment}")
    html.concatenate(f"Team 2: {team2}, alignment: {team2.alignment}")
    html.concatenate(" ")
    team1.define_team_stats()
    team2.define_team_stats()
    
    return team1, team2


def simulate_battle(team1: Team, team2: Team) -> None:
    # Teams take turns to start an attack, team1 is always the first attacker
    # An attacker and a defender are chosen randomly from each team
    turn = "team1"
    while team1.members and team2.members:
        team1_member = choice(team1.members)
        team2_member = choice(team2.members)
        if turn == "team1":
            html.concatenate(f"Team 1 attacks with {team1_member.name}")
            html.concatenate(f"Team 2 defends with {team2_member.name}")
            turn = "team2"
            simulate_fight(attacker = team1_member, defender = team2_member, teams={
                "defending_team": team2,
                "attacking_team": team1
            })
        elif turn == "team2":
            html.concatenate(f"Team 2 attacks with {team2_member.name}")
            html.concatenate(f"Team 1 defends with {team1_member.name}")
            turn = "team1"
            simulate_fight(attacker = team2_member, defender = team1_member, teams={
                "defending_team": team1,
                "attacking_team": team2
            })
    
    html.concatenate(f"Team 1 victory {team1}", bold=True) if team1.members \
        else html.concatenate(f"Team 2 victory {team2}", bold=True)


def simulate_fight(attacker: Superhero, defender: Superhero, teams: Dict[str, Team]) -> None:
    attack = choice([attacker.mental, attacker.strong, attacker.fast])
    html.concatenate(f"{attacker.name} attacks {defender.name} ({defender.hp} HP) dealing {attack} damage")
    defender.hp -= attack
    html.concatenate(f"{defender.name} has ({defender.hp}) HP left")
    if defender.hp <= 0:
        html.concatenate(f"{defender.name} has been defeated")
        html.concatenate(" ")
        teams["defending_team"].remove_member(member = defender)
        attacker.restore_hp_points()
    else:
        #If the attacker did not deafeat the defender, the roles are reverses until one of them wins
        simulate_fight(attacker = defender, defender = attacker, teams={
            "defending_team": teams["attacking_team"],
            "attacking_team": teams["defending_team"]
        })


def send_email() -> None:
    # For simplicity, mailgun token and domain were left hardcoded
    html.close_string()
    post(
        "https://api.mailgun.net/v3/sandbox7bff10a398a5462ca45eb46690dd2fb3.mailgun.org/messages",
        auth=("api", "f5a0c5dffec950b952a0283004434580-309b0ef4-4ae510d4"),
        data={"from": "mtmartinez2@uc.cl",
              "to": [EMAIL],
              "subject": "Superhero Battle Result",
              "html": html.email_string})


main()
