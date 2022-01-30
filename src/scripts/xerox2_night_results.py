import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from src.utils import sheet

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
SECRET = 'conf/google_creds.json'

SHEET_NAME = "Turbo Xerox Metal Raiders Besieged: Ultimate Pro Tour Duelist Series signups (Responses)"
PAGE_NAME = "n6 draws"
DEAD = {
    "Ani#7899",
    "apollos#6792",
    "PassTheSaltDude",
    "Xinnidy#1317",
}


@dataclass
class CardCount:
    count: int
    card: str


@dataclass
class HPStuff:
    max: int
    start: int
    dmg: int
    heal: int
    final: int


def main():
    conn = sheet.SheetConnection(secret=SECRET, scope=SCOPE)
    page = conn.get_page(
        sheet_name=SHEET_NAME,
        page_name=PAGE_NAME)

    records = page.get_all_records()

    players: Dict[str, List[CardCount]] = defaultdict(list)
    aliases: Dict[str, str] = {}
    hps: Dict[str, HPStuff] = {}

    for row in records:
        action_name: str = row["Action Name"].strip()
        player_name: str = row["Player"]
        location: str = row["Location"]
        if location.lower() == "shot" and action_name == "(1) Standard shot":
            # action name needed to filter out NPCs
            hps[player_name] = HPStuff(
                max=int(row["Max"]),
                start=int(row["HP"]),
                dmg=int(row["D Net"]),
                heal=-1 * int(row["Low"]) if row["Low"] != "" else 0,  # healing is inverted
                final=int(row["Final"]),
            )
        if location not in {"Hand", "Token"}:
            continue
        # need to ignore npcs, which are of "shot" location
        aliases[player_name] = row["Alias"]
        if player_name in DEAD:
            # dead players never got cleaned up and also we don't care about those losers
            continue
        if action_name.lower().endswith(" token"):
            # it's a token, can be repeated
            players[player_name].append(CardCount(0, action_name))
        else:
            # it's not a token, has an "ID" and we need to filter out multirow cards
            m = re.match(r"^\((\d)\) ([^()]*)( \(.*)?$", action_name)
            if not m:
                print(action_name)
            cc = CardCount(int(m.group(1)), m.group(2))
            if cc not in players[player_name]:
                players[player_name].append(cc)

    output_row1_header = []
    output_row2_inforesponse = []
    output_row3_nightresult = []

    for player, cards in players.items():
        header = f"{player} / {aliases[player]}"
        print(header)
        output_row1_header.append(header)

        cards = sorted(cards, key=lambda x: x.card.lower())
        nontokens = [card for card in cards if "token" not in card.card.lower()]
        tokens = [card for card in cards if "token" in card.card.lower()]
        print("```")
        for card in nontokens:
            if "token" not in card.card.lower():
                print(card.card)
        if tokens:
            print(" ")
            for card in tokens:
                if "token" in card.card.lower():
                    print(card.card)
        print("```\n\n")

        hand_str = "\n".join(card.card for card in nontokens)

        # info response doesn't get tokens
        inforesponse = f"`{aliases[player]}`'s hand is: ```\n{hand_str}\n```"

        if tokens:
            hand_str += "\n\n" + "\n".join(card.card for card in tokens)

        hp_result = "FIXME"
        hp = hps[player]
        actual_healing = min(hp.max - (hp.start - hp.dmg), hp.heal)
        assert hp.start - hp.dmg + actual_healing == hp.final
        if hp.dmg > 0 and hp.heal > 0:
            hp_result = f"You lost {hp.dmg} HP and healed {actual_healing}, leaving you with {hp.final}."
        elif hp.dmg > 0 and hp.heal == 0:
            hp_result = f"You lost {hp.dmg} HP, leaving you with {hp.final}."
        elif hp.dmg == 0 and hp.heal > 0:
            hp_result = f"You healed {hp.heal} HP, leaving you with {hp.final}."
        elif hp.dmg == hp.heal == 0:
            assert hp.final == hp.start
            hp_result = f"You remain at {hp.final} HP."

        nightresult = f"{hp_result}\n\nYour new hand is: ```\n{hand_str}\n```"
        output_row2_inforesponse.append(inforesponse)
        output_row3_nightresult.append(nightresult)

    with open(f"output_{PAGE_NAME}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(output_row1_header)
        writer.writerow(output_row2_inforesponse)
        writer.writerow(output_row3_nightresult)


if __name__ == "__main__":
    main()
