"""
Contains the Custom Mission Order option. Also validates the option value, so generation can assume the data matches the specification.
"""

from __future__ import annotations
import random

from Options import OptionDict, Visibility, OptionError
from typing import (
    Any,
    Iterable,
    Callable,
    TYPE_CHECKING,
    TypeVar,
    overload,
    Self,
    Type,
    Mapping,
    cast,
    overload,
)
import copy
import logging

from .. import locations
from ..mission_tables import lookup_name_to_mission
from ..mission_groups import mission_groups
from ..item.item_tables import item_table
from ..item import item_groups
from ..tables import HeroOptions
from . import layout_types
from .mission_pools import Difficulty
from . import presets_scripted, presets_static

if TYPE_CHECKING:
    from .types import (
        CampaignDict,
        CampaignPresetDict,
        LayoutDict,
        LayoutPresetDict,
        EntryRuleDict,
        MissionSlotDict,
    )


T = TypeVar("T")
U = TypeVar("U")

logger = logging.getLogger("Starcraft 2")

GENERIC_KEY_NAME = "Key".casefold()
GENERIC_PROGRESSIVE_KEY_NAME = "Progressive Key".casefold()
HERO_OPTION_VALUES = {
    HeroOptions.KERRIGAN.casefold(): HeroOptions.KERRIGAN,
    HeroOptions.NOVA.casefold(): HeroOptions.NOVA,
    HeroOptions.ARTANIS.casefold(): HeroOptions.ARTANIS,
}

PRESET_NONE = "none"
PRESET_OPTIONS: dict[str, Callable[[dict], 'CampaignPresetDict']] = {
    PRESET_NONE: lambda _: {},
    "wol + prophecy":      presets_static.static_preset(presets_static.preset_wol_with_prophecy),
    "wol":                 presets_static.static_preset(presets_static.preset_wol),
    "prophecy":            presets_static.static_preset(presets_static.preset_prophecy),
    "hots":                presets_static.static_preset(presets_static.preset_hots),
    "prologue":            presets_static.static_preset(presets_static.preset_lotv_prologue),
    "lotv prologue":       presets_static.static_preset(presets_static.preset_lotv_prologue),
    "lotv":                presets_static.static_preset(presets_static.preset_lotv),
    "epilogue":            presets_static.static_preset(presets_static.preset_lotv_epilogue),
    "lotv epilogue":       presets_static.static_preset(presets_static.preset_lotv_epilogue),
    "nco":                 presets_static.static_preset(presets_static.preset_nco),
    "mini wol + prophecy": presets_static.static_preset(presets_static.preset_mini_wol_with_prophecy),
    "mini wol":            presets_static.static_preset(presets_static.preset_mini_wol),
    "mini prophecy":       presets_static.static_preset(presets_static.preset_mini_prophecy),
    "mini hots":           presets_static.static_preset(presets_static.preset_mini_hots),
    "mini prologue":       presets_static.static_preset(presets_static.preset_mini_lotv_prologue),
    "mini lotv prologue":  presets_static.static_preset(presets_static.preset_mini_lotv_prologue),
    "mini lotv":           presets_static.static_preset(presets_static.preset_mini_lotv),
    "mini epilogue":       presets_static.static_preset(presets_static.preset_mini_lotv_epilogue),
    "mini lotv epilogue":  presets_static.static_preset(presets_static.preset_mini_lotv_epilogue),
    "mini nco":            presets_static.static_preset(presets_static.preset_mini_nco),
    "golden path":         presets_scripted.make_golden_path,
}
DIFFICULTY_OPTIONS = {
    "relative": Difficulty.RELATIVE.value,
    "starter": Difficulty.STARTER.value,
    "easy": Difficulty.EASY.value,
    "medium": Difficulty.MEDIUM.value,
    "normal": Difficulty.MEDIUM.value,
    "hard": Difficulty.HARD.value,
    "very hard": Difficulty.VERY_HARD.value,
}
GLOBAL_ENTRY = "global"

CONDITIONAL_LAYOUT_KEYS = {
    "column": ("size",),
    "grid": (
        "width",
        "two_start_positions",
        "size",
    ),
    "canvas": (
        "canvas",
        "jump_distance_orthogonal",
        "jump_distance_diagonal",
    ),
    "hopscotch": (
        "width",
        "spacer",
        "two_start_positions",
        "size",
    ),
    "gauntlet": ("width", "size",),
    "blitz": ("width", "size",),
}
LAYOUT_DICT_KEYS = (
    "display_name",
    "unique_name",
    "type",
    "exit",
    "goal",
    "entry_rules",
    "unique_progression_track",
    "mission_pool",
    "min_difficulty",
    "max_difficulty",
    "missions",
)
CAMPAIGN_DICT_KEYS = (
    "display_name",
    "unique_name",
    "preset",
    "entry_rules",
    "unique_progression_track",
    "goal",
    "min_difficulty",
    "max_difficulty",
    "single_layout_campaign",
)
MISSION_SLOT_KEYS = (
    "index",
    "entrance",
    "exit",
    "goal",
    "empty",
    "next",
    "entry_rules",
    "mission_pool",
    "difficulty",
    "victory_cache",
    "heroes",
)


