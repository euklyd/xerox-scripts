from dataclasses import dataclass, field

from typing import List, Dict

CARDNAME = "Card Name"
RESTR = "Restr."
PRIO = "Prio"
RULES_TEXT = "Rules Text"
BENE = "B"
HARM = "H"
SHORTHAND = "Effect Shorthand"
COST = "Cost"
DRAW = "Draw"
NEXT_NIGHT = "Next-night discard"


@dataclass
class Action:
    name: str
    text: str
    prio: str
    b_h: str
    ninja: bool = False


@dataclass
class Card:
    name: str
    short_text: str
    long_text: str
    prio: str
    b_h: str

    cost: str = ""
    draw: str = ""
    next_night: str = ""
    restr: int = 0

    actions: List[Action] = field(default_factory=list)

    @staticmethod
    def from_record(record: Dict[str, str]) -> "Card":
        h = record[HARM].lower() == "true"
        b = record[BENE].lower() == "true"
        if b and h:
            b_h = "B/H"
        elif b:
            b_h = "B"
        elif h:
            b_h = "H"
        else:
            b_h = ""

        return Card(
            name=record[CARDNAME],
            restr=int(record[RESTR]),
            prio=record[PRIO],
            long_text=record[RULES_TEXT],
            short_text=record[SHORTHAND],
            b_h=b_h,
            actions=[
                Action(
                    name=record[CARDNAME],
                    prio=record[PRIO],
                    text=record[SHORTHAND],
                    b_h=b_h,
                )
            ],
            cost=record[COST],
            draw=record[DRAW],
            next_night=record[NEXT_NIGHT],
        )


