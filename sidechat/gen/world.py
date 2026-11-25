"""What conversations are about: settings, agents, people, devices, registers.

Some settings and agent names are held out: conversations that use them go to the test split
only, so the test set measures settings and names the model never saw (scorecard item 14).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Setting:
    id: str
    scene: str  # what is going on, for the writer
    role: str  # the agent's role, as the request's `agent.role`
    leads: bool  # the agent runs the session (G6 "the agent leads")
    people: tuple[int, int]  # how many people, min and max
    topics: tuple[str, ...]
    controls: tuple[str, ...] = ()  # things the agent can set or play (timers, music, calls)
    devices: bool = False  # other voice devices are plausibly around
    heldout: bool = False
    # gen-0.6: what a device in a room does on its own screen, board or bench, which the people
    # cannot do instead. Only such a setting has `device_request` and the kinds around it
    # (`planner._allowed`). A role may name more than this (music, a timer, a story): a person
    # could see to those as well, so a request for one with no name stays an even call (SD-32),
    # and they are left out here.
    abilities: tuple[str, ...] = ()


def _local_settings(name: str) -> tuple[Setting, ...]:
    """Settings whose definitions are kept out of this repository (`world_local.py`, when it is there)."""
    try:
        from sidechat.gen import world_local
    except ImportError:
        return ()
    return tuple(Setting(**kw) for kw in getattr(world_local, name, ()))


SETTINGS: tuple[Setting, ...] = (
    Setting(
        "team_meeting",
        "a team meeting on a video call",
        "AI assistant on the call",
        False,
        (3, 5),
        (
            "a product launch",
            "next quarter's budget",
            "a hiring plan",
            "a website redesign",
            "an office move",
            "a customer complaint",
        ),
    ),
    Setting(
        "standup",
        "a daily standup on a video call",
        "AI assistant on the call",
        False,
        (3, 5),
        ("a release that slipped", "a flaky test", "a database migration", "sprint goals", "an on-call handover"),
    ),
    Setting(
        "sales_call",
        "a sales call between a vendor's rep and two customers",
        "the vendor's AI assistant on the call",
        False,
        (3, 4),
        ("pricing for a software plan", "an integration question", "a renewal", "a security review", "a pilot project"),
    ),
    Setting(
        "support_call",
        "a household on a support call about a problem at home",
        "AI support agent for the provider",
        True,
        (2, 3),
        ("broadband dropping", "a broken washing machine", "a billing error", "a delayed delivery", "a boiler fault"),
    ),
    Setting(
        "family_kitchen",
        "a family cooking in the kitchen with a smart speaker",
        "smart speaker in the kitchen",
        False,
        (2, 4),
        ("dinner for six", "a birthday cake", "a Sunday roast", "school lunches", "a new recipe"),
        controls=("a timer", "music", "a shopping list"),
        devices=True,
    ),
    Setting(
        "car",
        "a family or friends on a drive with the car's assistant",
        "in-car voice assistant",
        False,
        (2, 4),
        ("a road trip", "the school run", "getting to a wedding", "finding petrol", "a detour"),
        controls=("navigation", "music", "a phone call"),
        devices=True,
    ),
    Setting(
        "study_group",
        "students in a study group with an AI tutor on hand",
        "AI tutor for the study group",
        False,
        (2, 4),
        ("calculus", "the French revolution", "photosynthesis", "statistics homework", "an essay plan"),
    ),
    Setting(
        "quiz_tutor",
        "an AI tutor running a quiz for a few students",
        "AI tutor running the quiz",
        True,
        (2, 3),
        ("capital cities", "the periodic table", "world history", "spelling", "mental arithmetic"),
    ),
    Setting(
        "podcast",
        "a podcast recording with a guest and an AI co-host",
        "AI co-host of the podcast",
        False,
        (2, 3),
        ("baking bread", "running a small business", "climbing", "urban gardening", "learning languages"),
    ),
    Setting(
        "tabletop_game",
        "friends playing a tabletop role-playing game run by an AI game master",
        "AI game master running the adventure",
        True,
        (3, 4),
        ("a haunted castle", "a heist", "a jungle temple", "a space station", "a dragon's lair"),
    ),
    Setting(
        "telehealth_intake",
        "a patient and a relative on a telehealth intake before the doctor joins",
        "AI intake assistant for the clinic",
        True,
        (2, 2),
        ("medications", "allergies", "a sore knee", "sleep problems", "a follow-up visit"),
    ),
    Setting(
        "incident_call",
        "engineers on an incident call",
        "AI assistant on the call",
        False,
        (3, 5),
        ("an outage", "rising error rates", "a failed deploy", "a full disk", "a security alert"),
    ),
    Setting(
        "friends_call",
        "friends catching up on a video call",
        "AI assistant on the call",
        False,
        (2, 4),
        ("weekend plans", "a quiz night", "a film to watch", "a birthday surprise", "a house move"),
    ),
    Setting(
        "hybrid_room",
        "a meeting room with a voice device and one person joining remotely",
        "the meeting room's voice assistant",
        False,
        (3, 4),
        ("a board update", "a project kickoff", "an interview debrief", "a training plan"),
        controls=("the screen", "the agenda"),
    ),
    Setting(
        "classroom",
        "a teacher and students with an AI teaching assistant",
        "AI teaching assistant",
        False,
        (3, 5),
        ("volcanoes", "fractions", "a poem", "the water cycle", "a science fair"),
    ),
    Setting(
        "trip_planning",
        "friends planning a trip together",
        "AI travel assistant on the call",
        False,
        (2, 4),
        ("a weekend in Lisbon", "a ski trip", "a camping trip", "a wedding abroad", "a train tour"),
    ),
    # held out: test only
    Setting(
        "onboarding",
        "an onboarding call with a new customer and the vendor's AI onboarding guide",
        "AI onboarding guide",
        True,
        (2, 3),
        ("setting up accounts", "importing data", "training the team", "connecting a calendar"),
        heldout=True,
    ),
    Setting(
        "book_club",
        "a book club meeting with an AI assistant on the call",
        "AI assistant on the call",
        False,
        (3, 5),
        ("a mystery novel", "a memoir", "a sci-fi classic", "next month's pick"),
        heldout=True,
    ),
)

# gen-0.6: a device in a room, asked for things mostly without its name. Each role says what the
# device does, in a few words (the small build reads the role with every line, in 96 tokens). Kept
# out of `SETTINGS`, so the default pool and every earlier corpus's plans are unchanged; drawn with
# `make_cast(pool=ROOM_POOL)`. One person alone with the device is common, so people start at 1.
ROOM_DEVICES: tuple[Setting, ...] = (
    Setting(
        "living_room_screen",
        "a household in the living room with a voice-controlled screen on the wall",
        "voice assistant in the living room's wall screen; it shows photos and videos, plays music and puts up a clock",
        False,
        (1, 4),
        ("a film night", "last summer's holiday photos", "a lazy Sunday", "tidying before guests arrive", "a match on later"),
        controls=("the photos on the screen", "the music", "the clock on the screen"),
        abilities=(
            "bring photos up on the screen",
            "play a video or a film on the screen",
            "change how things are shown on the screen (bigger, side by side, the next one, full screen)",
        ),
    ),
    Setting(
        "workout_mirror",
        "people working out at home in front of a voice-controlled mirror",
        "voice assistant in a workout mirror; it shows exercises, counts reps and times rounds",
        False,
        (1, 3),
        ("a morning stretch", "a circuit before work", "getting back into running", "a sore shoulder", "a plank challenge"),
        controls=("the exercise on the mirror", "the rep count", "the round timer"),
        abilities=(
            "show an exercise or a routine on the mirror",
            "count the reps or reset the count",
            "show their form or their progress on the mirror",
        ),
    ),
    Setting(
        "whiteboard",
        "colleagues in an office in front of a voice-controlled digital whiteboard",
        "voice assistant in the office's digital whiteboard; it draws diagrams, writes up notes and shows a timer",
        False,
        (1, 4),
        ("a system design", "a project timeline", "names for a product", "a retrospective", "a floor plan for the move"),
        controls=("the diagram on the board", "the notes on the board", "the timer on the board"),
        abilities=(
            "draw or change a diagram on the board",
            "write up or tidy the notes on the board",
            "move, resize or clear things on the board",
        ),
    ),
    Setting(
        "games_board",
        "a parent and children around a voice-controlled games board",
        "voice assistant in a games board; it sets up board games, keeps the score and tells stories",
        False,
        (1, 4),
        ("snakes and ladders", "a rainy afternoon", "a memory game", "a game of draughts", "a story before bed"),
        controls=("the game on the board", "the score"),
        abilities=(
            "set up or clear a game on the board",
            "keep or correct the score",
            "move a piece or take back a move on the board",
        ),
    ),
    Setting(
        "workshop_projector",
        "people in a home workshop with a voice-controlled projector over the bench",
        "voice assistant in the workshop's bench projector; it shows plans and measurements and sets timers",
        False,
        (1, 3),
        ("a bookshelf", "a bird box", "mending a chair", "a bike repair", "a picture frame"),
        controls=("the plan on the bench", "the glue timer"),
        abilities=(
            "show a plan or a cutting list on the bench",
            "mark a measurement or an angle on the bench",
            "zoom in on or move what is shown on the bench",
        ),
    ),
)
# The settings above are the ones this repository defines. gen-0.6 also has a held-out setting,
# written only for its test split, that is not published: it is added here when its definition is
# on this machine, and its lines are left out of the public dataset (`pipeline/dataset.py`).
OWN_IDS = frozenset(s.id for s in (*SETTINGS, *ROOM_DEVICES))
ROOM_DEVICES = (*ROOM_DEVICES, *_local_settings("ROOM_DEVICES"))
# With the three earlier settings where a device shares a room with people. They have no abilities,
# so they get only the people's side: talk that carries on after the device speaks.
ROOM_POOL: tuple[Setting, ...] = (
    *ROOM_DEVICES,
    *(s for s in SETTINGS if s.id in ("family_kitchen", "car", "hybrid_room")),
)
ROOM_IDS = frozenset(s.id for s in ROOM_POOL)
ALL_SETTINGS: tuple[Setting, ...] = (*SETTINGS, *ROOM_DEVICES)

# Agent names. Word-like names make "the name as an ordinary word" possible (G5). Each may have
# speech-to-text mishearings as aliases. Duplex-MPE's "Aria" and Ambient Bench's "alfi" are left
# out so those benchmarks stay unseen.
AGENTS: dict[str, tuple[str, ...]] = {
    "Atlas": ("at last",),
    "Nova": ("no va",),
    "Echo": ("eco",),
    "Sage": (),
    "Juno": ("june oh",),
    "Max": ("macs",),
    "Rook": ("rook's",),
    "Ivy": ("ivey",),
    "Orion": ("o ryan",),
    "Iris": (),
    "Remy": ("remmy",),
    "Kai": ("kye",),
    "Pip": (),
    "Milo": ("my low",),
    "Luna": (),
    "Quinn": ("quin",),
    "Ada": ("aider",),
    "Bea": ("bee",),
    "Penny": (),
    "Ace": (),
    "Bolt": (),
    "Clover": (),
    "Dash": (),
    "Ember": (),
    "Frankie": (),
    "Gus": (),
    "Hugo": (),
    "Indy": (),
}
WORDLIKE = {
    "Echo",
    "Sage",
    "Max",
    "Pip",
    "Penny",
    "Ace",
    "Bolt",
    "Clover",
    "Dash",
    "Ember",
    "Ivy",
    "Rook",
    "Iris",
    "Luna",
    "Bea",
}
HELDOUT_AGENTS: dict[str, tuple[str, ...]] = {"Wren": ("ren",), "Otto": ("auto",), "Cleo": (), "Tess": ("tess's",)}
UNNAMED = ("the assistant", "the AI", "the bot")  # an agent with no name, called by its role
SOUNDALIKE = {
    "Nova": "Noah",
    "Juno": "June",
    "Max": "Mac",
    "Ivy": "Evie",
    "Remy": "Rémi",
    "Kai": "Kay",
    "Milo": "Myla",
    "Luna": "Lana",
    "Quinn": "Gwen",
    "Ada": "Aida",
    "Bea": "Dee",
    "Iris": "Isis",
    "Hugo": "Hugh",
    "Atlas": "Alice",
    "Orion": "Ryan",
    "Echo": "Eko",
    "Wren": "Ren",
    "Otto": "Ottie",
    "Cleo": "Chloe",
    "Tess": "Jess",
}

PEOPLE = (
    "Jon",
    "Sam",
    "Priya",
    "Maya",
    "Tom",
    "Lena",
    "Dana",
    "Chris",
    "Mei",
    "Raj",
    "Anita",
    "Paul",
    "Karen",
    "Ella",
    "Leo",
    "Nina",
    "Theo",
    "Amy",
    "Ben",
    "Chloe",
    "Marco",
    "Tess",
    "Kit",
    "Zoe",
    "Finn",
    "Harold",
    "Kate",
    "Omar",
    "Jill",
    "Wes",
    "Grace",
    "Hugo",
    "Bea",
    "Cal",
    "Dev",
    "Ruth",
    "Olu",
    "Jack",
    "Mira",
    "Greg",
    "Hana",
    "Ines",
    "Ivo",
    "Sue",
    "Raf",
    "Ken",
    "Lucy",
    "Ravi",
    "Marta",
    "Aisha",
    "Tariq",
    "Sofia",
    "Diego",
    "Yuki",
    "Hiro",
    "Fatima",
    "Kwame",
    "Ngozi",
    "Lars",
    "Ingrid",
    "Pedro",
    "Lucia",
    "Anna",
    "Mateo",
    "Zara",
    "Imran",
    "Chen",
    "Wei",
    "Sara",
    "Noor",
    "Elif",
    "Can",
    "Oskar",
    "Freya",
    "Malik",
    "Joy",
    "Femi",
    "Ada",
    "Rosa",
    "Pablo",
    "Eli",
    "Noa",
    "Tomas",
    "Petra",
    "Ivan",
    "Olga",
    "Rhys",
    "Siobhan",
    "Connor",
    "Aoife",
    "Mohammed",
    "Leila",
    "Arjun",
    "Divya",
    "Kofi",
    "Abena",
    "Nils",
    "Astrid",
    "Jamal",
    "Tanya",
    "Victor",
)
DEVICES = ("Hey Siri", "OK Google", "Hey Google", "Alexa", "Hey Cortana", "Hey TV", "OK car")
REGISTERS = (
    "casual and friendly",
    "businesslike and brisk",
    "chatty, with fillers like 'um', 'like', 'you know'",
    "terse, people speak in short fragments",
    "warm and joking",
    "spoken naturally, with false starts and self-corrections",
)


@dataclass
class Cast:
    setting: Setting
    agent: str  # the name, or "Assistant" for an unnamed agent
    aliases: tuple[str, ...]
    unnamed: bool
    people: list[str]
    topic: str
    register: str
    soundalike: str | None = None  # a person whose name sounds like the agent's, if any
    heldout: list[str] = field(default_factory=list)  # why this cast is test-only

    @property
    def calls(self) -> tuple[str, ...]:
        """Every way of calling the agent."""
        return (*UNNAMED,) if self.unnamed else (self.agent, *self.aliases)


def make_cast(
    rng, setting: Setting | None = None, test_only: bool = False, pool: tuple[Setting, ...] | None = None
) -> Cast:
    """A random cast. `test_only` may draw held-out settings and names. `pool` draws the setting
    from other settings than the default ones (gen-0.6: `ROOM_POOL`)."""
    pool = [s for s in (pool or SETTINGS) if test_only or not s.heldout]
    setting = setting or rng.choice(pool)
    heldout = ["setting"] if setting.heldout else []
    unnamed = rng.random() < 0.08
    names = dict(AGENTS)
    if test_only and rng.random() < 0.4:
        names = dict(HELDOUT_AGENTS)
    if unnamed:
        agent, aliases = "Assistant", ()
    else:
        agent = rng.choice(sorted(names))
        aliases = names[agent]
        if agent in HELDOUT_AGENTS:
            heldout.append("agent_name")
    n = rng.randint(*setting.people)
    people = rng.sample([p for p in PEOPLE if p != agent], n)
    soundalike = None
    if not unnamed and agent in SOUNDALIKE and rng.random() < 0.25:
        soundalike = SOUNDALIKE[agent]
        people[rng.randrange(n)] = soundalike
    return Cast(
        setting, agent, aliases, unnamed, people, rng.choice(setting.topics), rng.choice(REGISTERS), soundalike, heldout
    )