def errormsg_invalid_type(option_name: str, value: Any, expected_type: Type | tuple[Type, ...]) -> str:
    value_printout = str(value)
    if len(value_printout) > 20:
        value_printout = value_printout[:16] + "[...]"
    if isinstance(expected_type, tuple):
        type_name = " or ".join(x.__name__ for x in expected_type)
    else:
        type_name = expected_type.__name__
    return (
        f"Option '{option_name}' got invalid type. "
        f"Expected {type_name}, got type {type(value).__name__}, value {value_printout}"
    )


def flatten(element: Any | list) -> Any:
    if isinstance(element, list):
        for subelement in element:
            yield from flatten(subelement)
    else:
        yield element


class ResolveOption:
    def __init__(self, option_name_prefix: str, key: str = "") -> None:
        self.value = None
        self.option_name = f"{option_name_prefix}.{key}"
        self.key = key

    def fallback(self, value: Any) -> Self:
        if self.value is None:
            self.value = value
        return self

    def fallback_from_dict(self, d: Mapping) -> Self:
        assert self.key
        if self.value is None:
            self.value = d.get(self.key)
        return self

    def replace_value(self, from_value: Any, to_value: Any) -> Self:
        if self.value == from_value:
            self.value = to_value
        return self

    def listify(self) -> Self:
        if self.value is None:
            return self
        if isinstance(self.value, list):
            return self
        self.value = [self.value]
        return self

    def require(self, target_type: Type[T]) -> T:
        if self.value is None:
            raise OptionError(f"Missing required value {self.option_name}")
        if not isinstance(self.value, target_type):
            raise OptionError(errormsg_invalid_type(self.option_name, self.value, target_type))
        return self.value

    def require_nullable(self, target_type: Type[T]) -> T | None:
        if self.value is None:
            return None
        if not isinstance(self.value, target_type):
            raise OptionError(errormsg_invalid_type(self.option_name, self.value, target_type))
        return self.value

    @overload
    def require_list_of(self, target_type: Type[T]) -> list[T]: ...
    @overload
    def require_list_of(self, target_type: tuple[Type[T], Type[U]]) -> list[T | U]: ...

    def require_list_of(self, target_type: Type[T] | tuple[Type[T], Type[U]]) -> list[T] | list[T | U]:
        value = self.require(list)
        for index, element in enumerate(value):
            if not isinstance(element, target_type):
                raise OptionError(errormsg_invalid_type(
                    f"{self.option_name}[{index}]", element, target_type)
                )
        return value

    @overload
    def require_nullable_list_of(self, target_type: Type[T]) -> list[T] | None: ...
    @overload
    def require_nullable_list_of(self, target_type: tuple[Type[T], Type[U]]) -> list[T | U] | None: ...

    def require_nullable_list_of(self, target_type: Type[T] | tuple[Type[T], Type[U]]) -> list[T] | list[T | U] | None:
        if self.value is None:
            return None
        return self.require_list_of(target_type)

    def require_string_enum(self, enum_options: list[str]) -> str:
        value = self.require(str)
        if value not in enum_options:
            raise OptionError(
                f"Option {self.option_name} got invalid value {value}. "
                f"Allowed values: {enum_options}"
            )
        return value

    def resolve_range(self) -> Self:
        if isinstance(self.value, str) and self.value.startswith("random-range-"):
            self.value = _custom_range(self.value, self.option_name)
        return self

    def flatten_list(self) -> Self:
        if self.value is None:
            return self
        assert isinstance(self.value, list)
        self.value = [x for x in flatten(self.value)]
        return self

    def map(self, func: Callable[[Any], Any], type_filter: Type | None = None) -> Self:
        if self.value is None:
            return self
        if type_filter is None or isinstance(self.value, type_filter):
            self.value = func(self.value)
        return self

    def assert_greater_than_equal_to(self, threshold: int, type_filter: Type = int) -> Self:
        if self.value is None:
            return self
        if isinstance(self.value, type_filter) and not (self.value >= threshold):
            raise OptionError(
                f"Option {self.option_name} got invalid value {self.value}. "
                f"Expected a value of at least {threshold}."
            )
        return self

    def assert_less_than_equal_to(self, threshold: int, type_filter: Type = int) -> Self:
        if self.value is None:
            return self
        if isinstance(self.value, type_filter) and not (self.value <= threshold):
            raise OptionError(
                f"Option {self.option_name} got invalid value {self.value}. "
                f"Expected a value of at most {threshold}."
            )
        return self


