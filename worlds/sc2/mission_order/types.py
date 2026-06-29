"""
Types used throughout the mission order package.
"""

from typing import TypedDict, Literal, NotRequired, Required, final


@final
class SubRuleEntryRuleDict(TypedDict):
    rules: list['EntryRuleDict']
    amount: NotRequired[int]


@final
class MissionCountEntryRuleDict(TypedDict):
    scope: str
    amount: int


@final
class BeatMissionsEntryRuleDict(TypedDict):
    scope: list[str] | str


@final
class ItemsEntryRuleDict(TypedDict):
    items: dict[str, int]


EntryRuleDict = SubRuleEntryRuleDict | MissionCountEntryRuleDict | BeatMissionsEntryRuleDict | ItemsEntryRuleDict
DifficultyType = Literal["relative", "starter", "easy", "medium", "hard", "very hard"]


class MissionSlotDict(TypedDict, total=False):
    index: Required[int | str | list[str | int]]
    entrance: bool
    exit: bool
    goal: bool
    empty: bool
    next: list[int | str]
    entry_rules: list[EntryRuleDict]
    mission_pool: set[str] | list[str] | str
    difficulty: DifficultyType
    victory_cache: int
    heroes: list[str]


class LayoutDict(TypedDict, total=False):
    # Naming
    display_name: str | list[str]
    unique_name: bool
    # Layout Type
    type: Literal["column", "grid", "hopscotch", "gauntlet", "blitz", "canvas"]
    size: int
    # Links
    exit: bool
    goal: bool
    entry_rules: list[EntryRuleDict]
    unique_progression_track: int
    # Mission pool
    mission_pool: list[str]
    min_difficulty: DifficultyType
    max_difficulty: DifficultyType
    # missions
    missions: list[MissionSlotDict]


# Note(mm): extra_items added in 3.15 to express the layout name keys, but that's not available to AP yet.
CampaignDict = dict[str, LayoutDict]
