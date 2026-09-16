from enum import IntFlag


class HeroOptions:
    KERRIGAN = "Kerrigan"
    NOVA = "Nova"
    ARTANIS = "Artanis"

    ALL_HERO_OPTIONS = (
        KERRIGAN,
        NOVA,
        ARTANIS,
    )


class HeroFlag(IntFlag):
    """Hero presence bitflag. Must match the SC2Data implementation."""
    NONE = 0
    KERRIGAN = 1
    NOVA = 2
    ARTANIS = 4


class StabilityOptions:
    STARTER_LOCATIONS = "Starter locations"
    ITEM_RE_INCLUSION = "Item re-inclusions"

    ALL_KEYS = (
        STARTER_LOCATIONS,
        ITEM_RE_INCLUSION,
    )