DEFAULT_CAMPAIGN_SETTINGS = {
    "display_name": "null",
    "unique_name": False,
    "entry_rules": [],
    "unique_progression_track": 0,
    "goal": True,
    "min_difficulty": "relative",
    "max_difficulty": "relative",
}
DEFAULT_LAYOUT_SETTINGS = {
    "display_name": "null",
    "unique_name": False,
    "entry_rules": [],
    "unique_progression_track": 0,
    "goal": False,
    "exit": False,
    "mission_pool": ["all missions"],
    "min_difficulty": "relative",
    "max_difficulty": "relative",
    "missions": [],
}


class CustomMissionOrder(OptionDict):
    """
    Used to generate a custom mission order. Please see documentation to understand usage.
    Will do nothing unless `mission_order` is set to `custom`.
    """
    display_name = "Custom Mission Order"
    visibility = Visibility.template
    value: dict[str, 'CampaignDict']
    default = {
        "Default Campaign": {
            **DEFAULT_CAMPAIGN_SETTINGS,
            GLOBAL_ENTRY: DEFAULT_LAYOUT_SETTINGS,
            "Default Layout": {
                "type": "grid",
                "size": 9,
            },
        },
    }

    def __init__(self, yaml_value: dict) -> None:
        # This function constructs self.value by parts,
        # so the parent constructor isn't called
        self.value: dict[str, 'CampaignDict'] = {}
        yaml_value = copy.deepcopy(yaml_value) # Ensure that all the mutations are local to the world

        # if not isinstance()

        for campaign_name, campaign_spec in yaml_value.items():
            if not isinstance(campaign_name, str):
                campaign_name = str(campaign_name)

            if not isinstance(campaign_spec, dict):
                raise OptionError(f"The top-level value of `custom_mission_order` must be a dictionary, got '{type(campaign_spec).__name__}'")

            # Check if this campaign has a layout type, making it a campaign-level layout
            single_layout_campaign = "type" in campaign_spec
            if single_layout_campaign:
                # Single-layout campaigns are not allowed to declare more layouts
                single_layout = {key: val for (key, val) in campaign_spec.items() if type(val) != dict}
                campaign_spec = {campaign_name: single_layout}
                # Campaign should inherit certain values from the layout
                if "goal" not in single_layout or not single_layout["goal"]:
                    campaign_spec["goal"] = False
                if "unique_progression_track" in single_layout:
                    campaign_spec["unique_progression_track"] = single_layout["unique_progression_track"]
                # Hide campaign name for single-layout campaigns
                campaign_spec["display_name"] = ""

            if "single_layout_campaign" in campaign_spec:
                raise OptionError(
                    f"Invalid use of reserved key 'single_layout_campaign' in campaign {campaign_name}. "
                    "Use a different name."
                )
            campaign_spec["single_layout_campaign"] = single_layout_campaign

            self.value[campaign_name] = _resolve_campaign_dict(f"custom_mission_order.{campaign_name}", campaign_spec)


