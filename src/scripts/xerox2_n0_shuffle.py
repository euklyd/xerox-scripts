import random
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

from src.utils import sheet

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
SECRET = 'conf/google_creds.json'
SHEET_NAME = "Turbo Xerox Metal Raiders Besieged: Ultimate Pro Tour Duelist Series signups (Responses)"
PAGE_NAME = "Deck Submissions"

# SEED = "larper above"  # og
SEED = "Eat the rich"  # Mulligan

USERNAME = "What's your discord username? (with discriminator)"
DECK = "What's in your deck?"
DECKNAME = "What's your deck name?"
IGNOREME = "IGNOREME"

HANDSIZE = 4
DECKSIZE = 18


@dataclass
class Card:
    name: str
    short_text: str
    long_text: str
    prio: str
    b_h: str


@dataclass
class DeckEntry:
    username: str
    # deck: List[Card]
    deck: List[str]
    deckname: str
    hand: List[Card] = field(default_factory=list)

    @staticmethod
    def from_record(record: Dict[str, str]) -> "DeckEntry":
        cards = record[DECK].strip()
        cards = [line.strip() for line in cards.split("\n")]
        deck = []
        for card in cards:
            m = re.match(r"(\d)x (.*)", card)
            quantity = int(m.group(1))
            cardname = m.group(2)
            for _ in range(quantity):
                deck.append(cardname)

        return DeckEntry(username=record[USERNAME], deckname=record[DECKNAME], deck=deck)

    def n0(self):
        random.shuffle(self.deck)
        self.hand = self.deck[:HANDSIZE]

    @property
    def remaining_deck(self) -> List[Card]:
        return self.deck[len(self.hand):]


def main():
    conn = sheet.SheetConnection(secret=SECRET, scope=SCOPE)
    page = conn.get_page(
        sheet_name=SHEET_NAME,
        page_name=PAGE_NAME)

    records = page.get_all_records()

    players = {}
    for record in records:
        if record[IGNOREME]:
            continue
        player = DeckEntry.from_record(record)
        players[player.username] = player

    print("Validating decks...")
    bad_lengths = False
    for player in players.values():
        if len(player.deck) != DECKSIZE:
            print(f"{player.username} has {len(player.deck)} cards in their deck.")
            bad_lengths = True
        player.n0()
    if bad_lengths:
        return
    print("All decks legal.")

    sortedplayers = sorted(players.values(), key=lambda x: x.username.lower())

    sheet = conn.get_sheet(
        sheet_name=SHEET_NAME
    )
    ws = sheet.add_worksheet(title=f"n0_rand_{datetime.now().isoformat().replace(':', '_')}", cols=100, rows=1)

    row = ["Seed", SEED]
    ws.append_row(row, insert_data_option="INSERT_ROWS")
    print(row)
    row = ["Username"] + [player.username for player in sortedplayers]
    ws.append_row(row, insert_data_option="INSERT_ROWS")
    print(row)
    row = ["Deck Name"] + [player.deckname for player in sortedplayers]
    ws.append_row(row, insert_data_option="INSERT_ROWS")
    print(row)

    for i in range(HANDSIZE):
        row = [f"Hand #{i + 1}"] + [player.deck[i] for player in sortedplayers]
        ws.append_row(row, insert_data_option="INSERT_ROWS")
        print(row)

    for i in range(HANDSIZE, DECKSIZE):
        row = [f"Deck #{i + 1}"] + [player.deck[i] for player in sortedplayers]
        ws.append_row(row, insert_data_option="INSERT_ROWS")
        print(row)

    row = ["Role PM Message"] + [role_pm_msg(player) for player in sortedplayers]
    ws.append_row(row, insert_data_option="INSERT_ROWS")
    print(row)


def role_pm_msg(player: DeckEntry) -> str:
    s = "\n".join([player.deck[i] for i in range(HANDSIZE)])
    return (
        "Attention duelist!\n\n"
        f"**{player.username}**, you registered the deck **{player.deckname}**.\n\n"
        "This is your one mulligan. Your new hand (which you must keep) is:\n"
        "```\n"
        f"{s}"  # ugh why can't I just put a string here
        "\n```"
        "You will draw a fifth card at the beginning of Night 1."
    )


if __name__ == "__main__":
    random.seed(SEED)
    main()
