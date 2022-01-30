import pprint
import random
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

from src.utils import sheet

from src.cards.xerox2_cards import Card, Action, CARDS

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
SECRET = 'conf/google_creds.json'

CARDS_SHEET_NAME = "EIMM TURBO (xerox) ON MOTORCYCLES"
CARDS_PAGE_NAME = "Card Database: Season 2"

DAMAGING = "Dmg"

SHOTCARD = Card(
    name="Standard Shot",
    short_text="3 atk shot",
    long_text="",
    prio="Damaging",
    b_h="",
    actions=[Action(name="Standard shot", prio=DAMAGING, text="3 atk shot", b_h="H")]
)

DECKS_SHEET_NAME = "Turbo Xerox Metal Raiders Besieged: Ultimate Pro Tour Duelist Series signups (Responses)"
DECKS_PAGE_NAME = "N0 Decks"

USERNAME = "Username"
# DECK = "What's in your deck?"
DECKNAME = "Deck Name"
# IGNOREME = "IGNOREME"

HANDSIZE = 5
DECKSIZE = 18


@dataclass
class DeckEntry:
    username: str
    deck: List[Card] = field(default_factory=list)
    deckname: str = ""
    hand: List[Card] = field(default_factory=list)

    # @staticmethod
    # def from_record(record: Dict[str, str]) -> "DeckEntry":
    #     cards = record[DECK].strip()
    #     cards = [line.strip() for line in cards.split("\n")]
    #     deck = []
    #     for card in cards:
    #         m = re.match(r"(\d)x (.*)", card)
    #         quantity = int(m.group(1))
    #         cardname = m.group(2)
    #         for _ in range(quantity):
    #             deck.append(cardname)
    #
    #     return DeckEntry(username=record[USERNAME], deckname=record[DECKNAME], deck=deck)

    # def n0(self):
    #     random.shuffle(self.deck)
    #     self.hand = self.deck[:HANDSIZE]
    #
    # @property
    # def remaining_deck(self) -> List[Card]:
    #     return self.deck[len(self.hand):]


def main():
    conn = sheet.SheetConnection(secret=SECRET, scope=SCOPE)
    page = conn.get_page(
        sheet_name=CARDS_SHEET_NAME,
        page_name=CARDS_PAGE_NAME,
    )

    records = page.get_all_records()

    cards = {}
    for record in records:
        print(record)
        try:
            card = Card.from_record(record)
        except ValueError:
            print(f"Skipping record: {record}")
            continue
        cards[card.name] = card

    pprint.pprint(cards)

    page = conn.get_page(
        sheet_name=DECKS_SHEET_NAME,
        page_name=DECKS_PAGE_NAME,
    )

    records = page.get_all_records()

    players: Dict[str, DeckEntry] = {player: DeckEntry(username=player) for player in page.row_values(1) if
                                     player not in {"Username", ""}}

    print(len(players))
    for player in players:
        players[player].deckname = records[0][player]
        for i in range(1, 1 + DECKSIZE):
            players[player].deck.append(cards[records[i][player]])

    # print(players)  # HAHA VIEWERS DON'T GET ILLEGAL KNOWLEDGE
    # for key in records
    #
    # for record in records

    ws_out = conn.get_page(DECKS_SHEET_NAME, "n0 test")

    row_num = 0
    rows = []
    for player in sorted(players.values(), key=lambda x: x.username.lower()):
        shot_row = make_row("Shot", player.username, "", action=SHOTCARD.actions[0], row=row_num, n=1)
        row_num += 1
        card_rows = []
        counts = {}
        for i, card in enumerate(player.deck):
            if card.name not in counts:
                counts[card.name] = 0
            counts[card.name] += 1
            if i < 5:
                # hand
                for action in CARDS[card.name].actions:
                    card_rows.append(make_row("Hand", player.username, "", n=counts[card.name], action=action))
            else:
                # deck
                for action in CARDS[card.name].actions:
                    card_rows.append(make_row("Deck", player.username, "", n=counts[card.name], action=action))
        row_num += len(card_rows)

        # ws_out.append_row(shot_row, value_input_option='USER_ENTERED')  # i hope this works
        # ws_out.append_rows(card_rows)
        rows.append(shot_row)
        rows.extend(card_rows)
    ws_out.append_rows(rows)


def make_row(location: str, username: str, alias: str, action: Action, n: int, row: int = None) -> list:
    hp = ''
    atk = ''
    hp_net_dmg = ''
    net_dmg = ''
    status = ''
    final_hp = ''
    if location == 'Shot':
        assert row is not None
        hp = 12
        atk = 3
        hp_net_dmg = f'=if(P{row}-Q{row}>0, 0, Q{row}-P{row})'
        net_dmg = f'=if(F{row}-R{row}<1, R{row}, if(S{row}-T{row}>0, 0, T{row}-S{row})+R{row}+U{row})'
        status = f'=if(F{row}-R{row}<1, "Dead", if(F{row}-V{row}<1, "Dead", if(F{row}-V{row}<1, "Dead", "Alive")))'
        final_hp = f'=min(if(F{row}-R{row}<1, F{row}-R{row}, if(F{row}-V{row}<1, F{row}-V{row}, max(F{row}-V{row}-X{row}, 1)+Y{row})), E{row})'
    return [
        '',  # #
        "",  # temp
        action.ninja,  # ninja
        location,
        username,
        alias,
        hp,
        hp,
        atk,
        f"({n}) {action.name}",
        action.prio,
        action.b_h,
        action.text,
        '',  # night notes
        '',  # target
        # '',  # final target
        '',  # outcome
        '',
        '',
        hp_net_dmg,
        '',
        '',
        '',
        net_dmg,
        status,
        '',
        # '',
        final_hp,
        '',  # written results
        '',  # next-night notes
    ]


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
    main()
