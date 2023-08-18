from superheroes import Team, Superhero
from utils import SuperheroAPICaller, EmailString
from typing import Tuple
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
    # Teams take turns to attack, team1 is always the first attacker
    # An attacker and a victim are chosen randomly from each team
    turn = "team1"
    while team1.members and team2.members:
        team1_member = choice(team1.members)
        team2_member = choice(team2.members)
        if turn == "team1":
            html.concatenate("Team 1 turn")
            turn = "team2"
            simulate_fight(attacker=team1_member, defender=team2_member, defender_team=team2)
        elif turn == "team2":
            html.concatenate("Team 2 turn")
            turn = "team1"
            simulate_fight(attacker=team2_member, defender=team1_member, defender_team=team1)
    
    html.concatenate(f"Team 1 victory {team1}", bold=True) if team1.members \
        else html.concatenate(f"Team 2 victory {team2}", bold=True)


def simulate_fight(attacker: Superhero, defender: Superhero, defender_team: Team) -> None:
    attack = choice([attacker.mental, attacker.strong, attacker.fast])
    html.concatenate(
        f"{attacker.name} attacks {defender.name} ({defender.hp} HP) dealing {attack} damage")
    defender.hp -= attack
    html.concatenate(f"{defender.name} has ({defender.hp}) HP left")
    if defender.hp <= 0:
        html.concatenate(f"{defender.name} is dead")
        defender_team.members.remove(defender)
    html.concatenate(" ")


def send_email() -> None:
    # For simplicity, mailgun token and domain were left hardcoded
    html.close_string()
    post(
        "https://api.mailgun.net/v3/sandbox7bff10a398a5462ca45eb46690dd2fb3.mailgun.org/messages",
        auth=("api", "key-ccb69ebbe0d54fd3df3e1f87a07d91ae"),
        data={"from": "mtmartinez2@uc.cl",
              "to": [EMAIL],
              "subject": "Superhero Battle Result",
              "html": html.email_string})


main()
