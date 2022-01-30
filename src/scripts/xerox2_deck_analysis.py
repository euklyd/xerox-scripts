import csv
import pprint
from typing import List

from src.scripts.xerox2_n0_shuffle import (
    IGNOREME,
    DeckEntry,
    SECRET,
    SCOPE,
    SHEET_NAME,
    PAGE_NAME,
    DECKSIZE,
)
from src.utils import sheet

CARDS = {
    "Thunderdome Elliptical": "discard 1: 8/3 nl hurtyjail",
    "Step on Me!": "discard 2: flex hijack",
    "Mystical Sleep Typhoon": "abilblock. if two of ~ used on same alias, fb.",
    "Harpie's Sheep Typhoon": "shotblock. if two of ~ used on same alias, fb.",
    "IDLE YOUR DOCS": "3 hp jdoc",
    "Disposable Gavin": "6 hp doc. if dmg >= doc amt, draw 1.",
    "Upstart Goblin": "3 hp heal. if hp after heal < max OR if mutual heal successful, draw 1.",
    '"Graceful" Charity': "3 atk vig. draw 1. discard 1 next night.",
    "Sheep Shearing": "2 hp transplant",
    "Power Play": "2 atk buff. if alias's shot kills, draw 1. if mutual: next-night atk+1.",
    "Burst Stream of Destruction": "docbusterizer. draw 1.",
    "Tunnel Vision": "flex empower",
    "Everyone's Friend": "abil motivate (shot motivate on plusles). draw 1.",
    "We Didn't Shoot You Monde": "alias cop + track. draw 1 (2 if even number of mondes used)",
    "Sorry For Shooting You Monde": "hp cop + watch. draw 1 (2 if even number of mondes used)",
    "Cop of Greed": "hand cop. draw 2.",
    "Checker Bribery": "free card. tutor 1.",
    "I Hope This Finds You Well": "abil disable + force discard 1",
    "A Vest For Plusle's Life": "discard 2 or pay 2 hp [can mix and match]: 1 atk / 3 hp npc maker. max 2 npcs at once.",
    "Good News I Drew You a Card": "1 dmg nl vig. mutual draw 1.",
    "Pleading Face": "shot rogue (strongwilled if hellbent).",
    "Talking to TBZ": "2 dmg vig. 3-cards poison.",
    "Cockroach Strats": "draw 1 (+1 if hellbent).",
    "Sheep with a Gun": "1 dmg vig. madness: 2 dmg vig token.",
    "Wooly Sheep": "1 atk debuff. madness: 2 atk debuff token.",
    "Sheep, MD": "2 hp doc. madness: 4 hp doc token.",
    "Frantic Search": "discard 1: self card ninjaize. draw 2",
    "Literacy": "hand cop + mimic.",
    "Gravedigging Gravedigs": "temp npc. self-moti for tokens",
    "Helping Hand": "shot motivate. if on own plusle, perma +1 atk. doesn't stack.",
    "Ojama RAD": "discard x: x+1 vig",
}


def get_decks(records, decksize) -> List[DeckEntry]:
    players = {}
    for record in records:
        if record[IGNOREME]:
            continue
        player = DeckEntry.from_record(record)
        players[player.username] = player

    print("Validating decks...")
    bad_lengths = False
    for player in players.values():
        if len(player.deck) != decksize:
            print(f"{player.username} has {len(player.deck)} cards in their deck.")
            bad_lengths = True
        # player.n0()
    if bad_lengths:
        raise RuntimeError("ILLEGAL DECK")
    print("All decks lengths legal.")

    sortedplayers = sorted(players.values(), key=lambda x: x.username.lower())

    return sortedplayers


def process(decks: List[DeckEntry]):
    headers = ["Card", "Effect", "% of decks", "# played per deck", "# played total"]
    result_matrix = [headers]

    for card, effect in CARDS.items():
        played_per_deck, played_total = num_played(card, decks)
        row = [
            card,
            effect,
            round(deck_percent(card, decks) * 100, 2),
            round(played_per_deck, 2),
            played_total,
        ]
        result_matrix.append(row)

    return result_matrix


def deck_percent(cardname: str, decks: List[DeckEntry]) -> float:
    total = 0
    for deck in decks:
        if cardname in [card for card in deck.deck]:
            total += 1
    return total / len(decks)


def num_played(cardname: str, decks: List[DeckEntry]) -> (float, int):
    """
    returns average played per deck that ran it and total played overall
    :param cardname:
    :param decks:
    :return:
    """
    total = 0
    num_decks_playing = 0
    for deck in decks:
        all_played = [card for card in deck.deck if card == cardname]
        if all_played:
            total += len(all_played)
            num_decks_playing += 1
    return total / num_decks_playing, total


def main():
    conn = sheet.SheetConnection(secret=SECRET, scope=SCOPE)
    page = conn.get_page(
        sheet_name=SHEET_NAME,
        page_name=PAGE_NAME,
    )

    records = page.get_all_records()

    decks = get_decks(records, DECKSIZE)

    pprint.pprint(decks)

    result_matrix = process(decks)

    # pprint.pprint(result_matrix)

    with open("xerox2_analysis.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(result_matrix)


if __name__ == "__main__":
    main()