def _resolve_campaign_dict(campaign_name: str, campaign_spec: dict[str, Any]) -> 'CampaignDict':
    # Check if this campaign has a global layout
    global_layout_spec: 'LayoutPresetDict' = {}
    for name in campaign_spec:
        if name.lower() == GLOBAL_ENTRY:
            global_layout_spec = campaign_spec.pop(name)
            break

    # Validate the global dict
    invalid_global_keys: list[str] = []
    for key in global_layout_spec:
        if key not in LAYOUT_DICT_KEYS:
            invalid_global_keys.append(key)
    if invalid_global_keys:
        raise OptionError(
            f"Invalid keys specified for global configuration of campaign {campaign_name}: "
            f"{invalid_global_keys}. Valid keys: {list(LAYOUT_DICT_KEYS)}"
        )

    # Split layouts from options
    layout_specs: dict[str, dict] = {}
    option_spec: dict[str, Any] = {}
    preset_options: dict[str, Any] = {}
    invalid_keys: list[str] = []
    for key, value in campaign_spec.items():
        if key in CAMPAIGN_DICT_KEYS:
            option_spec[key] = value
        elif key in presets_static.EXTRA_CAMPAIGN_DICT_KEYS + presets_scripted.EXTRA_CAMPAIGN_DICT_KEYS:
            preset_options[key] = value
        elif isinstance(value, dict):
            layout_specs[key] = value
        else:
            invalid_keys.append(key)
    if invalid_keys:
        raise OptionError(
            f"Campaign '{campaign_name}' had invalid keys: {invalid_keys}. "
            f"Layouts within the campaign must be dictionaries (have keys of their own). "
            f"Valid campaign option keys: {list(CAMPAIGN_DICT_KEYS)}"
        )

    # Determine the preset
    preset_key = option_spec.pop("preset", PRESET_NONE)
    if isinstance(preset_key, str):
        preset_key = _canonical_str_enum(preset_key)
    if not isinstance(preset_key, str) or preset_key not in PRESET_OPTIONS:
        raise OptionError(
            f"Invalid value for '{campaign_name}.preset': {preset_key}. Valid values are:\n"
            f"{list(PRESET_OPTIONS)}"
        )
    if preset_options and preset_key == PRESET_NONE:
        # Just a warning, to allow people to easily toggle the preset
        # without having to change their preset options
        logger.warning(
            f"Campaign '{campaign_name}' got preset-specific keys {list(preset_options)} "
            "when there is no preset. These options will have no effect."
        )

    # Resolve preset
    preset: 'CampaignPresetDict' = PRESET_OPTIONS[preset_key](preset_options | option_spec)

    # Preset global is resolved internally to avoid conflict with user global
    preset_global_spec: 'LayoutPresetDict' = cast('LayoutPresetDict', preset.pop("global", {}))
    preset_layout_specs = preset.pop("layouts", {})
    layout_names: list[str] = []
    for key in preset_layout_specs:
        preset_layout_specs[key] = copy.deepcopy(preset_global_spec) | preset_layout_specs[key]
        layout_names.append(key)
    for key in layout_specs:
        if key not in layout_names:
            layout_names.append(key)

    display_name = (
        ResolveOption(campaign_name, "display_name")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .replace_value("null", [])
        .listify()
        .require_list_of(str)
    )
    unique_name = (
        ResolveOption(campaign_name, "unique_name")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .require(bool)
    )
    entry_rule_specs = (
        ResolveOption(campaign_name, "entry_rules")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback([])
        .listify()
        .require_list_of(dict)
    )
    entry_rules: list['EntryRuleDict'] = []
    for index, entry_rule_spec in enumerate(entry_rule_specs):
        entry_rules.append(_resolve_entry_rule(f"{campaign_name}.entry_rules[{index}]", entry_rule_spec))
    unique_progression_track = (
        ResolveOption(campaign_name, "unique_progression_track")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .resolve_range()
        .require(int)
    )
    goal = (
        ResolveOption(campaign_name, "goal")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .require(bool)
    )
    min_difficulty = DIFFICULTY_OPTIONS[
        ResolveOption(campaign_name, "min_difficulty")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .map(_canonical_str_enum, type_filter=str)
        .require_string_enum(list(DIFFICULTY_OPTIONS))
    ]
    max_difficulty = DIFFICULTY_OPTIONS[
        ResolveOption(campaign_name, "max_difficulty")
        .fallback_from_dict(option_spec)
        .fallback_from_dict(preset)
        .fallback_from_dict(DEFAULT_CAMPAIGN_SETTINGS)
        .map(_canonical_str_enum, type_filter=str)
        .require_string_enum(list(DIFFICULTY_OPTIONS))
    ]
    missions = ""
    if preset_key != PRESET_NONE:
        missions = (
            ResolveOption(campaign_name, "missions")
            .fallback_from_dict(option_spec)
            .fallback("random")
            .require_string_enum(["random", "vanilla_shuffled", "vanilla"])
        )

    layouts = {
        layout_name: _resolve_layout_dict(
            f"{campaign_name}/{layout_name}",
            global_layout_spec | layout_specs.get(layout_name, {}),
            preset_layout_specs.get(layout_name, {}),
        )
        for layout_name in layout_names
    }
    result: 'CampaignDict' = {
        "display_name": display_name,
        "unique_name": unique_name,
        "unique_progression_track": unique_progression_track,
        "goal": goal,
        "entry_rules": entry_rules,
        "min_difficulty": min_difficulty,
        "max_difficulty": max_difficulty,
        "layouts": layouts,
        "single_layout_campaign": campaign_spec["single_layout_campaign"],
    }
    if missions:
        result["missions"] = missions
    return result


