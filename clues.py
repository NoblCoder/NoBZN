"""Conservative offline clue lookup; never invent answers for unknown clues."""
import re

# Small starter bank. Extend with a JSON clue_database mapping for real puzzles.
STARTER_CLUES = {
    "feline pet": ["CAT"], "canine pet": ["DOG"],
    "automobile": ["CAR", "AUTO"], "number after nine": ["TEN"],
    "tin container": ["CAN"], "moved quickly on foot": ["RAN"],
    "opposite of yes": ["NO"], "opposite of down": ["UP"],
    "frozen water": ["ICE"], "our star": ["SUN"],
    "baker's appliance": ["OVEN"], "capital of france": ["PARIS"],
}


def normalize_clue(clue):
    return re.sub(r"[^a-z0-9]+", " ", clue.lower()).strip()


def clue_candidates(grid, clues, explicit, database=None):
    bank = {normalize_clue(k): v for k, v in STARTER_CLUES.items()}
    bank.update({normalize_clue(k): v for k, v in (database or {}).items()})
    result = dict(explicit)
    for sid, clue in clues.items():
        if sid not in grid.slots:
            raise ValueError(f"Unknown clue slot: {sid}")
        if not isinstance(clue, str):
            raise ValueError(f"Clue for {sid} must be text")
        if sid not in result:
            answers = bank.get(normalize_clue(clue))
            if answers is None:
                raise ValueError(f"No offline answers for {sid}: {clue!r}. "
                                 "Add candidates or a clue_database entry.")
            result[sid] = [w for w in answers if len(re.sub(r"[\s'-]", "", w)) == grid.slots[sid].length]
    for sid, answers in result.items():
        if sid not in grid.slots:
            raise ValueError(f"Unknown candidate slot: {sid}")
        if not isinstance(answers, list) or not answers or any(not isinstance(w, str) for w in answers):
            raise ValueError(f"Candidates for {sid} must be a nonempty list of answers")
        normalized = [re.sub(r"[\s'-]", "", w).upper() for w in answers]
        if any(not re.fullmatch(r"[A-Z]+", w) or len(w) != grid.slots[sid].length for w in normalized):
            raise ValueError(f"Answers for {sid} must have {grid.slots[sid].length} A-Z letters")
        result[sid] = normalized
    if clues:
        missing = set(grid.slots) - set(result)
        if missing:
            raise ValueError(f"Clued puzzles need clues or candidates for every slot: {sorted(missing)}")
    return result
