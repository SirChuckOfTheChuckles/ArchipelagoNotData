"""
Types used throughout the mission order package.
"""

from typing import TypedDict, Literal, NotRequired, Required, final


@final
class SubRuleEntryRulePresetDict(TypedDict):
    rules: list['EntryRulePresetDict']
    amount: NotRequired[int]  # >= -1


@final
class MissionCountEntryRulePresetDict(TypedDict):
    scope: str | list[str]
    amount: NotRequired[int]  # >= -1, default: -1, -1 means all


@final
class ItemsEntryRuleDict(TypedDict):
    items: dict[str, int]


EntryRulePresetDict = (
    SubRuleEntryRulePresetDict
    | MissionCountEntryRulePresetDict
    | ItemsEntryRuleDict
)


@final
class SubRuleEntryRuleDict(TypedDict):
    rules: list['EntryRuleDict']
    amount: int  # >= 0


@final
class MissionCountEntryRuleDict(TypedDict):
    scope: list[str]
    amount: int  # >= 0


EntryRuleDict = (
    SubRuleEntryRuleDict
    | MissionCountEntryRuleDict
    | ItemsEntryRuleDict
)

DifficultyType = Literal["relative", "starter", "easy", "medium", "hard", "very hard"]


class MissionSlotPresetDict(TypedDict, total=False):
    index: Required[int | str | list[str | int]]
    entrance: bool
    exit: bool
    goal: bool
    empty: bool
    next: list[int | str]
    entry_rules: list[EntryRulePresetDict]
    mission_pool: set[str] | list[str] | str
    difficulty: DifficultyType
    victory_cache: int  # 0-10
    heroes: list[str]


class MissionSlotDict(TypedDict, total=False):
    index: Required[list[str | int]]
    entrance: bool
    exit: bool
    goal: bool
    empty: bool
    next: list[int | str]
    entry_rules: list[EntryRuleDict]
    mission_pool: set[int]
    difficulty: int  # 0-5, numeric value of difficulty pools
    victory_cache: int  # 0-10
    heroes: list[str]


class LayoutPresetDict(TypedDict, total=False):
    # Naming
    display_name: str | list[str]
    unique_name: bool
    # Layout Type
    type: Literal["column", "grid", "hopscotch", "gauntlet", "blitz", "canvas"]
    size: int  # >=1
    # Links
    exit: bool
    goal: bool
    entry_rules: list[EntryRulePresetDict]
    unique_progression_track: int
    # Mission pool
    mission_pool: list[str]
    min_difficulty: DifficultyType
    max_difficulty: DifficultyType
    # missions
    missions: list[MissionSlotPresetDict]
    # layout type-specific
    width: int
    two_start_positions: bool
    canvas: list[str]
    jump_distance_orthogonal: int
    jump_distance_diagonal: int
    spacer: int


class LayoutDict(TypedDict):
    # Naming
    display_name: list[str]
    unique_name: bool
    # Layout Type
    type: str
    size: int  # >=1
    # Links
    exit: bool
    goal: bool
    entry_rules: list[EntryRuleDict]
    unique_progression_track: int
    # Mission pool
    mission_pool: set[int]
    min_difficulty: int
    max_difficulty: int
    # missions
    missions: list[MissionSlotDict]
    # layout type-specific
    width: NotRequired[int]
    two_start_positions: NotRequired[bool]
    canvas: NotRequired[list[str]]
    jump_distance_orthogonal: NotRequired[int]
    jump_distance_diagonal: NotRequired[int]
    spacer: NotRequired[int]


CampaignPresetDict = TypedDict("CampaignPresetDict", {
    "display_name": str | list[str],
    "unique_name": bool,
    "entry_rules": list[EntryRulePresetDict],
    "unique_progression_track": int,
    "goal": bool,
    "min_difficulty": DifficultyType,
    "max_difficulty": DifficultyType,
    "layouts": dict[str, LayoutPresetDict],
    # Included in preset data but stripped by option parsing
    "preset": str,
    "global": dict,
    # Only if there is a preset
    "size": int,
    "two_start_positions": bool,
    "missions": Literal["random", "vanilla_shuffled", "vanilla"],
    "shuffle_raceswaps": bool,
    "keys": str,
}, total=False)


CampaignDict = TypedDict("CampaignDict", {
    "display_name": list[str],
    "unique_name": bool,
    "entry_rules": list[EntryRuleDict],
    "unique_progression_track": int,
    "goal": bool,
    "min_difficulty": int,
    "max_difficulty": int,
    # Specific to campaigns with a preset
    "missions": NotRequired[str],  # random, vanilla_shuffled, vanilla
    # "Not user-facing; adapted from the free-string keys used to specify layouts"""
    "layouts": dict[str, LayoutDict],
    # Unique to processed option
    # Not user-facing; used to modify search paths so an extra nested layer isn't artificially added"""
    "single_layout_campaign": bool,
})