def _resolve_layout_dict(
    layout_name: str,
    layout_spec: dict[str, Any],
    preset_layout_spec: 'LayoutPresetDict',
) -> 'LayoutDict':
    extra_keys: list[str] = []
    allowed_keys = set(LAYOUT_DICT_KEYS)
    for conditional_keys in CONDITIONAL_LAYOUT_KEYS.values():
        allowed_keys.update(conditional_keys)
    for key in layout_spec:
        if key not in allowed_keys:
            extra_keys.append(key)
    if extra_keys:
        raise OptionError(
            f"Invalid keys specified for layout {layout_name}: {extra_keys}. "
            f"Allowed keys are {LAYOUT_DICT_KEYS}"
        )

    display_name = (
        ResolveOption(layout_name, "display_name")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .replace_value("null", [])
        .listify()
        .require_list_of(str)
    )
    unique_name = (
        ResolveOption(layout_name, "unique_name")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .require(bool)
    )
    layout_type = (
        ResolveOption(layout_name, "type")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .map(str.lower, type_filter=str)
        .require_string_enum(list(layout_types.LAYOUT_TYPE_NAME_TO_CLASS))
    )
    layout_exit = (
        ResolveOption(layout_name, "exit")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .require(bool)
    )
    goal = (
        ResolveOption(layout_name, "goal")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .require(bool)
    )
    entry_rule_specs = (
        ResolveOption(layout_name, "entry_rules")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback([])
        .listify()
        .require_list_of(dict)
    )
    entry_rules: list['EntryRuleDict'] = []
    for index, entry_rule_spec in enumerate(entry_rule_specs):
        entry_rules.append(_resolve_entry_rule(f"{layout_name}.entry_rules[{index}]", entry_rule_spec))
    unique_progression_track = (
        ResolveOption(layout_name, "unique_progression_track")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .require(int)
    )
    mission_pool_spec = (
        ResolveOption(layout_name, "mission_pool")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .require_list_of(str)
    )
    mission_pool = _resolve_mission_pool(f"{layout_name}.mission_pool", mission_pool_spec)
    min_difficulty = DIFFICULTY_OPTIONS[
        ResolveOption(layout_name, "min_difficulty")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .map(_canonical_str_enum, type_filter=str)
        .require_string_enum(list(DIFFICULTY_OPTIONS))
    ]
    max_difficulty = DIFFICULTY_OPTIONS[
        ResolveOption(layout_name, "max_difficulty")
        .fallback_from_dict(layout_spec)
        .fallback_from_dict(preset_layout_spec)
        .fallback_from_dict(DEFAULT_LAYOUT_SETTINGS)
        .map(_canonical_str_enum, type_filter=str)
        .require_string_enum(list(DIFFICULTY_OPTIONS))
    ]
    missions: list['MissionSlotDict'] = []

    for index, mission_spec in enumerate(preset_layout_spec.get("missions", [])):
        missions.append(_resolve_mission_spec(f"{layout_name}.preset_missions[{index}]", mission_spec))
    for index, mission_spec in enumerate(layout_spec.get("missions", [])):
        missions.append(_resolve_mission_spec(f"{layout_name}.missions[{index}]", mission_spec))

    result: 'LayoutDict' = {
        "display_name": display_name,
        "unique_name": unique_name,
        "type": layout_type,
        "size": 0,
        "exit": layout_exit,
        "goal": goal,
        "entry_rules": entry_rules,
        "unique_progression_track": unique_progression_track,
        "mission_pool": mission_pool,
        "min_difficulty": min_difficulty,
        "max_difficulty": max_difficulty,
        "missions": missions,
    }

    # Second check of keys now that we know the type
    # just print a warning on invalid keys to allow easy reconfiguration of type
    allowed_keys = set(LAYOUT_DICT_KEYS).union(CONDITIONAL_LAYOUT_KEYS.get(layout_type, ()))
    for key in layout_spec:
        if key not in allowed_keys:
            logger.warning(
                f"Layout '{layout_name}' has key '{key}' which is not recognized for type '{layout_type}'. "
                "Ignoring this key."
            )

    layout_keys_for_this_type = CONDITIONAL_LAYOUT_KEYS.get(layout_type, ())
    if "size" in layout_keys_for_this_type:
        size = (
            ResolveOption(layout_name, "size")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .assert_greater_than_equal_to(1)
            .require(int)
        )
        if size is not None:
            result["size"] = size
    if "width" in layout_keys_for_this_type:
        width = (
            ResolveOption(layout_name, "width")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .assert_greater_than_equal_to(1)
            .require_nullable(int)
        )
        if width is not None:
            result["width"] = width
    if "two_start_positions" in layout_keys_for_this_type:
        two_start_positions = (
            ResolveOption(layout_name, "two_start_positions")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .require_nullable(bool)
        )
        if two_start_positions is not None:
            result["two_start_positions"] = two_start_positions
    if "spacer" in layout_keys_for_this_type:
        spacer = (
            ResolveOption(layout_name, "spacer")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .assert_greater_than_equal_to(1)
            .require_nullable(int)
        )
        if spacer is not None:
            result["spacer"] = spacer
    if "canvas" in layout_keys_for_this_type:
        canvas = (
            ResolveOption(layout_name, "canvas")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .listify()
            .require_list_of(str)
        )
        result["canvas"] = canvas
        width = 0
        for line in canvas:
            if len(line) > width:
                width = len(line)
        result["width"] = width
        result["size"] = width * len(canvas)
    if "jump_distance_orthogonal" in layout_keys_for_this_type:
        jump_distance_orthogonal = (
            ResolveOption(layout_name, "jump_distance_orthogonal")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .assert_greater_than_equal_to(1)
            .require_nullable(int)
        )
        if jump_distance_orthogonal is not None:
            result["jump_distance_orthogonal"] = jump_distance_orthogonal
    if "jump_distance_diagonal" in layout_keys_for_this_type:
        jump_distance_diagonal = (
            ResolveOption(layout_name, "jump_distance_diagonal")
            .fallback_from_dict(layout_spec)
            .fallback_from_dict(preset_layout_spec)
            .assert_greater_than_equal_to(0)
            .require_nullable(int)
        )
        if jump_distance_diagonal is not None:
            result["jump_distance_diagonal"] = jump_distance_diagonal

    return result