CARDS = {
    '"Graceful" Charity': Card(
        name='"Graceful" Charity',
        short_text="",
        long_text="ALIAS takes 3 damage. | Draw one card, then discard one card the next night. ",
        prio="Dmg",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night=1,
        restr=3,
        actions=[Action(name='"Graceful" Charity', text="", prio="Dmg", b_h="H")],
    ),
    "A Vest For Plusle's Life": Card(
        name="A Vest For Plusle's Life",
        short_text="discard 2 or pay 2 hp [can mix and match]: 1 atk / 3 hp npc maker. max 2 npcs at once.",
        long_text="Take 2 nonlethal damage at the end of Damaging priority. This can be reduced by discarding 1 or 2 cards, reducing damage by the number of cards discarded. | Create a 1/3 Plusle NPC with an alias of your choice. *(An NPC alias with 1 Atk and 3 HP.)* If its owner's shot is disrupted, Plusle's shot also fails.\nYou cannot have more than two Plusle NPC's at once. *(The second is a Minun.)*",
        prio="Dmg/Low",
        b_h="N",
        cost="2 [hp or cards]",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="A Vest For Plusle's Life",
                text="discard 2 or pay 2 hp [can mix and match]: 1 atk / 3 hp npc maker. max 2 npcs at once.",
                prio="Dmg/Low",
                b_h="N",
            ),
        ],
    ),
    "Burst Stream of Destruction": Card(
        name="Burst Stream of Destruction",
        short_text="docbusterizer. draw 1.",
        long_text='ALIAS gains the following ability: "Your shot target loses protection equal to your Atk". | Draw a card.',
        prio="Util",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Burst Stream of Destruction",
                text="docbusterizer. draw 1.",
                prio="Util",
                b_h="B",
            )
        ],
    ),
    "Checker Bribery": Card(
        name="Checker Bribery",
        short_text="free card. tutor 1.",
        long_text='As an additional cost to cast this spell, discard a card. This card does not count against your action limit. | At "instant speed", search your library for a card and put that card into your hand. (You may use the searched card on the same night.)',
        prio="Inst",
        b_h="N",
        cost=1,
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Checker Bribery", text="free card. tutor 1.", prio="Inst", b_h="N", ninja=True
            )
        ],
    ),
    "Cockroach Strats": Card(
        name="Cockroach Strats",
        short_text="draw 1 (+1 if hellbent).",
        long_text="Draw 1 card. Create a 0/1 NPC with an alias of your choice. It dies at the end of the next night.  *Hellbent:* If you have no cards in your hand, draw an additional card.",
        prio="Low",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Cockroach Strats",
                text="draw 1 (+1 if hellbent).",
                prio="Low",
                b_h="N",
            )
        ],
    ),
    "Cop of Greed": Card(
        name="Cop of Greed",
        short_text="hand cop. draw 2.",
        long_text="Learn all cards in ALIAS's hand. | Draw two cards. ",
        prio="Low",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[
            Action(name="Cop of Greed", text="hand cop. draw 2.", prio="Low", b_h="N")
        ],
    ),
    "Disposable Gavin": Card(
        name="Disposable Gavin",
        short_text="6 hp doc. if dmg >= doc amt, draw 1.",
        long_text="ALIAS is protected against 6 damage. | If damage on ALIAS is equal to or exceeds their total protection tonight, draw a card.",
        prio="Util",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Disposable Gavin",
                text="6 hp doc. if dmg >= doc amt, draw 1.",
                prio="Util",
                b_h="B",
            )
        ],
    ),
    "Everyone's Friend": Card(
        name="Everyone's Friend",
        short_text="abil motivate (shot motivate on plusles). draw 1.",
        long_text="ALIAS may use an additional card the next night. If ALIAS is a Plusle, it may submit an additional shot instead. | Draw a card.",
        prio="Low",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Everyone's Friend",
                text="abil motivate (shot motivate on plusles). draw 1.",
                prio="Low",
                b_h="B",
            )
        ],
    ),
    "Frantic Search": Card(
        name="Frantic Search",
        short_text="discard 1: draw 2",
        long_text="As an additional cost to cast this spell, discard a card. Other cards you play this night are ninja. Draw 2 cards.",
        prio="Low",
        b_h="N",
        cost=1,
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(name="Frantic Search", text="discard 1: draw 2", prio="Low", b_h="N")
        ],
    ),
    "Good News I Drew You a Card": Card(
        name="Good News I Drew You a Card",
        short_text="1 dmg nl vig. mutual draw 1.",
        long_text="ALIAS takes 1 nonlethal strongman damage and draws 1 card. Draw 1 card.",
        prio="Dmg",
        b_h="B/H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Good News I Drew You a Card",
                text="1 dmg nl vig. mutual draw 1.",
                prio="Dmg",
                b_h="B/H",
            )
        ],
    ),
    "Gravedigging Gravedigs": Card(
        name="Gravedigging Gravedigs",
        short_text="",
        long_text="You may cast an additional spell tonight, but it must be a token ability *(all token abilities are from Madness cards)*. This card does not count against your action limit.",
        prio="Inst",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[Action(name="Gravedigging Gravedigs", text="self-moti for tokens", prio="Inst", b_h="B")],
    ),
    "Harpie's Sheep Typhoon": Card(
        name="Harpie's Sheep Typhoon",
        short_text="shotblock. if two of ~ used on same alias, fb.",
        long_text='ALIAS\'s standard shot fails. | *Entwine:* If any two "Mystical Sheep Typhoon" cards are successfully played on the same player, that player is fullblocked instead. | *This card\'s name is treated as "Mystical Sheep Typhoon" for deckbuilding purposes.*',
        prio="Disr",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Harpie's Sheep Typhoon",
                text="shotblock. if two of ~ used on same alias, fb.",
                prio="Disr",
                b_h="H",
            )
        ],
    ),
    "Helping Hand": Card(
        name="Helping Hand",
        short_text="shot motivate. if on own plusle, perma +1 atk. doesn't stack.",
        long_text="ALIAS may use their standard shot an additional time the next night. If ALIAS is **your own** Plusle, it also permanently gains 1 Atk. Additional copies of ~ on the same alias during the same night have no effect. Plusles cannot gain the bonus more then once.",
        prio="Low",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[
            Action(
                name="Helping Hand",
                text="shot motivate. if on own plusle, perma +1 atk. doesn't stack.",
                prio="Low",
                b_h="B",
            )
        ],
    ),
    "I Hope This Finds You Well": Card(
        name="I Hope This Finds You Well",
        short_text="abil disable + force discard 1",
        long_text="On the next night, ALIAS discards a card and cannot submit their abilities.",
        prio="Low",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="I Hope This Finds You Well",
                text="abil disable + force discard 1",
                prio="Low",
                b_h="H",
            )
        ],
    ),
    "IDLE YOUR DOCS": Card(
        name="IDLE YOUR DOCS",
        short_text="3 hp jdoc",
        long_text="Protect ALIAS against 3 damage. All other protective effects on ALIAS fail. ",
        prio="Disr",
        b_h="B/H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(name="IDLE YOUR DOCS", text="3 hp jdoc", prio="Disr", b_h="B/H")
        ],
    ),
    "Literacy": Card(
        name="Literacy",
        short_text="hand cop + mimic.",
        long_text="Learn all cards in ALIAS's hand. | Choose a card you learned. You may cast a copy of that card as if it were your own. (This card counts as part of Literacy and does not take an extra action. Any costs on the copied card must still be paid.)",
        prio="Inst",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[
            Action(name="Literacy", text="hand cop + mimic.", prio="Inst", b_h="N", ninja=True),
            Action(name="Literacy", text="mimic.", prio="Varying", b_h="N")
        ],
    ),
    "Mystical Sleep Typhoon": Card(
        name="Mystical Sleep Typhoon",
        short_text="abilblock. if two of ~ used on same alias, fb.",
        long_text='ALIAS\'s Active abilities fail. | *Entwine:* If any two "Mystical Sheep Typhoon" cards are successfully played on the same player, that player is fullblocked instead. | *This card\'s name is treated as "Mystical Sheep Typhoon" for deckbuilding purposes.*',
        prio="Disr",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Mystical Sleep Typhoon",
                text="abilblock. if two of ~ used on same alias, fb.",
                prio="Disr",
                b_h="H",
            )
        ],
    ),
    "Ojama RAD": Card(
        name="Ojama RAD",
        short_text="discard x: x+1 vig",
        long_text="As an additional cost to cast this spell, discard X cards. ALIAS takes X+1 damage.",
        prio="Dmg",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[
            Action(name="Ojama RAD", text="discard x: x+1 vig", prio="Dmg", b_h="N")
        ],
    ),
    "Pleading Face": Card(
        name="Pleading Face",
        short_text="shot rogue (strongwilled if hellbent).",
        long_text="Any shots ALIAS would use on you fail instead. Hellbent: If you have no cards in your hand, this action is strongwilled.",
        prio="Util",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="Pleading Face",
                text="shot rogue (strongwilled if hellbent).",
                prio="Util",
                b_h="H",
            )
        ],
    ),
    "Power Play": Card(
        name="Power Play",
        short_text="2 atk buff. if alias's shot kills, draw 1.\nif mutual: next-night atk+1.",
        long_text="ALIAS's Atk is increased by 2 until the end of the night. | If ALIAS's standard shot kills a player tonight, draw a card. | *Entwine:* If two players successfully target each other with ~, gain +1 Atk for the next night only.",
        prio="Util",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Power Play",
                text="2 atk buff. if alias's shot kills, draw 1.\nif mutual: next-night atk+1.",
                prio="Util",
                b_h="B",
            )
        ],
    ),
    "Sheep Shearing": Card(
        name="Sheep Shearing",
        short_text="2 hp transplant",
        long_text="ALIAS 1 takes 2 damage. | ALIAS 2 heals 2 damage at Low priority. *Reminder: You may not successfully heal a single alias for more than 4 HP.*",
        prio="Dmg/Low",
        b_h="B/H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Sheep Shearing (vig)", text="2 hp transplant - dmg", prio="Dmg", b_h="H"
            ),
            Action(
                name="Sheep Shearing (heal)", text="2 hp transplant - heal", prio="Low", b_h="B"
            )
        ],
    ),
    "Sheep with a Gun": Card(
        name="Sheep with a Gun",
        short_text="1 dmg vig. madness: 2 dmg vig token.",
        long_text='ALIAS takes 1 damage. | *Madness:* Gain a 1x "2 Atk vig" token.',
        prio="Dmg",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Sheep with a Gun",
                text="1 dmg vig. madness: 2 dmg vig token.",
                prio="Dmg",
                b_h="H",
            )
        ],
    ),
    "Sheep, MD": Card(
        name="Sheep, MD",
        short_text="2 hp doc. madness: 4 hp doc token.",
        long_text='2 Dmg doc. | *Madness:* Gain a 1x "4 Dmg doc" token.',
        prio="Util",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Sheep, MD",
                text="2 hp doc. madness: 4 hp doc token.",
                prio="Util",
                b_h="B",
            )
        ],
    ),
    "Sorry For Shooting You Monde": Card(
        name="Sorry For Shooting You Monde",
        short_text="hp cop + watch. draw 1 (2 if even number of mondes used)",
        long_text='Learn ALIAS\'s HP, along with which aliases visited them. Draw a card. | If you have used an even number of "Monde" cards, draw an additional card.',
        prio="Low",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="Sorry For Shooting You Monde",
                text="hp cop + watch. draw 1 (2 if even number of mondes used)",
                prio="Low",
                b_h="N",
            )
        ],
    ),
    "Step on Me!": Card(
        name="Step on Me!",
        short_text="discard 2: flex hijack",
        long_text="As an additional cost to cast this spell, discard 2 cards. | Choose one:\n• Redirect ALIAS 1's shot to ALIAS 2. \n• Redirect ALIAS 1's harmful abilities to ALIAS 2 and beneficial abilities to ALIAS 3. *(If an ability is both, it is considered harmful.)*",
        prio="Disr",
        b_h="H",
        cost=2,
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="Step on Me! (src)", text="discard 2: flex hijack", prio="Disr", b_h="H"
            ),
            Action(
                name="Step on Me! (dest - h)", text="flex hijack h-dest", prio="Disr", b_h="H", ninja=True
            ),
            Action(
                name="Step on Me! (dest - b)", text="flex hijack b-dest (non-h)", prio="Disr", b_h="H", ninja=True
            )
        ],
    ),
    "Talking to TBZ": Card(
        name="Talking to TBZ",
        short_text="2 dmg vig. 3-cards poison.",
        long_text="ALIAS takes 2 damage. On the next night, ALIAS takes damage equal to 3 minus the current number of cards in your hand, (min. 0).",
        prio="Dmg/Delayed",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=1,
        actions=[
            Action(
                name="Talking to TBZ (vig)",
                text="2 dmg vig",
                prio="Dmg/ Delayed",
                b_h="H",
            ),
            Action(
                name="Talking to TBZ (poison)",
                text="poison for (3 - cards).",
                prio="Low",
                b_h="H",
            )
        ],
    ),
    "Thunderdome Elliptical": Card(
        name="Thunderdome Elliptical",
        short_text="discard 1: 8/3 nl hurtyjail",
        long_text="As an additional cost to cast this spell, discard a card. | ALIAS is protected against 8 damage and their actions fail. ALIAS takes 3 nonlethal strongman damage *(at the end of Damaging priority)* if this ability is successful. ",
        prio="Disr",
        b_h="H",
        cost=1,
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="Thunderdome Elliptical (jail)",
                text="discard 1: 8/3 nl hurtyjail",
                prio="Disr",
                b_h="H",
            ),
            Action(
                name="Thunderdome Elliptical (dmg)",
                text="hurtyjail (3 nl sm dmg)",
                prio="Dmg",
                b_h="H",
            )
        ],
    ),
    "Tunnel Vision": Card(
        name="Tunnel Vision",
        short_text="flex empower",
        long_text="ALIAS's abilities or standard shot (choose one) are strongwilled.",
        prio="Disr",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(name="Tunnel Vision (shot)", text="flex empower (shot)", prio="Util", b_h="B"),
            Action(name="Tunnel Vision (cards)", text="flex empower (cards)", prio="Disr", b_h="B")
        ],
    ),
    "Upstart Goblin": Card(
        name="Upstart Goblin",
        short_text="3 hp heal. if hp after heal < max OR if mutual heal successful, draw 1.",
        long_text="ALIAS regains 3 HP. *Reminder: You may not successfully heal a single alias for more than 4 HP.* | If ALIAS has less than 12 HP at the end of the night: draw a card. | *Entwine:* Alternatively, if two players successfully target each other with ~ and both heal HP, draw even at full HP.",
        prio="Low",
        b_h="B",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Upstart Goblin",
                text="3 hp heal. if hp after heal < max OR if mutual heal successful, draw 1.",
                prio="Low",
                b_h="B",
            )
        ],
    ),
    "We Didn't Shoot You Monde": Card(
        name="We Didn't Shoot You Monde",
        short_text="alias cop + track. draw 1 (2 if even number of mondes used)",
        long_text='Learn ALIAS\'s username, along with which aliases they visited. Draw a card. | If you have used an even number of "Monde" cards, draw an additional card.',
        prio="Low",
        b_h="N",
        cost="",
        draw="FALSE",
        next_night="",
        restr=2,
        actions=[
            Action(
                name="We Didn't Shoot You Monde",
                text="alias cop + track. draw 1 (2 if even number of mondes used)",
                prio="Low",
                b_h="N",
            )
        ],
    ),
    "Wooly Sheep": Card(
        name="Wooly Sheep",
        short_text="1 atk debuff. madness: 2 atk debuff token.",
        long_text='1 Atk debuff. | *Madness:* Gain a 1x "2 Atk debuff" token.',
        prio="Util",
        b_h="H",
        cost="",
        draw="FALSE",
        next_night="",
        restr=3,
        actions=[
            Action(
                name="Wooly Sheep",
                text="1 atk debuff. madness: 2 atk debuff token.",
                prio="Util",
                b_h="H",
            )
        ],
    ),
}
