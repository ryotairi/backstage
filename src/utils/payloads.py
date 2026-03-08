from typing import Any


def convert_deck_to_sekai_deck(deck: dict[str, Any]) -> dict[str, Any]:
    """Convert a UserDeck database record to the Sekai payload format."""
    members = deck["members"]
    return {
        "userId": deck["userId"],
        "deckId": deck["deckId"],
        "name": deck["name"],
        "leader": members[0] if len(members) > 0 else 0,
        "subLeader": members[1] if len(members) > 1 else 0,
        "member1": members[0] if len(members) > 0 else 0,
        "member2": members[1] if len(members) > 1 else 0,
        "member3": members[2] if len(members) > 2 else 0,
        "member4": members[3] if len(members) > 3 else 0,
        "member5": members[4] if len(members) > 4 else 0,
    }