def _resolve_entry_rule(option_name: str, option_value: dict) -> 'EntryRuleDict':
    amount: int | None = None

    VALID_KEYS = {"amount", "scope", "rules", "items"}
    invalid_keys = set(option_value) - VALID_KEYS
    if invalid_keys:
        raise OptionError(
            f"Invalid keys in '{option_name}': {sorted(invalid_keys)}. "
            f"Allowed keys: {sorted(VALID_KEYS)}"
        )

    VALID_COMBINATIONS = (
        {"amount", "rules"},
        {"amount", "scope"},
        {"rules"},
        {"scope"},
        {"items"},
    )
    if set(option_value) not in VALID_COMBINATIONS:
        raise OptionError(
            f"Invalid key combination in '{option_name}': {list(option_value)}. "
            f"Expected one of {[sorted(x) for x in VALID_COMBINATIONS]}"
        )

    if "amount" in option_value:
        parsed_amount = _resolve_potential_range(option_value["amount"], f"{option_name}.amount")
        if not isinstance(parsed_amount, int):
            raise OptionError(
                f"Invalid type for amount in {option_name}. "
                f"Expected an integer, got value of {type(parsed_amount).__name__} ('{parsed_amount}')."
            )
        amount = parsed_amount
    if "scope" in option_value:
        scope: list[str] = []
        # A scope may be a list or a single address
        if isinstance(option_value["scope"], list):
            subscopes = option_value["scope"]
        else:
            subscopes = [option_value["scope"]]
        for index, subscope in enumerate(subscopes):
            if isinstance(subscope, int):
                subscope = str(subscope)
            if not isinstance(subscope, str):
                raise OptionError(errormsg_invalid_type(f"{option_name}.scope[{index}]", subscope, str))
            scope.append(subscope)
        if not scope:
            raise OptionError(f"'{option_name}.scope' is empty, expected a mission slot or list of mission slots")
        if amount is None:
            amount = -1
        return {"scope": scope, "amount": amount}
    if "rules" in option_value:
        subrules = [
            _resolve_entry_rule(f"{option_name}.rules[{index}]", subrule_dict)
            for index, subrule_dict in enumerate(option_value["rules"])
        ]
        # Make sure sub-rule rules have a specified amount
        if amount is None:
            amount = -1
        return {"rules": subrules, "amount": amount}

    assert "items" in option_value
    option_items = option_value["items"]
    if not isinstance(option_items, dict):
        raise OptionError(errormsg_invalid_type(f"{option_name}.items", option_items, dict))
    items_result: dict[str, int] = {}
    for item_name, item_amount in option_items.items():
        item_name = str(item_name)
        item_amount = _resolve_potential_range(item_amount, f"{option_name}.items[{item_name}]")
        if not isinstance(item_amount, int):
            raise OptionError(errormsg_invalid_type(f"{option_name}.items[{item_name}]", item_amount, int))
        items_result[item_name] = item_amount
    items_result = _resolve_item_names(items_result)

    # Check for invalid item names, resolve item amounts based on item quantities
    invalid_items: list[str] = []
    for item in items_result:
        if item not in item_table:
            if item.casefold() == GENERIC_KEY_NAME or item.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME):
                items_result[item] = max(0, items_result[item])
                continue
            invalid_items.append(item)
            continue
        amount = max(-1, items_result[item])
        quantity = item_table[item].quantity
        if amount == -1:
            final_amount = quantity
        elif quantity == 0:
            final_amount = amount
        else:
            final_amount = amount
        items_result[item] = final_amount
    if invalid_items:
        raise OptionError(f"Item rule '{option_name}.items' contains invalid item names: {invalid_items}")
    return {"items": items_result}


def _resolve_potential_range(option_value: Any | str, option_name: str) -> Any | int:
    # An option value may be a range
    if isinstance(option_value, str) and option_value.startswith("random-range-"):
        resolved = _custom_range(option_value, option_name)
        return resolved
    else:
        # As this is a catch-all function,
        # assume non-range option values are handled elsewhere
        # or intended to fall through
        return option_value


def _resolve_mission_pool(option_name: str, option_value: list[str]) -> set[int]:
    result: set[int] = set()
    for index, line in enumerate(option_value):
        if line.startswith("~"):
            if len(result) == 0:
                raise OptionError(f"'{option_name}[{index}]': line '{line}' tried to remove missions from an empty pool.")
            term = line[1:].strip()
            missions = _get_target_missions(f"{option_name}[{index}]", term)
            result.difference_update(missions)
        elif line.startswith("^"):
            if len(result) == 0:
                raise OptionError(f"'{option_name}[{index}]': line '{line}' tried to remove missions from an empty pool.")
            term = line[1:].strip()
            missions = _get_target_missions(f"{option_name}[{index}]", term)
            result.intersection_update(missions)
        else:
            if line.startswith("+"):
                term = line[1:].strip()
            else:
                term = line.strip()
            missions = _get_target_missions(f"{option_name}[{index}]", term)
            result.update(missions)
    if len(result) == 0:
        raise OptionError(f"'{option_name}': Mission pool evaluated to zero missions: {option_value}")
    return result


def _get_target_missions(option_name: str, term: str) -> set[int]:
    if term in lookup_name_to_mission:
        return {lookup_name_to_mission[term].id}
    else:
        groups = [mission_groups[group] for group in mission_groups if group.casefold() == term.casefold()]
        if len(groups) > 0:
            return {lookup_name_to_mission[mission].id for mission in groups[0]}
        else:
            raise OptionError(f"'{option_name}': line '{term}' did not resolve to any specific mission or mission group.")


def _resolve_mission_spec(option_name: str, option_value: Any) -> 'MissionSlotDict':
    if not isinstance(option_value, dict):
        raise OptionError(errormsg_invalid_type(option_name, option_value, dict))
    extra_keys: list[str] = []
    for key in option_value:
        if key not in MISSION_SLOT_KEYS:
            extra_keys.append(key)
    if extra_keys:
        raise OptionError(
            f"Invalid keys specified for mission {option_name}: {extra_keys}. "
            f"Allowed keys are {MISSION_SLOT_KEYS}"
        )

    mission_index = (
        ResolveOption(option_name, "index")
        .fallback_from_dict(option_value)
        .resolve_range()
        .listify()
        .flatten_list()
        .map(lambda li: [str(x) for x in li], type_filter=list)
        .require_list_of((str, int))
    )
    entrance = (
        ResolveOption(option_name, "entrance")
        .fallback_from_dict(option_value)
        .require_nullable(bool)
    )
    mission_exit = (
        ResolveOption(option_name, "exit")
        .fallback_from_dict(option_value)
        .require_nullable(bool)
    )
    goal = (
        ResolveOption(option_name, "goal")
        .fallback_from_dict(option_value)
        .require_nullable(bool)
    )
    empty = (
        ResolveOption(option_name, "empty")
        .fallback_from_dict(option_value)
        .require_nullable(bool)
    )
    next_missions = (
        ResolveOption(option_name, "next")
        .fallback_from_dict(option_value)
        .listify()
        .flatten_list()
        .require_nullable_list_of((str, int))
    )
    entry_rule_specs = (
        ResolveOption(option_name, "entry_rules")
        .fallback_from_dict(option_value)
        .listify()
        .require_nullable_list_of(dict)
    )
    if entry_rule_specs is not None:
        entry_rules: list['EntryRuleDict'] = []
        for index, entry_rule_spec in enumerate(entry_rule_specs):
            entry_rules.append(_resolve_entry_rule(f"{option_name}.entry_rules[{index}]", entry_rule_spec))
    mission_pool_spec = (
        ResolveOption(option_name, "mission_pool")
        .fallback_from_dict(option_value)
        .listify()
        .require_nullable_list_of(str)
    )
    if mission_pool_spec is not None:
        mission_pool = _resolve_mission_pool(f"{option_name}.mission_pool", mission_pool_spec)
    difficulty_spec = (
        ResolveOption(option_name, "difficulty")
        .fallback_from_dict(option_value)
        .map(_canonical_str_enum, type_filter=str)
    )
    if difficulty_spec.value is not None:
        difficulty = DIFFICULTY_OPTIONS[difficulty_spec.require_string_enum(list(DIFFICULTY_OPTIONS))]
    victory_cache = (
        ResolveOption(option_name, "victory_cache")
        .fallback_from_dict(option_value)
        .assert_less_than_equal_to(locations.NUM_VICTORY_CACHE_LOCATIONS)
        .require_nullable(int)
    )
    heroes_spec = (
        ResolveOption(option_name, "heroes")
        .fallback_from_dict(option_value)
        .listify()
    )
    if heroes_spec.value is not None:
        heroes = heroes_spec.require_list_of(str)
        heroes = [hero.capitalize() for hero in heroes]
        invalid_heroes: list[str] = []
        for hero in heroes:
            if hero not in (HeroOptions.ALL_HERO_OPTIONS):
                invalid_heroes.append(hero)
        if invalid_heroes:
            raise OptionError(
                f"{option_name}.heroes: Invalid hero values specified: {invalid_heroes}. "
                f"Valid heroes are {HeroOptions.ALL_HERO_OPTIONS}"
            )

    result: 'MissionSlotDict' = {"index": mission_index}
    if entrance is not None:
        result["entrance"] = entrance
    if mission_exit is not None:
        result["exit"] = mission_exit
    if goal is not None:
        result["goal"] = goal
    if empty is not None:
        result["empty"] = empty
    if next_missions is not None:
        result["next"] = cast(list[int | str], next_missions)
    if entry_rule_specs is not None:
        result["entry_rules"] = entry_rules
    if mission_pool_spec is not None:
        result["mission_pool"] = mission_pool
    if difficulty_spec.value is not None:
        result["difficulty"] = difficulty
    if victory_cache is not None:
        result["victory_cache"] = victory_cache
    if heroes_spec.value is not None:
        result["heroes"] = heroes
    return result


def _resolve_heroes(option_value: str | list[str]) -> list[str]:
    if isinstance(option_value, str):
        heroes = [option_value]
    else:
        heroes = option_value

    resolved: list[str] = []
    for hero in heroes:
        formatted_hero = str(hero).casefold()
        if formatted_hero not in HERO_OPTION_VALUES:
            raise ValueError(
                f"Hero entry \"{hero}\" did not resolve to a known hero. "
                f"Allowed values are: {list(HERO_OPTION_VALUES.values())}"
            )
        resolved_hero = HERO_OPTION_VALUES[formatted_hero]
        if resolved_hero not in resolved:
            resolved.append(resolved_hero)
    return resolved


# Class-agnostic version of AP Options.Range.custom_range
def _custom_range(text: str, option_name: str) -> int:
    textsplit = text.split("-")
    try:
        random_range = [int(textsplit[-2]), int(textsplit[-1])]
    except ValueError:
        raise OptionError(f"Invalid random range {text} for option {option_name}")
    random_range.sort()
    if text.startswith("random-range-low"):
        return _triangular(random_range[0], random_range[1], random_range[0])
    elif text.startswith("random-range-middle"):
        return _triangular(random_range[0], random_range[1])
    elif text.startswith("random-range-high"):
        return _triangular(random_range[0], random_range[1], random_range[1])
    else:
        return random.randint(random_range[0], random_range[1])


def _triangular(lower: int, end: int, tri: int | None = None) -> int:
    return int(round(random.triangular(lower, end, tri), 0))


# Version of options.Sc2ItemDict.verify without World
def _resolve_item_names(value: dict[str, int]) -> dict[str, int]:
    new_value: dict[str, int] = {}
    case_insensitive_group_mapping: dict[str, Iterable[str]] = {
        group_name.casefold(): group_value for group_name, group_value in item_groups.item_name_groups.items()
    }
    case_insensitive_group_mapping.update({item.casefold(): {item} for item in item_table})
    for group_name in value:
        item_names = case_insensitive_group_mapping.get(group_name.casefold(), (group_name,))
        for item_name in item_names:
            new_value[item_name] = new_value.get(item_name, 0) + value[group_name]
    return new_value


def _canonical_str_enum(raw_option: str) -> str:
    return raw_option.lower().replace("_", " ")
