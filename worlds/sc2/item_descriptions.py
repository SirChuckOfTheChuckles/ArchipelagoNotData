"""
Contains descriptions for Starcraft 2 items.
"""
import inspect

from . import item_names

WEAPON_ARMOR_UPGRADE_NOTE = inspect.cleandoc("""
    Must be researched during the mission if the mission type isn't set to auto-unlock generic upgrades.
""")
GENERIC_UPGRADE_TEMPLATE = "Increases {} of {} {}.\n" + WEAPON_ARMOR_UPGRADE_NOTE
TERRAN = "Terran"
ZERG = "Zerg"
PROTOSS = "Protoss"

LASER_TARGETING_SYSTEMS_DESCRIPTION = "Increases vision by 2 and weapon range by 1."
STIMPACK_SMALL_COST = 10
STIMPACK_SMALL_HEAL = 30
STIMPACK_LARGE_COST = 20
STIMPACK_LARGE_HEAL = 60
STIMPACK_TEMPLATE = inspect.cleandoc("""
    Level 1: Stimpack: Increases unit movement and attack speed for 15 seconds. Injures the unit for {} life.
    Level 2: Super Stimpack: Instead of injuring the unit, heals the unit for {} life instead.
""")
STIMPACK_SMALL_DESCRIPTION = STIMPACK_TEMPLATE.format(STIMPACK_SMALL_COST, STIMPACK_SMALL_HEAL)
STIMPACK_LARGE_DESCRIPTION = STIMPACK_TEMPLATE.format(STIMPACK_LARGE_COST, STIMPACK_LARGE_HEAL)
SMART_SERVOS_DESCRIPTION = "Increases transformation speed between modes."
INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE = "{} can be trained from a {} without an attached Tech Lab."
CLOAK_DESCRIPTION_TEMPLATE = "Allows {} to use the Cloak ability."

DISPLAY_NAME_BROOD_LORD = "Brood Lord"
DISPLAY_NAME_CLOAKED_ASSASSIN = "Dark Templar, Avenger, and Blood Hunter"

resource_efficiency_cost_reduction = {
    item_names.REAPER:        (0, 50, 0),
    item_names.MEDIC:         (25, 25, 1),
    item_names.FIREBAT:       (50, 0, 1),
    item_names.GOLIATH:       (50, 0, 1),
    item_names.SIEGE_TANK:    (0, 25, 1),
    item_names.DIAMONDBACK:   (0, 50, 1),
    item_names.PREDATOR:      (0, 75, 1),
    item_names.WARHOUND:      (75, 0, 0),
    item_names.HERC:          (25, 25, 1),
    item_names.WRAITH:        (0, 50, 0),
    item_names.GHOST:         (125, 75, 1),
    item_names.SPECTRE:       (125, 75, 1),
    item_names.RAVEN:         (0, 50, 0),
    item_names.CYCLONE:       (25, 50, 1),
    item_names.WIDOW_MINE:    (0, 25, 1),
    item_names.LIBERATOR:     (0, 25, 0),
    item_names.VALKYRIE:      (100, 25, 1),
    item_names.DEVASTATOR_TURRET: (50, 0, 0),
    item_names.MISSILE_TURRET: (25, 0, 0),
    item_names.SCOURGE:       (0, 50, 0),
    item_names.HYDRALISK:     (25, 25, 1),
    item_names.SWARM_HOST:    (100, 25, 0),
    item_names.ULTRALISK:     (100, 0, 2),
    item_names.ABERRATION:    (50, 25, 0),
    item_names.CORRUPTOR:     (50, 25, 0),
    DISPLAY_NAME_BROOD_LORD:  (0, 75, 0),
    item_names.SWARM_QUEEN:   (0, 50, 0),
    item_names.ARBITER:       (50, 0, 0),
    item_names.REAVER:        (100, 100, 2),
    DISPLAY_NAME_CLOAKED_ASSASSIN: (0, 50, 0),
    item_names.SCOUT:         (125, 25, 1),
    item_names.DESTROYER:     (50, 25, 1),

    # War Council
    item_names.CENTURION:     (0, 50, 0),
    item_names.SENTINEL:      (60, 0, 1),
    item_names.INSTIGATOR:    (40, 15, 0),
}


def _get_resource_efficiency_desc(item_name: str) -> str:
    cost = resource_efficiency_cost_reduction[item_name]
    parts = [f"{cost[0]} minerals"] if cost[0] else []
    parts += [f"{cost[1]} gas"] if cost[1] else []
    parts += [f"{cost[2]} supply"] if cost[2] else []
    assert parts, f"{item_name} doesn't reduce cost by anything"
    if len(parts) == 1:
        amount = parts[0]
    elif len(parts) == 2:
        amount = " and ".join(parts)
    else:
        amount = ", ".join(parts[:-1]) + ", and " + parts[-1]
    return (f"Reduces {item_name} cost by {amount}.")


def _get_start_and_max_energy_desc(unit_name_plural: str, starting_amount_increase: int = 150, maximum_amount_increase: int = 50) -> str:
    return f"{unit_name_plural} gain +{starting_amount_increase} starting energy and +{maximum_amount_increase} maximum energy."


def _ability_desc(unit_name_plural: str, ability_name: str, ability_description: str = '') -> str:
    if ability_description:
        suffix = f", \nwhich {ability_description}"
    else:
        suffix = ""
    return f"{unit_name_plural} gain the {ability_name} ability{suffix}."


item_descriptions = {
    item_names.MARINE: "General-purpose infantry.",
    item_names.MEDIC: "Support trooper. Heals nearby biological units.",
    item_names.FIREBAT: "Specialized anti-infantry attacker.",
    item_names.MARAUDER: "Heavy assault infantry.",
    item_names.REAPER: "Raider. Capable of jumping up and down cliffs. Throws explosive mines.",
    item_names.HELLION: "Fast scout. Has a flame attack that damages all enemy units in its line of fire.",
    item_names.VULTURE: "Fast skirmish unit. Can use the Spider Mine ability.",
    item_names.GOLIATH: "Heavy-fire support unit.",
    item_names.DIAMONDBACK: "Fast, high-damage hovertank. Rail Gun can fire while the Diamondback is moving.",
    item_names.SIEGE_TANK: "Heavy tank. Long-range artillery in Siege Mode.",
    item_names.MEDIVAC: "Air transport. Heals nearby biological units.",
    item_names.WRAITH: "Highly mobile flying unit. Excellent at surgical strikes.",
    item_names.VIKING: inspect.cleandoc("""
        Durable support flyer. Loaded with strong anti-capital air missiles. 
        Can switch into Assault Mode to attack ground units.
    """),
    item_names.BANSHEE: "Tactical-strike aircraft.",
    item_names.BATTLECRUISER: "Powerful warship.",
    item_names.GHOST: inspect.cleandoc("""
        Infiltration unit. Can use Snipe and Cloak abilities. Can also call down Tactical Nukes.
    """),
    item_names.SPECTRE: inspect.cleandoc("""
        Infiltration unit. Can use Ultrasonic Pulse, Psionic Lash, and Cloak. 
        Can also call down Tactical Nukes.
    """),
    item_names.THOR: "Heavy assault mech.",
    item_names.LIBERATOR: inspect.cleandoc("""
        Artillery fighter. Loaded with missiles that deal area damage to enemy air targets. 
        Can switch into Defender Mode to provide siege support.
    """),
    item_names.VALKYRIE: inspect.cleandoc("""
        Advanced anti-aircraft fighter. 
        Able to use cluster missiles that deal area damage to air targets.
    """),
    item_names.WIDOW_MINE: inspect.cleandoc("""
        Robotic mine. Launches missiles at nearby enemy units while burrowed. 
        Attacks deal splash damage in a small area around the target. 
        Widow Mine is revealed when Sentinel Missile is on cooldown.
    """),
    item_names.CYCLONE: inspect.cleandoc("""
        Mobile assault vehicle. Can use Lock On to quickly fire while moving.
    """),
    item_names.HERC: inspect.cleandoc("""
        Front-line infantry. Can use Grapple.
    """),
    item_names.WARHOUND: inspect.cleandoc("""
        Anti-vehicle mech. Haywire missiles do bonus damage to mechanical units.
    """),
    item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "infantry"),
    item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "infantry"),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "vehicles"),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "vehicles"),
    item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "starships"),
    item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "starships"),
    item_names.PROGRESSIVE_TERRAN_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "units"),
    item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "units"),
    item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "infantry"),
    item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "vehicles"),
    item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "starships"),
    item_names.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "units"),
    item_names.BUNKER_PROJECTILE_ACCELERATOR: "Increases range of all units in the Bunker by 1.",
    item_names.BUNKER_NEOSTEEL_BUNKER: "Increases the number of Bunker slots by 2.",
    item_names.MISSILE_TURRET_TITANIUM_HOUSING: "Increases Missile Turret life by 75.",
    item_names.MISSILE_TURRET_HELLSTORM_BATTERIES: "The Missile Turret unleashes an additional flurry of missiles with each attack.",
    item_names.SCV_ADVANCED_CONSTRUCTION: "Multiple SCVs can construct a structure, reducing its construction time.",
    item_names.SCV_DUAL_FUSION_WELDERS: "SCVs repair twice as fast.",
    item_names.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM: inspect.cleandoc("""
        Level 1: While on low health, Terran structures are repaired to half health instead of burning down.
        Level 2: Terran structures are repaired to full health instead of half health.
    """),
    item_names.PROGRESSIVE_ORBITAL_COMMAND: inspect.cleandoc("""
        Deprecated. Replaced by Scanner Sweep, MULE, and Orbital Module (Planetary Fortress)
        Level 1: Allows Command Centers to use Scanner Sweep and Calldown: MULE abilities.
        Level 2: Orbital Command abilities work even in Planetary Fortress mode.
    """),
    item_names.MARINE_PROGRESSIVE_STIMPACK: STIMPACK_SMALL_DESCRIPTION,
    item_names.MARINE_COMBAT_SHIELD: "Increases Marine life by 10.",
    item_names.MEDIC_ADVANCED_MEDIC_FACILITIES: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Medics", "Barracks"),
    item_names.MEDIC_STABILIZER_MEDPACKS: "Increases Medic heal speed. Reduces the amount of energy required for each heal.",
    item_names.FIREBAT_INCINERATOR_GAUNTLETS: "Increases Firebat's damage radius by 40%.",
    item_names.FIREBAT_JUGGERNAUT_PLATING: "Increases Firebat's armor by 2.",
    item_names.MARAUDER_CONCUSSIVE_SHELLS: "Marauder attack temporarily slows all units in target area.",
    item_names.MARAUDER_KINETIC_FOAM: "Increases Marauder life by 25.",
    item_names.REAPER_U238_ROUNDS: inspect.cleandoc("""
        Increases Reaper pistol attack range by 1.
        Reaper pistols do additional 3 damage to Light Armor.
    """),
    item_names.REAPER_G4_CLUSTERBOMB: "Timed explosive that does heavy area damage.",
    item_names.CYCLONE_MAG_FIELD_ACCELERATORS: "Increases Cyclone Lock-On damage.",
    item_names.CYCLONE_MAG_FIELD_LAUNCHERS: "Increases Cyclone attack range by 2.",
    item_names.MARINE_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.MARINE_MAGRAIL_MUNITIONS: "Deals 20 damage to target unit. Autocast on attack with a cooldown.",
    item_names.MARINE_OPTIMIZED_LOGISTICS: "Increases Marine training speed.",
    item_names.MEDIC_RESTORATION: _ability_desc("Medics", "Restoration", "removes negative status effects from a target allied unit"),
    item_names.MEDIC_OPTICAL_FLARE: _ability_desc("Medics", "Optical Flare", "reduces vision range of target enemy unit. Disables detection"),
    item_names.MEDIC_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.MEDIC),
    item_names.FIREBAT_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    item_names.FIREBAT_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.FIREBAT),
    item_names.MARAUDER_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    item_names.MARAUDER_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.MARAUDER_MAGRAIL_MUNITIONS: "Deals 20 damage to target unit. Autocast on attack with a cooldown.",
    item_names.MARAUDER_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Marauders", "Barracks"),
    item_names.SCV_HOSTILE_ENVIRONMENT_ADAPTATION: "Increases SCV life by 15 and attack speed slightly.",
    item_names.MEDIC_ADAPTIVE_MEDPACKS: "Allows Medics to heal mechanical and air units.",
    item_names.MEDIC_NANO_PROJECTOR: "Increases Medic heal range by 2.",
    item_names.FIREBAT_INFERNAL_PRE_IGNITER: "Firebats do an additional 4 damage to Light Armor.",
    item_names.FIREBAT_KINETIC_FOAM: "Increases Firebat life by 100.",
    item_names.FIREBAT_NANO_PROJECTORS: "Increases Firebat attack range by 2.",
    item_names.MARAUDER_JUGGERNAUT_PLATING: "Increases Marauder's armor by 2.",
    item_names.REAPER_JET_PACK_OVERDRIVE: inspect.cleandoc("""
        Allows the Reaper to fly for 10 seconds.
        While flying, the Reaper can attack air units.
    """),
    item_names.HELLION_INFERNAL_PLATING: "Increases Hellion and Hellbat armor by 2.",
    item_names.VULTURE_AUTO_REPAIR: "Vultures regenerate life.",
    item_names.GOLIATH_SHAPED_HULL: "Increases Goliath life by 25.",
    item_names.GOLIATH_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.GOLIATH),
    item_names.GOLIATH_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Goliaths", "Factory"),
    item_names.SIEGE_TANK_SHAPED_HULL: "Increases Siege Tank life by 25.",
    item_names.SIEGE_TANK_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SIEGE_TANK),
    item_names.PREDATOR_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Predators"),
    item_names.PREDATOR_CHARGE: "Allows Predators to intercept enemy ground units.",
    item_names.MEDIVAC_SCATTER_VEIL: "Medivacs get 100 shields.",
    item_names.REAPER_PROGRESSIVE_STIMPACK: STIMPACK_SMALL_DESCRIPTION,
    item_names.REAPER_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.REAPER_ADVANCED_CLOAKING_FIELD: "Reapers are permanently cloaked.",
    item_names.REAPER_SPIDER_MINES: "Allows Reapers to lay Spider Mines. 3 charges per Reaper.",
    item_names.REAPER_COMBAT_DRUGS: "Reapers regenerate life while out of combat.",
    item_names.HELLION_HELLBAT_ASPECT: "Allows Hellions to transform into Hellbats.",
    item_names.HELLION_SMART_SERVOS: "Transforms faster between modes. Hellions can attack while moving.",
    item_names.HELLION_OPTIMIZED_LOGISTICS: "Increases Hellion training speed.",
    item_names.HELLION_JUMP_JETS: inspect.cleandoc("""
        Increases movement speed in Hellion mode.
        In Hellbat mode, launches the Hellbat toward enemy ground units and briefly stuns them.
    """),
    item_names.HELLION_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    item_names.VULTURE_ION_THRUSTERS: "Increases Vulture movement speed.",
    item_names.VULTURE_AUTO_LAUNCHERS: "Allows Vultures to attack while moving.",
    item_names.SPIDER_MINE_HIGH_EXPLOSIVE_MUNITION: "Increases Spider mine damage.",
    item_names.GOLIATH_JUMP_JETS: "Allows Goliaths to jump up and down cliffs.",
    item_names.GOLIATH_OPTIMIZED_LOGISTICS: "Increases Goliath training speed.",
    item_names.DIAMONDBACK_HYPERFLUXOR: "Increases Diamondback attack speed.",
    item_names.DIAMONDBACK_BURST_CAPACITORS: inspect.cleandoc("""
        While not attacking, the Diamondback charges its weapon. 
        The next attack does 10 additional damage.
    """),
    item_names.DIAMONDBACK_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.DIAMONDBACK),
    item_names.SIEGE_TANK_JUMP_JETS: inspect.cleandoc("""
        Repositions Siege Tank to a target location. 
        Can be used in either mode and to jump up and down cliffs. 
    """),
    item_names.SIEGE_TANK_SPIDER_MINES: inspect.cleandoc("""
        Allows Siege Tanks to lay Spider Mines. 
        Lays 3 Spider Mines at once. 3 charges.
    """),
    item_names.SIEGE_TANK_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    item_names.SIEGE_TANK_GRADUATING_RANGE: inspect.cleandoc("""
        Increases the Siege Tank's attack range by 1 every 3 seconds while in Siege Mode, 
        up to a maximum of 5 additional range.
    """),
    item_names.SIEGE_TANK_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.SIEGE_TANK_ADVANCED_SIEGE_TECH: "Siege Tanks gain +3 armor in Siege Mode.",
    item_names.SIEGE_TANK_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Siege Tanks", "Factory"),
    item_names.PREDATOR_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.PREDATOR),
    item_names.MEDIVAC_EXPANDED_HULL: "Increases Medivac cargo space by 4.",
    item_names.MEDIVAC_AFTERBURNERS: "Ability. Temporarily increases the Medivac's movement speed by 70%.",
    item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY: inspect.cleandoc("""
        Burst Lasers do more damage and can hit both ground and air targets.
        Replaces Gemini Missiles weapon.
    """),
    item_names.VIKING_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    item_names.VIKING_ANTI_MECHANICAL_MUNITION: "Increases Viking damage to mechanical units while in Assault Mode.",
    item_names.DIAMONDBACK_ION_THRUSTERS: "Increases Diamondback movement speed.",
    item_names.WARHOUND_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.WARHOUND),
    item_names.WARHOUND_REINFORCED_PLATING: "Increases Warhound armor by 2.",
    item_names.HERC_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.HERC),
    item_names.HERC_JUGGERNAUT_PLATING: "Increases HERC armor by 2.",
    item_names.HERC_KINETIC_FOAM: "Increases HERC life by 50.",
    item_names.REAPER_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.REAPER),
    item_names.REAPER_KINETIC_FOAM: "Increases Reaper life by 10.",
    item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK: inspect.cleandoc("""
        Level 1: Allows Siege Tanks to be transported in Siege Mode.
        Level 2: Siege Tanks in Siege Mode can attack air units while transported by a Medivac.
    """),
    item_names.SIEGE_TANK_ENHANCED_COMBUSTION_ENGINES: "Increases movement speed of Siege Tanks in Tank Mode.",
    item_names.MEDIVAC_RAPID_REIGNITION_SYSTEMS: inspect.cleandoc("""
        Increases slightly Medivac movement speed.
        Reduces Medivac's Afterburners ability cooldown.
    """),
    item_names.BATTLECRUISER_BEHEMOTH_REACTOR: "All Battlecruiser spells require 25 less energy to cast.",
    item_names.THOR_RAPID_RELOAD: "Increases Thor's ground attack speed.",
    item_names.LIBERATOR_GUERILLA_MISSILES: "Liberators in Fighter Mode apply an attack and movement debuff to enemies they attack.",
    item_names.WIDOW_MINE_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.WIDOW_MINE),
    item_names.HERC_GRAPPLE_PULL: "Allows HERCs to use their grappling gun to pull a ground unit towards the HERC.",
    item_names.COMMAND_CENTER_SCANNER_SWEEP: "Temporarily reveals an area of the map, detecting cloaked and burrowed units.",
    item_names.COMMAND_CENTER_MULE: "Summons a unit that gathers minerals more quickly than regular SCVs. Has timed life.",
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES: "Drops additional supplies, permanently increasing the supply output of the target Supply Depot by 8.",
    item_names.HELLION_TWIN_LINKED_FLAMETHROWER: "Doubles the width of the Hellion's flame attack.",
    item_names.HELLION_THERMITE_FILAMENTS: "Hellions do an additional 10 damage to Light Armor.",
    item_names.SPIDER_MINE_CERBERUS_MINE: "Increases trigger and blast radius of Spider Mines.",
    item_names.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE: inspect.cleandoc("""
        Level 1: Allows Vultures to replace used Spider Mines. Costs 15 minerals.
        Level 2: Replacing used Spider Mines no longer costs minerals.
    """),
    item_names.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM: "Goliaths can attack both ground and air targets simultaneously.",
    item_names.GOLIATH_ARES_CLASS_TARGETING_SYSTEM: "Increases Goliath ground attack range by 1 and air by 3.",
    item_names.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL: inspect.cleandoc("""
        Level 1: Tri-Lithium Power Cell: Increases Diamondback attack range by 1.
        Level 2: Tungsten Spikes: Increases Diamondback attack range by 3.
    """),
    item_names.DIAMONDBACK_SHAPED_HULL: "Increases Diamondback life by 50.",
    item_names.SIEGE_TANK_MAELSTROM_ROUNDS: "Siege Tanks do an additional 40 damage to the primary target in Siege Mode.",
    item_names.SIEGE_TANK_SHAPED_BLAST: "Reduces splash damage to friendly targets while in Siege Mode by 75%.",
    item_names.MEDIVAC_RAPID_DEPLOYMENT_TUBE: "Medivacs deploy loaded troops almost instantly.",
    item_names.MEDIVAC_ADVANCED_HEALING_AI: "Medivacs can heal two targets at once.",
    item_names.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS: inspect.cleandoc("""
        Level 1: Tomahawk Power Cells: Increases Wraith starting energy by 100.
        Level 2: Unregistered Cloaking Module: Wraiths do not require energy to cloak and remain cloaked.
    """),
    item_names.WRAITH_DISPLACEMENT_FIELD: "Wraiths evade 20% of incoming attacks while cloaked.",
    item_names.VIKING_RIPWAVE_MISSILES: "Vikings do area damage while in Fighter Mode.",
    item_names.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM: "Increases Viking attack range by 1 in Assault mode and 2 in Fighter mode.",
    item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS: inspect.cleandoc("""
        Level 1: Banshees can remain cloaked twice as long.
        Level 2: Banshees do not require energy to cloak and remain cloaked.
    """),
    item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY: "Banshees do area damage in a straight line.",
    item_names.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS: inspect.cleandoc(f"""
        {_ability_desc('Battlecruisers', 'Missile Pods', 'deals damage to air units in a target area')}
        Level 1: Deals 40 damage (+50 vs light).
        Level 2: Deals 110 damage and costs -50 less energy.
    """),
    item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX: inspect.cleandoc("""
        Level 1: Spell. For 20 seconds the Battlecruiser gains a shield that can absorb up to 200 damage.
        Level 2: Passive. Battlecruiser gets 200 shields.
    """),
    item_names.GHOST_OCULAR_IMPLANTS: "Increases Ghost sight range by 3 and attack range by 2.",
    item_names.GHOST_CRIUS_SUIT: "Cloak no longer requires energy to activate or maintain.",
    item_names.SPECTRE_PSIONIC_LASH: "Spell. Deals 200 damage to a single target.",
    item_names.SPECTRE_NYX_CLASS_CLOAKING_MODULE: "Cloak no longer requires energy to activate or maintain.",
    item_names.THOR_330MM_BARRAGE_CANNON: inspect.cleandoc("""
        Improves 250mm Strike Cannons ability to deal area damage and stun units in a small area.
        Can be also freely aimed on ground.
    """),
    item_names.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL: inspect.cleandoc("""
        Level 1: Allows destroyed Thors to be reconstructed on the field. Costs Vespene Gas.
        Level 2: Thors are automatically reconstructed after falling for free.
    """),
    item_names.LIBERATOR_ADVANCED_BALLISTICS: "Increases Liberator range by 3 in Defender Mode.",
    item_names.LIBERATOR_RAID_ARTILLERY: "Allows Liberators to attack structures while in Defender Mode.",
    item_names.WIDOW_MINE_DRILLING_CLAWS: "Allows Widow Mines to burrow and unburrow faster.",
    item_names.WIDOW_MINE_CONCEALMENT: "Burrowed Widow Mines are no longer revealed when the Sentinel Missile is on cooldown.",
    item_names.MEDIVAC_ADVANCED_CLOAKING_FIELD: "Medivacs are permanently cloaked.",
    item_names.WRAITH_TRIGGER_OVERRIDE: "Wraith attack speed increases by 10% with each attack, up to a maximum of 100%.",
    item_names.WRAITH_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Wraiths", "Starport"),
    item_names.WRAITH_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.WRAITH),
    item_names.VIKING_SHREDDER_ROUNDS: "Attacks in Assault mode do line splash damage.",
    item_names.VIKING_WILD_MISSILES: "Launches 5 rockets at the target unit. Each rocket does 25 (40 vs armored) damage.",
    item_names.BANSHEE_SHAPED_HULL: "Increases Banshee life by 100.",
    item_names.BANSHEE_ADVANCED_TARGETING_OPTICS: "Increases Banshee attack range by 2 while cloaked.",
    item_names.BANSHEE_DISTORTION_BLASTERS: "Increases Banshee attack damage by 25% while cloaked.",
    item_names.BANSHEE_ROCKET_BARRAGE: _ability_desc("Banshees", "Rocket Barrage", "deals 75 damage to enemy ground units in the target area"),
    item_names.GHOST_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.GHOST),
    item_names.SPECTRE_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SPECTRE),
    item_names.THOR_BUTTON_WITH_A_SKULL_ON_IT: "Allows Thors to launch nukes.",
    item_names.THOR_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.THOR_LARGE_SCALE_FIELD_CONSTRUCTION: "Allows Thors to be built by SCVs like a structure.",
    item_names.RAVEN_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.RAVEN),
    item_names.RAVEN_DURABLE_MATERIALS: "Extends timed life duration of Raven's summoned objects.",
    item_names.SCIENCE_VESSEL_IMPROVED_NANO_REPAIR: "Nano-Repair no longer requires energy to use.",
    item_names.SCIENCE_VESSEL_ADVANCED_AI_SYSTEMS: "Science Vessel can use Nano-Repair at two targets at once.",
    item_names.CYCLONE_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.CYCLONE),
    item_names.BANSHEE_HYPERFLIGHT_ROTORS: "Increases Banshee movement speed.",
    item_names.BANSHEE_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.BANSHEE_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Banshees", "Starport"),
    item_names.BATTLECRUISER_TACTICAL_JUMP: inspect.cleandoc("""
        Allows Battlecruisers to warp to a target location anywhere on the map.
    """),
    item_names.BATTLECRUISER_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Battlecruisers"),
    item_names.BATTLECRUISER_ATX_LASER_BATTERY: inspect.cleandoc("""
        Battlecruisers can attack while moving, 
        do the same damage to both ground and air targets, and fire faster.
    """),
    item_names.BATTLECRUISER_OPTIMIZED_LOGISTICS: "Increases Battlecruiser training speed.",
    item_names.BATTLECRUISER_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Battlecruisers", "Starport"),
    item_names.GHOST_EMP_ROUNDS: inspect.cleandoc("""
        Spell. Does 100 damage to shields and drains all energy from units in the targeted area. 
        Cloaked units hit by EMP are revealed for a short time.
    """),
    item_names.GHOST_LOCKDOWN: "Spell. Stuns a target mechanical unit for a long time.",
    item_names.SPECTRE_IMPALER_ROUNDS: "Spectres do additional damage to armored targets.",
    item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD: inspect.cleandoc(f"""
        Level 1: Allows Thors to transform in order to use an alternative air attack.
        Level 2: {SMART_SERVOS_DESCRIPTION}
    """),
    item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE: "Spell. Deploys a drone that can heal biological or mechanical units.",
    item_names.RAVEN_SPIDER_MINES: "Spell. Deploys 3 Spider Mines to a target location.",
    item_names.RAVEN_RAILGUN_TURRET: inspect.cleandoc("""
        Spell. Allows Ravens to deploy an advanced Auto-Turret, that can attack enemy ground units in a straight line.
    """),
    item_names.RAVEN_HUNTER_SEEKER_WEAPON: "Allows Ravens to attack with a Hunter-Seeker weapon.",
    item_names.RAVEN_INTERFERENCE_MATRIX: inspect.cleandoc("""
        Spell. Target enemy Mechanical or Psionic unit can't attack or use abilities for a short duration.
    """),
    item_names.RAVEN_ANTI_ARMOR_MISSILE: "Spell. Decreases target and nearby enemy units armor by 2.",
    item_names.RAVEN_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Ravens", "Starport"),
    item_names.SCIENCE_VESSEL_EMP_SHOCKWAVE: "Spell. Depletes all energy and shields of all units in a target area.",
    item_names.SCIENCE_VESSEL_DEFENSIVE_MATRIX: inspect.cleandoc("""
        Spell. Provides a target unit with a defensive barrier that can absorb up to 250 damage.
    """),
    item_names.CYCLONE_TARGETING_OPTICS: "Increases Cyclone Lock On casting range and the range while Locked On.",
    item_names.CYCLONE_RAPID_FIRE_LAUNCHERS: "The first 12 shots of Lock On are fired more quickly.",
    item_names.LIBERATOR_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Liberators"),
    item_names.LIBERATOR_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    item_names.LIBERATOR_OPTIMIZED_LOGISTICS: "Increases Liberator training speed.",
    item_names.WIDOW_MINE_BLACK_MARKET_LAUNCHERS: "Increases Widow Mine Sentinel Missile range.",
    item_names.WIDOW_MINE_EXECUTIONER_MISSILES: inspect.cleandoc("""
        Reduces Sentinel Missile cooldown.
        When killed, Widow Mines will launch several missiles at random enemy targets.
    """),
    item_names.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS: "Valkyries fire 2 additional rockets each volley.",
    item_names.VALKYRIE_SHAPED_HULL: "Increases Valkyrie life by 50.",
    item_names.VALKYRIE_FLECHETTE_MISSILES: "Equips Valkyries with Air-to-Surface missiles to attack ground units.",
    item_names.VALKYRIE_AFTERBURNERS: "Ability. Temporarily increases the Valkyries's movement speed by 70%.",
    item_names.CYCLONE_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Cyclones", "Factory"),
    item_names.LIBERATOR_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    item_names.LIBERATOR_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.LIBERATOR),
    item_names.HERCULES_INTERNAL_FUSION_MODULE: "Hercules can be trained from a Starport without having a Fusion Core.",
    item_names.HERCULES_TACTICAL_JUMP: inspect.cleandoc("""
        Allows Hercules to warp to a target location anywhere on the map.
    """),
    item_names.PLANETARY_FORTRESS_PROGRESSIVE_AUGMENTED_THRUSTERS: inspect.cleandoc("""
        Level 1: Lift Off - Planetary Fortress can lift off.
        Level 2: Armament Stabilizers - Planetary Fortress can attack while lifted off.
    """),
    item_names.PLANETARY_FORTRESS_ADVANCED_TARGETING: "Planetary Fortress can attack air units.",
    item_names.VALKYRIE_LAUNCHING_VECTOR_COMPENSATOR: "Allows Valkyries to shoot air while moving.",
    item_names.VALKYRIE_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.VALKYRIE),
    item_names.PREDATOR_PREDATOR_S_FURY: "Predators can use an attack that jumps between targets.",
    item_names.BATTLECRUISER_BEHEMOTH_PLATING: "Increases Battlecruiser armor by 2.",
    item_names.BATTLECRUISER_COVERT_OPS_ENGINES: "Increases Battlecruiser movement speed.",
    item_names.PLANETARY_FORTRESS_ORBITAL_MODULE: inspect.cleandoc("""
        Allows Planetary Fortresses to use Scanner Sweep, MULE, and Extra Supplies if those abilities are owned.
    """),
    item_names.DEVASTATOR_TURRET_CONCUSSIVE_GRENADES: "Devastator Turrets slow enemies they hit. Does not stack with Marauder Concussive Shells.",
    item_names.DEVASTATOR_TURRET_ANTI_ARMOR_MUNITIONS: "Increases Devastator Turret damage to armored targets by 10.",
    item_names.DEVASTATOR_TURRET_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.DEVASTATOR_TURRET),
    item_names.MISSILE_TURRET_RESOURCE_EFFICENCY: _get_resource_efficiency_desc(item_names.MISSILE_TURRET),
    item_names.SCIENCE_VESSEL_TACTICAL_JUMP: "Allows Science Vessels to warp to a target location anywhere on the map.",
    item_names.LIBERATOR_COMPRESSED_ROCKET_FUEL: "Increases Liberator attack range in Fighter mode by 4.",
    item_names.BUNKER: "Defensive structure. Able to load infantry units, giving them +1 range to their attacks.",
    item_names.MISSILE_TURRET: "Anti-air defensive structure.",
    item_names.SENSOR_TOWER: "Reveals locations of enemy units at long range.",
    item_names.WAR_PIGS: "Mercenary Marines.",
    item_names.DEVIL_DOGS: "Mercenary Firebats.",
    item_names.HAMMER_SECURITIES: "Mercenary Marauders.",
    item_names.SPARTAN_COMPANY: "Mercenary Goliaths.",
    item_names.SIEGE_BREAKERS: "Mercenary Siege Tanks.",
    item_names.HELS_ANGELS: "Mercenary Vikings.",
    item_names.DUSK_WINGS: "Mercenary Banshees.",
    item_names.JACKSONS_REVENGE: "Mercenary Battlecruiser.",
    item_names.SKIBIS_ANGELS: "Mercenary Medics.",
    item_names.DEATH_HEADS: "Mercenary Reapers.",
    item_names.WINGED_NIGHTMARES: "Mercenary Wraiths.",
    item_names.MIDNIGHT_RIDERS: "Mercenary Liberators.",
    item_names.BRYNHILDS: "Mercenary Valkyries.",
    item_names.JOTUN: "Mercenary Thor.",
    item_names.ULTRA_CAPACITORS: "Increases attack speed of units by 5% per weapon upgrade.",
    item_names.VANADIUM_PLATING: "Increases the life of units by 5% per armor upgrade.",
    item_names.ORBITAL_DEPOTS: "Supply depots are built instantly.",
    item_names.MICRO_FILTERING: "Refineries produce Vespene gas 25% faster.",
    item_names.AUTOMATED_REFINERY: "Eliminates the need for SCVs in vespene gas production.",
    item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR: "Command Centers can train two SCVs at once.",
    item_names.RAVEN: "Aerial Caster unit.",
    item_names.SCIENCE_VESSEL: "Aerial Caster unit. Can repair mechanical units.",
    item_names.TECH_REACTOR: "Merges Tech Labs and Reactors into one add on structure to provide both functions.",
    item_names.ORBITAL_STRIKE: "Trained units from Barracks are instantly deployed on rally point.",
    item_names.BUNKER_SHRIKE_TURRET: "Adds an automated turret to Bunkers.",
    item_names.BUNKER_FORTIFIED_BUNKER: "Bunkers have more life.",
    item_names.PLANETARY_FORTRESS: inspect.cleandoc("""
        Allows Command Centers to upgrade into a defensive structure with a turret and additional armor.
        Planetary Fortresses cannot Lift Off, or cast Orbital Command spells.
    """),
    item_names.PERDITION_TURRET: "Automated defensive turret. Burrows down while no enemies are nearby.",
    item_names.PREDATOR: "Anti-infantry specialist that deals area damage with each attack.",
    item_names.HERCULES: "Massive transport ship.",
    item_names.CELLULAR_REACTOR: "All Terran spellcasters get +100 starting and maximum energy.",
    item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL: inspect.cleandoc("""
        Allows Terran mechanical units to regenerate health while not in combat.
        Each level increases life regeneration speed.
    """),
    item_names.HIVE_MIND_EMULATOR: "Defensive structure. Can permanently Mind Control Zerg units.",
    item_names.PSI_DISRUPTER: "Defensive structure. Slows the attack and movement speeds of all nearby Zerg units.",
    item_names.DEVASTATOR_TURRET: "Defensive structure. Deals increased damage to armored targets. Attacks ground units.",
    item_names.STRUCTURE_ARMOR: "Increases armor of all Terran structures by 2.",
    item_names.HI_SEC_AUTO_TRACKING: "Increases attack range of all Terran structures by 1.",
    item_names.ADVANCED_OPTICS: "Increases attack range of all Terran mechanical units by 1.",
    item_names.ROGUE_FORCES: "Mercenary calldowns are no longer limited by charges.",
    item_names.MECHANICAL_KNOW_HOW: "Increases mechanical unit life by 20%.",
    item_names.MERCENARY_MUNITIONS: "Increases attack speed of all combat units by 15%.",
    item_names.FAST_DELIVERY: "Mercenary calldowns can be deployed right at the mission start.",
    item_names.RAPID_REINFORCEMENT: "Halves cooldowns of mercenary calldowns.",
    item_names.ZEALOT: "Powerful melee warrior. Can use the charge ability.",
    item_names.STALKER: "Ranged attack strider. Can use the Blink ability.",
    item_names.HIGH_TEMPLAR: "Potent psionic master. Can use the Feedback and Psionic Storm abilities. Can merge into an Archon.",
    item_names.DARK_TEMPLAR: "Deadly warrior-assassin. Permanently cloaked. Can use the Shadow Fury ability.",
    item_names.IMMORTAL: "Assault strider. Can use Barrier to absorb damage.",
    item_names.COLOSSUS: "Battle strider with a powerful area attack. Can walk up and down cliffs. Attacks set fire to the ground, dealing extra damage to enemies over time.",
    item_names.PHOENIX: "Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities.",
    item_names.VOID_RAY: "Surgical strike craft. Has the Prismatic Alignment and Prismatic Range abilities.",
    item_names.CARRIER: "Capital ship. Builds and launches Interceptors that attack enemy targets. Repair Drones heal nearby mechanical units.",
    item_names.STARTING_MINERALS: "Increases the starting minerals for all missions.",
    item_names.STARTING_VESPENE: "Increases the starting vespene for all missions.",
    item_names.STARTING_SUPPLY: "Increases the starting supply for all missions.",
    item_names.NOTHING: "Does nothing. Used to remove a location from the game.",
    item_names.NOVA_GHOST_VISOR: "Reveals the locations of enemy units in the fog of war around Nova. Can detect cloaked units.",
    item_names.NOVA_RANGEFINDER_OCULUS: "Increases Nova's vision range and non-melee weapon attack range by 2. Also increases range of melee weapons by 1.",
    item_names.NOVA_DOMINATION: "Gives Nova the ability to mind-control a target enemy unit.",
    item_names.NOVA_BLINK: "Gives Nova the ability to teleport a short distance and cloak for 10s.",
    item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE: inspect.cleandoc("""
        Level 1: Gives Nova the ability to cloak.
        Level 2: Nova is permanently cloaked.
    """),
    item_names.NOVA_ENERGY_SUIT_MODULE: "Increases Nova's maximum energy and energy regeneration rate.",
    item_names.NOVA_ARMORED_SUIT_MODULE: "Increases Nova's health by 100 and armour by 1. Nova also regenerates life quickly out of combat.",
    item_names.NOVA_JUMP_SUIT_MODULE: "Increases Nova's movement speed and allows her to jump up and down cliffs.",
    item_names.NOVA_C20A_CANISTER_RIFLE: "Allows Nova to equip the C20A Canister Rifle, which has a ranged attack and allows Nova to cast Snipe.",
    item_names.NOVA_HELLFIRE_SHOTGUN: "Allows Nova to equip the Hellfire Shotgun, which has a short-range area attack in a cone and allows Nova to cast Penetrating Blast.",
    item_names.NOVA_PLASMA_RIFLE: "Allows Nova to equip the Plasma Rifle, which has a rapidfire ranged attack and allows Nova to cast Plasma Shot.",
    item_names.NOVA_MONOMOLECULAR_BLADE: "Allows Nova to equip the Monomolecular Blade, which has a melee attack and allows Nova to cast Dash Attack.",
    item_names.NOVA_BLAZEFIRE_GUNBLADE: "Allows Nova to equip the Blazefire Gunblade, which has a melee attack and allows Nova to cast Fury of One.",
    item_names.NOVA_STIM_INFUSION: "Gives Nova the ability to heal herself and temporarily increase her movement and attack speeds.",
    item_names.NOVA_PULSE_GRENADES: "Gives Nova the ability to throw a grenade dealing large damage in an area.",
    item_names.NOVA_FLASHBANG_GRENADES: "Gives Nova the ability to throw a grenade to stun enemies and disable detection in a large area.",
    item_names.NOVA_IONIC_FORCE_FIELD: "Gives Nova the ability to shield herself temporarily.",
    item_names.NOVA_HOLO_DECOY: "Gives Nova the ability to summon a decoy unit which enemies will prefer to target and takes reduced damage.",
    item_names.NOVA_NUKE: "Gives Nova the ability to launch tactical nukes built from the Shadow Ops.",
    item_names.ZERGLING: "Fast inexpensive melee attacker. Hatches in pairs from a single larva. Can morph into a Baneling.",
    item_names.SWARM_QUEEN: "Ranged support caster. Can use the Spawn Creep Tumor and Rapid Transfusion abilities.",
    item_names.ROACH: "Durable short ranged attacker. Regenerates life quickly when burrowed.",
    item_names.HYDRALISK: "High-damage generalist ranged attacker.",
    item_names.ZERGLING_BANELING_ASPECT: "Anti-ground suicide unit. Does damage over a small area on death. Morphed from the Zergling.",
    item_names.ABERRATION: "Durable melee attacker that deals heavy damage and can walk over other units.",
    item_names.MUTALISK: "Fragile flying attacker. Attacks bounce between targets.",
    item_names.SWARM_HOST: "Siege unit that attacks by rooting in place and continually spawning Locusts.",
    item_names.INFESTOR: "Support caster that can move while burrowed. Can use the Fungal Growth, Parasitic Domination, and Consumption abilities.",
    item_names.ULTRALISK: "Massive melee attacker. Has an area-damage cleave attack.",
    item_names.SPORE_CRAWLER: "Anti-air defensive structure that can detect cloaked units.",
    item_names.SPINE_CRAWLER: "Anti-ground defensive structure.",
    item_names.CORRUPTOR: "Anti-air flying attacker specializing in taking down enemy capital ships.",
    item_names.SCOURGE: "Flying anti-air suicide unit. Hatches in pairs from a single larva.",
    item_names.BROOD_QUEEN: "Flying support caster. Can cast the Ocular Symbiote and Spawn Broodlings abilities.",
    item_names.DEFILER: "Support caster. Can use the Dark Swarm, Consume, and Plague abilities.",
    item_names.INFESTED_MARINE: "General-purpose Infested infantry. Has a timed life of 90 seconds.",
    item_names.INFESTED_BUNKER: "Defensive structure. Periodically spawns Infested infantry that fight from inside. Acts as a mobile ground transport while uprooted.",
    item_names.PROGRESSIVE_ZERG_MELEE_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "melee ground units"),
    item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "ranged ground units"),
    item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "ground units"),
    item_names.PROGRESSIVE_ZERG_FLYER_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "flyers"),
    item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "flyers"),
    item_names.PROGRESSIVE_ZERG_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "units"),
    item_names.PROGRESSIVE_ZERG_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "units"),
    item_names.PROGRESSIVE_ZERG_GROUND_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "ground units"),
    item_names.PROGRESSIVE_ZERG_FLYER_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "flyers"),
    item_names.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "units"),
    item_names.ZERGLING_HARDENED_CARAPACE: "Increases Zergling health by +10.",
    item_names.ZERGLING_ADRENAL_OVERLOAD: "Increases Zergling attack speed.",
    item_names.ZERGLING_METABOLIC_BOOST: "Increases Zergling movement speed.",
    item_names.ROACH_HYDRIODIC_BILE: "Roaches deal +8 damage to light targets.",
    item_names.ROACH_ADAPTIVE_PLATING: "Roaches gain +3 armour when their life is below 50%.",
    item_names.ROACH_TUNNELING_CLAWS: "Allows Roaches to move while burrowed.",
    item_names.HYDRALISK_FRENZY: "Allows Hydralisks to use the Frenzy ability, which increases their attack speed by 50%.",
    item_names.HYDRALISK_ANCILLARY_CARAPACE: "Hydralisks gain +20 health.",
    item_names.HYDRALISK_GROOVED_SPINES: "Hydralisks gain +1 range.",
    item_names.BANELING_CORROSIVE_ACID: "Increases the damage banelings deal to their primary target. Splash damage remains the same.",
    item_names.BANELING_RUPTURE: "Increases the splash radius of baneling attacks.",
    item_names.BANELING_REGENERATIVE_ACID: "Banelings will heal nearby friendly units when they explode.",
    item_names.MUTALISK_VICIOUS_GLAIVE: "Mutalisks attacks will bounce an additional 3 times.",
    item_names.MUTALISK_RAPID_REGENERATION: "Mutalisks will regenerate quickly when out of combat.",
    item_names.MUTALISK_SUNDERING_GLAIVE: "Mutalisks deal increased damage to their primary target.",
    item_names.SWARM_HOST_BURROW: "Allows Swarm Hosts to burrow instead of root to spawn locusts.",
    item_names.SWARM_HOST_RAPID_INCUBATION: "Swarm Hosts will spawn locusts 20% faster.",
    item_names.SWARM_HOST_PRESSURIZED_GLANDS: "Allows Swarm Host Locusts to attack air targets.",
    item_names.ULTRALISK_BURROW_CHARGE: "Allows Ultralisks to burrow and charge at enemy units, knocking back and stunning units when it emerges.",
    item_names.ULTRALISK_TISSUE_ASSIMILATION: "Ultralisks recover health when they deal damage.",
    item_names.ULTRALISK_MONARCH_BLADES: "Ultralisks gain increased splash damage.",
    item_names.CORRUPTOR_CAUSTIC_SPRAY: "Allows Corruptors to use the Caustic Spray ability, which deals ramping damage to buildings over time.",
    item_names.CORRUPTOR_CORRUPTION: "Allows Corruptors to use the Corruption ability, which causes a target enemy unit to take increased damage.",
    item_names.SCOURGE_VIRULENT_SPORES: "Scourge will deal splash damage.",
    item_names.SCOURGE_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SCOURGE),
    item_names.SCOURGE_SWARM_SCOURGE: "An extra Scourge will be built from each egg at no additional cost.",
    item_names.ZERGLING_SHREDDING_CLAWS: "Zergling attacks will temporarily reduce their target's armour to 0.",
    item_names.ROACH_GLIAL_RECONSTITUTION: "Increases Roach movement speed.",
    item_names.ROACH_ORGANIC_CARAPACE: "Increases Roach health by +25.",
    item_names.HYDRALISK_MUSCULAR_AUGMENTS: "Increases Hydralisk movement speed.",
    item_names.HYDRALISK_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.HYDRALISK),
    item_names.BANELING_CENTRIFUGAL_HOOKS: "Increases the movement speed of Banelings.",
    item_names.BANELING_TUNNELING_JAWS: "Allows Banelings to move while burrowed.",
    item_names.BANELING_RAPID_METAMORPH: "Banelings morph faster.",
    item_names.MUTALISK_SEVERING_GLAIVE: "Mutalisk bounce attacks will deal full damage.",
    item_names.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE: "Increases the attack range of Mutalisks by 2.",
    item_names.SWARM_HOST_LOCUST_METABOLIC_BOOST: "Increases Locust movement speed.",
    item_names.SWARM_HOST_ENDURING_LOCUSTS: "Increases the duration of Swarm Hosts' Locusts by 10s.",
    item_names.SWARM_HOST_ORGANIC_CARAPACE: "Increases Swarm Host health by +40.",
    item_names.SWARM_HOST_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SWARM_HOST),
    item_names.ULTRALISK_ANABOLIC_SYNTHESIS: "Ultralisks gain increased movement speed.",
    item_names.ULTRALISK_CHITINOUS_PLATING: "Ultralisks gain +2 armor.",
    item_names.ULTRALISK_ORGANIC_CARAPACE: "Ultralisks gain +100 life.",
    item_names.ULTRALISK_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.ULTRALISK),
    item_names.DEVOURER_CORROSIVE_SPRAY: "Devourer attacks will now deal area damage.",
    item_names.DEVOURER_GAPING_MAW: "Devourer's attack speed increased by 25%.",
    item_names.DEVOURER_IMPROVED_OSMOSIS: "Devourer's Acid Spores duration increased by 50%.",
    item_names.DEVOURER_PRESCIENT_SPORES: "Allows Devourers to attack ground targets.",
    item_names.GUARDIAN_PROLONGED_DISPERSION: "Guardians gain +3 range.",
    item_names.GUARDIAN_PRIMAL_ADAPTATION: "Allows Guardians to attack air units with a decreased attack damage.",
    item_names.GUARDIAN_SORONAN_ACID: "Guardians deal increased damage to ground targets.",
    item_names.IMPALER_ADAPTIVE_TALONS: "Impalers burrow faster.",
    item_names.IMPALER_SECRETION_GLANDS: "Impalers generate creep while standing still or burrowed.",
    item_names.IMPALER_HARDENED_TENTACLE_SPINES: "Impalers deal increased damage.",
    item_names.LURKER_SEISMIC_SPINES: "Lurkers gain +6 range.",
    item_names.LURKER_ADAPTED_SPINES: "Lurkers deal increased damage to non-light targets.",
    item_names.RAVAGER_POTENT_BILE: "Ravager Corrosive Bile deals an additional +40 damage.",
    item_names.RAVAGER_BLOATED_BILE_DUCTS: "Ravager Corrosive Bile hits a much larger area.",
    item_names.RAVAGER_DEEP_TUNNEL: _ability_desc("Ravagers", "Deep Tunnel", "allows them to burrow to any visible location on the map"),
    item_names.VIPER_PARASITIC_BOMB: _ability_desc("Vipers", "Parasitic Bomb", "inflicts an area-damaging effect on an enemy air unit"),
    item_names.VIPER_PARALYTIC_BARBS: "Viper Abduct stuns units for an additional 5 seconds.",
    item_names.VIPER_VIRULENT_MICROBES: "All Viper abilities gain +4 range.",
    item_names.BROOD_LORD_POROUS_CARTILAGE: "Brood Lords gain increased movement speed.",
    item_names.BROOD_LORD_EVOLVED_CARAPACE: "Brood Lords gain +100 life and +1 armor.",
    item_names.BROOD_LORD_SPLITTER_MITOSIS: "Brood Lord attacks spawn twice as many broodlings.",
    item_names.BROOD_LORD_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(DISPLAY_NAME_BROOD_LORD),
    item_names.INFESTOR_INFESTED_TERRAN: _ability_desc("Infestors", "Spawn Infested Terran"),
    item_names.INFESTOR_MICROBIAL_SHROUD: _ability_desc("Infestors", "Microbial Shroud", "reduces incoming damage from air units in an area"),
    item_names.SWARM_QUEEN_SPAWN_LARVAE: _ability_desc("Swarm Queens", "Spawn Larvae"),
    item_names.SWARM_QUEEN_DEEP_TUNNEL: _ability_desc("Swarm Queens", "Deep Tunnel"),
    item_names.SWARM_QUEEN_ORGANIC_CARAPACE: "Swarm Queens gain +25 life.",
    item_names.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION: "Swarm Queen Burst Heal heals an additional +10 life and can now target mechanical units.",
    item_names.SWARM_QUEEN_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SWARM_QUEEN),
    item_names.SWARM_QUEEN_INCUBATOR_CHAMBER: "Swarm Queens may now be built two at a time from the Hatchery, Lair, or Hive.",
    item_names.BROOD_QUEEN_FUNGAL_GROWTH: _ability_desc("Brood Queens", "Fungal Growth"),
    item_names.BROOD_QUEEN_ENSNARE: _ability_desc("Brood Queens", "Ensnare"),
    item_names.BROOD_QUEEN_ENHANCED_MITOCHONDRIA: "Brood Queens start with maximum energy and gain increased energy regeneration. Like powerhouses (of the cell).",
    item_names.DEFILER_PATHOGEN_PROJECTORS: "Defilers gain +4 cast range for Dark Swarm and Plague.",
    item_names.DEFILER_TRAPDOOR_ADAPTATION: "Defilers can now use abilities while burrowed.",
    item_names.DEFILER_PREDATORY_CONSUMPTION: "Defilers can now use Consume on any non-heroic biological unit, not just friendly Zerg.",
    item_names.DEFILER_COMORBIDITY: "Plague now stacks up to three times, and depletes energy as well as health.",
    item_names.ABERRATION_MONSTROUS_RESILIENCE: "Aberrations gain +140 life.",
    item_names.ABERRATION_CONSTRUCT_REGENERATION: "Aberrations gain increased life regeneration.",
    item_names.ABERRATION_PROTECTIVE_COVER: "Aberrations grant damage reduction to allied units directly beneath them.",
    item_names.ABERRATION_BANELING_INCUBATION: "Aberrations spawn 2 Banelings upon death.",
    item_names.ABERRATION_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.ABERRATION),
    item_names.CORRUPTOR_MONSTROUS_RESILIENCE: "Corruptors gain +100 life.",
    item_names.CORRUPTOR_CONSTRUCT_REGENERATION: "Corruptors gain increased life regeneration.",
    item_names.CORRUPTOR_SCOURGE_INCUBATION: "Corruptors spawn 2 Scourge upon death (3 with Swarm Scourge).",
    item_names.CORRUPTOR_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.CORRUPTOR),
    item_names.PRIMAL_IGNITER_CONCENTRATED_FIRE: "Primal Igniters deal +15 damage vs light armor.",
    item_names.PRIMAL_IGNITER_PRIMAL_TENACITY: "Primal Igniters gain +100 health and +1 armor.",
    item_names.INFESTED_SCV_BUILD_CHARGES: "Starting Infested SCV charges increased to 3. Maximum charges increased to 5.",
    item_names.INFESTED_MARINE_PLAGUED_MUNITIONS: "Infested Marines deal an extra 50 damage over 15 seconds to targets they attack.",
    item_names.INFESTED_MARINE_RETINAL_AUGMENTATION: "Infested Marines gain +1 range.",
    item_names.INFESTED_BUNKER_CALCIFIED_ARMOR: "Infested Bunkers gain +3 armor.",
    item_names.INFESTED_BUNKER_REGENERATIVE_PLATING: "Infested Bunkers gain increased life regeneration while rooted.",
    item_names.INFESTED_BUNKER_ENGORGED_BUNKERS: "Infested Bunkers gain +2 cargo slots. Infested Trooper spawn cooldown is reduced by 20%.",
    item_names.TYRANNOZOR_TYRANTS_PROTECTION: "Tyrannozors grants nearby friendly units 2 armor.",
    item_names.TYRANNOZOR_BARRAGE_OF_SPIKES: "Unleash a Barrage of Spikes, dealing 100 damage to enemy ground and air units around the Tyrannozor.",
    item_names.TYRANNOZOR_IMPALING_STRIKE: "Ultralisk and Tyrannozor melee attacks have a 20% chance to stun for 2 seconds.",
    item_names.TYRANNOZOR_HEALING_ADAPTATION: "Ultralisks and Tyrannozors regenerate life quickly when out of combat.",
    item_names.ZERGLING_RAPTOR_STRAIN: "Allows Zerglings to jump up and down cliffs and leap onto enemies. Also increases Zergling attack damage by 2.",
    item_names.ZERGLING_SWARMLING_STRAIN: "Zerglings will spawn instantly and with an extra Zergling per egg at no additional cost.",
    item_names.ROACH_VILE_STRAIN: "Roach attacks will slow the movement and attack speed of enemies.",
    item_names.ROACH_CORPSER_STRAIN: "Units killed after being attacked by Roaches will spawn 2 Roachlings.",
    item_names.HYDRALISK_IMPALER_ASPECT: "Allows Hydralisks to morph into Impalers.",
    item_names.HYDRALISK_LURKER_ASPECT: "Allows Hydralisks to morph into Lurkers.",
    item_names.BANELING_SPLITTER_STRAIN: "Banelings will split into two smaller Splitterlings on exploding.",
    item_names.BANELING_HUNTER_STRAIN: "Allows Banelings to jump up and down cliffs and leap onto enemies.",
    item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT: "Allows Mutalisks and Corruptors to morph into Brood Lords.",
    item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT: "Allows Mutalisks and Corruptors to morph into Vipers.",
    item_names.SWARM_HOST_CARRION_STRAIN: "Swarm Hosts will spawn Flying Locusts.",
    item_names.SWARM_HOST_CREEPER_STRAIN: "Allows Swarm Hosts to teleport to any creep on the map in vision. Swarm Hosts will spread creep around them when rooted or burrowed.",
    item_names.ULTRALISK_NOXIOUS_STRAIN: "Ultralisks will periodically spread poison, damaging nearby biological enemies.",
    item_names.ULTRALISK_TORRASQUE_STRAIN: "Ultralisks will revive after being killed.",
    item_names.KERRIGAN_KINETIC_BLAST: "Kerrigan deals 300 damage to target unit or structure from long range.",
    item_names.KERRIGAN_HEROIC_FORTITUDE: "Kerrigan gains +200 maximum life and double life regeneration rate.",
    item_names.KERRIGAN_LEAPING_STRIKE: "Kerrigan leaps to her target and deals 150 damage.",
    item_names.KERRIGAN_CRUSHING_GRIP: "Kerrigan stuns enemies in a target area for 3 seconds and deals 30 damage over time. Heroic units are not stunned.",
    item_names.KERRIGAN_CHAIN_REACTION: "Kerrigan's attacks deal normal damage to her target then jump to additional nearby enemies.",
    item_names.KERRIGAN_PSIONIC_SHIFT: "Kerrigan dashes through enemies, dealing 50 damage to all enemies in her path.",
    item_names.ZERGLING_RECONSTITUTION: "Killed Zerglings respawn from your primary Hatchery at no cost.",
    item_names.OVERLORD_IMPROVED_OVERLORDS: "Overlords morph instantly and provide 50% more supply.",
    item_names.AUTOMATED_EXTRACTORS: "Extractors automatically harvest Vespene Gas without the need for Drones.",
    item_names.KERRIGAN_WILD_MUTATION: "Kerrigan gives all units in an area +200 max life and double attack speed for 10 seconds.",
    item_names.KERRIGAN_SPAWN_BANELINGS: "Kerrigan spawns six Banelings with timed life.",
    item_names.KERRIGAN_MEND: "Kerrigan heals for 150 life and heals nearby friendly units for 50 life. An additional +50% life is healed over 15 seconds.",
    item_names.TWIN_DRONES: "Drones morph in groups of two at no additional cost and require less supply.",
    item_names.MALIGNANT_CREEP: "Your units and structures gain increased life regeneration and 30% increased attack speed while on creep. Creep Tumors also spread creep faster and farther.",
    item_names.VESPENE_EFFICIENCY: "Extractors produce Vespene gas 25% faster.",
    item_names.ZERG_CREEP_STOMACH: "Zerg buildings no longer take damage off-creep. Spore and Spine Crawlers can now root off-creep.",
    item_names.KERRIGAN_INFEST_BROODLINGS: "Enemies damaged by Kerrigan become infested and will spawn Broodlings with timed life if killed quickly.",
    item_names.KERRIGAN_FURY: "Each of Kerrigan's attacks temporarily increase her attack speed by 15%. Can stack up to 75%.",
    item_names.KERRIGAN_ABILITY_EFFICIENCY: "Kerrigan's abilities have their cooldown and energy cost reduced by 20%.",
    item_names.KERRIGAN_APOCALYPSE: "Kerrigan deals 300 damage (+400 vs Structure) to enemies in a large area.",
    item_names.KERRIGAN_SPAWN_LEVIATHAN: "Kerrigan summons a mightly flying Leviathan with timed life. Deals massive damage and has energy-based abilities.",
    item_names.KERRIGAN_DROP_PODS: "Kerrigan drops Primal Zerg forces with timed life to the battlefield.",
    item_names.KERRIGAN_PRIMAL_FORM: "Kerrigan takes on her Primal Zerg form and gains greatly increased energy regeneration.",
    item_names.KERRIGAN_LEVELS_10: "Gives Kerrigan +10 Levels.",
    item_names.KERRIGAN_LEVELS_9: "Gives Kerrigan +9 Levels.",
    item_names.KERRIGAN_LEVELS_8: "Gives Kerrigan +8 Levels.",
    item_names.KERRIGAN_LEVELS_7: "Gives Kerrigan +7 Levels.",
    item_names.KERRIGAN_LEVELS_6: "Gives Kerrigan +6 Levels.",
    item_names.KERRIGAN_LEVELS_5: "Gives Kerrigan +5 Levels.",
    item_names.KERRIGAN_LEVELS_4: "Gives Kerrigan +4 Levels.",
    item_names.KERRIGAN_LEVELS_3: "Gives Kerrigan +3 Levels.",
    item_names.KERRIGAN_LEVELS_2: "Gives Kerrigan +2 Levels.",
    item_names.KERRIGAN_LEVELS_1: "Gives Kerrigan +1 Level.",
    item_names.KERRIGAN_LEVELS_14: "Gives Kerrigan +14 Levels.",
    item_names.KERRIGAN_LEVELS_35: "Gives Kerrigan +35 Levels.",
    item_names.KERRIGAN_LEVELS_70: "Gives Kerrigan +70 Levels.",
    item_names.INFESTED_MEDICS: "Mercenary infested Medics that may be called in from the Hatchery.",
    item_names.INFESTED_SIEGE_TANKS: "Mercenary infested Siege Tanks that may be called in from the Hatchery.",
    item_names.INFESTED_BANSHEES: "Mercenary infested Banshees that may be called in from the Hatchery.",
    item_names.OVERLORD_VENTRAL_SACS: "Overlords gain the ability to transport ground units.",
    item_names.OVERLORD_GENERATE_CREEP: "Overlords gain the ability to generate creep while standing still.",
    item_names.OVERLORD_ANTENNAE: "Increases Overlord sight range.",
    item_names.OVERLORD_PNEUMATIZED_CARAPACE: "Increases Overlord movement speed.",
    item_names.OVERLORD_OVERSEER_ASPECT: "Allows to morph Overlords into Overseers. Overseers can use Spawn Creep Tumor and Contaminate abilities.",
    item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT: "Long-range anti-ground flyer. Can attack ground units. Morphed from the Mutalisk or Corruptor.",
    item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT: "Anti-air flyer. Attack inflict Acid Spores. Can attack air units. Morphed from the Mutalisk or Corruptor.",
    item_names.ROACH_RAVAGER_ASPECT: "Ranged artillery. Can use Corrosive Bile. Can attack ground units. Morphed from the Roach.",
    item_names.ROACH_PRIMAL_IGNITER_ASPECT: "Assault unit. Has an area-damage attack. Regenerates life quickly when burrowed. Can attack ground units. Morphed by merging two Roaches.",
    item_names.ULTRALISK_TYRANNOZOR_ASPECT: "Heavy assault beast. Has a ground-area attack, and powerful anti-air attack.  Morphed by merging two Ultralisks.",
    item_names.OBSERVER: "Flying spy. Cloak renders the unit invisible to enemies without detection.",
    item_names.CENTURION: "Powerful melee warrior. Has the Shadow Charge and Darkcoil abilities.",
    item_names.SENTINEL: "Powerful melee warrior. Has the Charge and Reconstruction abilities.",
    item_names.SUPPLICANT: "Powerful melee warrior. Has powerful damage resistant shields.",
    item_names.INSTIGATOR: "Ranged support strider. Can store multiple Blink charges.",
    item_names.SLAYER: "Ranged attack strider. Can use the Phase Blink and Phasing Armor abilities.",
    item_names.SENTRY: "Robotic support unit can use the Guardian Shield ability and restore the shields of nearby Protoss units.",
    item_names.ENERGIZER: "Robotic support unit. Can use the Chrono Beam ability and become stationary to power nearby structures.",
    item_names.HAVOC: "Robotic support unit. Can use the Target Lock and Force Field abilities and increase the range of nearby Protoss units.",
    item_names.SIGNIFIER: "Potent permanently cloaked psionic master. Can use the Feedback and Crippling Psionic Storm abilities. Can merge into an Archon.",
    item_names.ASCENDANT: "Potent psionic master. Can use the Psionic Orb, Mind Blast, and Sacrifice abilities.",
    item_names.AVENGER: "Deadly warrior-assassin. Permanently cloaked. Recalls to the nearest Dark Shrine upon death.",
    item_names.BLOOD_HUNTER: "Deadly warrior-assassin. Permanently cloaked. Can use the Void Stasis ability.",
    item_names.DRAGOON: "Ranged assault strider. Has enhanced health and damage.",
    item_names.DARK_ARCHON: "Potent psionic master. Can use the Confuse and Mind Control abilities.",
    item_names.ADEPT: "Ranged specialist. Can use the Psionic Transfer ability.",
    item_names.WARP_PRISM: "Flying transport. Can carry units and become stationary to deploy a power field.",
    item_names.ANNIHILATOR: "Assault Strider. Can use the Shadow Cannon ability to damage air and ground units.",
    item_names.STALWART: "Assault strider. Has shields that deflect high-damage attacks.",
    item_names.VANGUARD: "Assault Strider. Deals splash damage around the primary target.",
    item_names.WRATHWALKER: "Battle strider with a powerful single target attack.  Can walk up and down cliffs.",
    item_names.REAVER: "Area damage siege unit. Builds and launches explosive Scarabs for high burst damage.",
    item_names.DISRUPTOR: "Robotic disruption unit. Can use the Purification Nova ability to deal heavy area damage.",
    item_names.MIRAGE: "Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities.",
    item_names.SKIRMISHER: "Fast skirmish starfighter.",
    item_names.CORSAIR: "Air superiority starfighter. Can use the Disruption Web ability.",
    item_names.DESTROYER: "Area assault craft. Can use the Destruction Beam ability to attack multiple units at once.",
    item_names.WARP_RAY: "Surgical-strike craft. Damage output increases the longer the Warp Ray remains on target.",
    item_names.DAWNBRINGER: "Flying Anti-Surface Assault Ship. Attacks in an area around the target. Attack count increases as it continues firing.",
    item_names.SCOUT: "Versatile high-speed fighter.",
    item_names.TEMPEST: "Siege artillery craft. Attacks from long range. Can use the Disintegration ability.",
    item_names.MOTHERSHIP: "Ultimate Protoss vessel, Can use the Vortex and Mass Recall abilities. Cloaks nearby units and structures.",
    item_names.ARBITER: "Army support craft. Has the Stasis Field and Recall abilities. Cloaks nearby units.",
    item_names.ORACLE: "Flying caster. Can use the Revelation and Stasis Ward abilities.",
    item_names.SKYLORD: "Capital ship. Fires a powerful laser that deals damage in a line. Can use Tactical Jump ability.",
    item_names.PURGER: "Capital ship. Builds and launches Interceptors that attack enemy targets. Has Solar Beam weapon.",
    item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "ground units"),
    item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "ground units"),
    item_names.PROGRESSIVE_PROTOSS_SHIELDS: GENERIC_UPGRADE_TEMPLATE.format("shields", PROTOSS, "units"),
    item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "starships"),
    item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "starships"),
    item_names.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "units"),
    item_names.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "units"),
    item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "ground units"),
    item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "starships"),
    item_names.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "units"),
    item_names.PHOTON_CANNON: "Protoss defensive structure. Can attack ground and air units.",
    item_names.KHAYDARIN_MONOLITH: "Advanced Protoss defensive structure. Has superior range and damage, but is very expensive and attacks slowly.",
    item_names.SHIELD_BATTERY: "Protoss defensive structure. Restores shields to nearby friendly units and structures.",
    item_names.SUPPLICANT_BLOOD_SHIELD: "Increases the armor value of Supplicant shields.",
    item_names.SUPPLICANT_SOUL_AUGMENTATION: "Increases Supplicant max shields by +25.",
    item_names.SUPPLICANT_SHIELD_REGENERATION: "Increases Supplicant shield regeneration rate.",
    item_names.ADEPT_SHOCKWAVE: "When Adepts deal a finishing blow, their projectiles can jump onto 2 additional targets.",
    item_names.ADEPT_RESONATING_GLAIVES: "Increases Adept attack speed.",
    item_names.ADEPT_PHASE_BULWARK: "Increases Adept shield maximum by +50.",
    item_names.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES: "Increases weapon damage of Stalkers, Instigators, and Slayers.",
    item_names.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION: "Attacks fired by Stalkers, Instigators, and Slayers have a chance to bounce to additional targets for reduced damage.",
    item_names.DRAGOON_HIGH_IMPACT_PHASE_DISRUPTORS: "Dragoons deal increased damage.",
    item_names.DRAGOON_TRILLIC_COMPRESSION_SYSTEM: "Dragoons gain +20 life and their shield regeneration rate is doubled. Allows Dragoons to regenerate shields in combat.",
    item_names.DRAGOON_SINGULARITY_CHARGE: "Increases Dragoon range by +2.",
    item_names.DRAGOON_ENHANCED_STRIDER_SERVOS: "Increases Dragoon movement speed.",
    item_names.SCOUT_COMBAT_SENSOR_ARRAY: "Scouts gain +3 range against air and +1 range against ground.",
    item_names.SCOUT_APIAL_SENSORS: "Scouts gain increased sight range.",
    item_names.SCOUT_GRAVITIC_THRUSTERS: "Scouts gain increased movement speed.",
    item_names.SCOUT_ADVANCED_PHOTON_BLASTERS: "Scouts gain increased damage against ground targets.",
    item_names.SCOUT_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.SCOUT),
    item_names.TEMPEST_TECTONIC_DESTABILIZERS: "Tempests deal increased damage to buildings.",
    item_names.TEMPEST_QUANTIC_REACTOR: "Tempests deal increased damage to massive units.",
    item_names.TEMPEST_GRAVITY_SLING: "Tempests gain +8 range against air targets.",
    item_names.PHOENIX_CLASS_IONIC_WAVELENGTH_FLUX: "Increases Phoenix, Mirage, and Skirmisher weapon damage by +2.",
    item_names.PHOENIX_CLASS_ANION_PULSE_CRYSTALS: "Increases Phoenix, Mirage, and Skirmiser range by +2.",
    item_names.CORSAIR_STEALTH_DRIVE: "Corsairs become permanently cloaked.",
    item_names.CORSAIR_ARGUS_JEWEL: "Corsairs can store 2 charges of disruption web.",
    item_names.CORSAIR_SUSTAINING_DISRUPTION: "Corsair disruption webs last longer.",
    item_names.CORSAIR_NEUTRON_SHIELDS: "Increases corsair maximum shields by +20.",
    item_names.ORACLE_STEALTH_DRIVE: "Oracles become permanently cloaked.",
    item_names.ORACLE_STASIS_CALIBRATION: "Enemies caught by the Oracle's Stasis Ward may now be attacked.",
    item_names.ORACLE_TEMPORAL_ACCELERATION_BEAM: "Oracles no longer need to to spend energy to attack.",
    item_names.ORACLE_BOSONIC_CORE: "Increases starting energy by 150 and maximum energy by 50.",
    item_names.ARBITER_CHRONOSTATIC_REINFORCEMENT: "Arbiters gain +50 maximum life and +1 armor.",
    item_names.ARBITER_KHAYDARIN_CORE: _get_start_and_max_energy_desc("Arbiters"),
    item_names.ARBITER_SPACETIME_ANCHOR: "Arbiter Stasis Field lasts 50 seconds longer.",
    item_names.ARBITER_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.ARBITER),
    item_names.ARBITER_ENHANCED_CLOAK_FIELD: "Increases Arbiter Cloaking Field range.",
    item_names.CARRIER_SKYLORD_PURGER_GRAVITON_CATAPULT: "Carriers can launch Interceptors more quickly.",
    item_names.CARRIER_SKYLORD_PURGER_HULL_OF_PAST_GLORIES: "Carriers gain +2 armour.",
    item_names.VOID_RAY_DESTROYER_WARP_RAY_DAWNBRINGER_FLUX_VANES: "Increases movement speed of Void Ray variants.",
    item_names.DESTROYER_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.DESTROYER),
    item_names.WARP_PRISM_GRAVITIC_DRIVE: "Increases the movement speed of Warp Prisms.",
    item_names.WARP_PRISM_PHASE_BLASTER: "Equips Warp Prisms with an auto-attack that can hit ground and air targets.",
    item_names.WARP_PRISM_WAR_CONFIGURATION: "Warp Prisms transform faster and gain increased power radius in Phasing Mode.",
    item_names.OBSERVER_GRAVITIC_BOOSTERS: "Increases Observer movement speed.",
    item_names.OBSERVER_SENSOR_ARRAY: "Increases Observer sight range.",
    item_names.REAVER_SCARAB_DAMAGE: "Reaver Scarabs deal +25 damage.",
    item_names.REAVER_SOLARITE_PAYLOAD: "Reaver Scarabs gain increased splash damage radius.",
    item_names.REAVER_REAVER_CAPACITY: "Reavers can store 10 Scarabs.",
    item_names.REAVER_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(item_names.REAVER),
    item_names.VANGUARD_AGONY_LAUNCHERS: "Increases Vanguard attack range by +2.",
    item_names.VANGUARD_MATTER_DISPERSION: "Increases Vanguard attack area.",
    item_names.IMMORTAL_ANNIHILATOR_STALWART_SINGULARITY_CHARGE: "Increases Immortal, Annihilator, and Stalwart attack range by +2.",
    item_names.IMMORTAL_ANNIHILATOR_STALWART_ADVANCED_TARGETING_MECHANICS: "Immortals, Annihilators, and Stalwarts can attack air units.",
    item_names.IMMORTAL_ANNIHILATOR_STALWART_DISRUPTOR_DISPERSION: "Immortals, Annihilators, and Stalwarts deal minor splash damage.",
    item_names.COLOSSUS_PACIFICATION_PROTOCOL: "Increases Colossus attack speed.",
    item_names.WRATHWALKER_RAPID_POWER_CYCLING: "Reduces the charging time and increases attack speed of the Wrathwalker's Charged Blast.",
    item_names.WRATHWALKER_EYE_OF_WRATH: "Increases Wrathwalker weapon range by +1.",
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHROUD_OF_ADUN: f"Increases {DISPLAY_NAME_CLOAKED_ASSASSIN} maximum shields by +80.",
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHADOW_GUARD_TRAINING: f"Increases {DISPLAY_NAME_CLOAKED_ASSASSIN} maximum life by +40.",
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK: _ability_desc("Dark Templar, Avengers, and Blood Hunters", "Blink"),
    item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_RESOURCE_EFFICIENCY: _get_resource_efficiency_desc(DISPLAY_NAME_CLOAKED_ASSASSIN),
    item_names.DARK_TEMPLAR_DARK_ARCHON_MELD: "Allows 2 Dark Templar to meld into a Dark Archon.",
    item_names.HIGH_TEMPLAR_SIGNIFIER_UNSHACKLED_PSIONIC_STORM: "High Templar and Signifiers deal increased damage with Psi Storm.",
    item_names.HIGH_TEMPLAR_SIGNIFIER_HALLUCINATION: _ability_desc("High Templar and Signifiers", "Hallucination", "creates 2 hallucinated copies of a target unit"),
    item_names.HIGH_TEMPLAR_SIGNIFIER_KHAYDARIN_AMULET: _get_start_and_max_energy_desc("High Templar and Signifiers"),
    item_names.ARCHON_HIGH_ARCHON: "Archons can use High Templar abilities.",
    item_names.DARK_ARCHON_FEEDBACK: _ability_desc("Dark Archons", "Feedback", "drains all energy from a target and deals 1 damage per point of energy drained"),
    item_names.DARK_ARCHON_MAELSTROM: _ability_desc("Dark Archons", "Maelstrom", "stuns biological units in an area"),
    item_names.DARK_ARCHON_ARGUS_TALISMAN: _get_start_and_max_energy_desc("Dark Archons"),
    item_names.ASCENDANT_POWER_OVERWHELMING: "Ascendants gain the ability to sacrifice Supplicants for increased shields and spell damage.",
    item_names.ASCENDANT_CHAOTIC_ATTUNEMENT: "Ascendants' Psionic Orbs gain 25% increased travel distance.",
    item_names.ASCENDANT_BLOOD_AMULET: _get_start_and_max_energy_desc("Ascendants"),
    item_names.SENTRY_ENERGIZER_HAVOC_CLOAKING_MODULE: "Sentries, Energizers, and Havocs become permanently cloaked.",
    item_names.SENTRY_ENERGIZER_HAVOC_SHIELD_BATTERY_RAPID_RECHARGING: "Sentries, Energizers, and Havocs gain +100% energy regeneration rate.",
    item_names.SENTRY_FORCE_FIELD: _ability_desc("Sentries", "Force Field"),
    item_names.SENTRY_HALLUCINATION: _ability_desc("Sentries", "Hallucination", "creates hallucinated versions of Protoss units"),
    item_names.ENERGIZER_RECLAMATION: _ability_desc("Energizers", "Reclamation"),
    item_names.ENERGIZER_FORGED_CHASSIS: "Increases Energizer Life by +20.",
    item_names.HAVOC_DETECT_WEAKNESS: "Havocs' Target Lock gives an additional +15% damage bonus.",
    item_names.HAVOC_BLOODSHARD_RESONANCE: "Havoc gain increased range for Squad Sight, Target Lock, and Force Field.",
    item_names.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS: "Zealots, Sentinels, and Centurions gain increased movement speed.",
    item_names.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY: "Zealots, Sentinels, and Centurions gain +30 maximum shields.",
    item_names.ZEALOT_WHIRLWIND: "Zealot War Council upgrade. Gives Zealots the whirlwind ability, dealing damage in an area over 3 seconds.",
    item_names.CENTURION_RESOURCE_EFFICIENCY: "Centurion War Council upgrade. " + _get_resource_efficiency_desc(item_names.CENTURION),
    item_names.SENTINEL_RESOURCE_EFFICIENCY: "Sentinel War Council upgrade. " + _get_resource_efficiency_desc(item_names.SENTINEL),
    item_names.STALKER_PHASE_REACTOR: "Stalker War Council upgrade. Stalkers restore 80 shields over 5 seconds after they Blink.",
    item_names.DRAGOON_PHALANX_SUIT: "Dragoon War Council upgrade. Dragoons gain +1 range, move slightly faster, and can form tighter formations.",
    item_names.INSTIGATOR_RESOURCE_EFFICIENCY: f"Instigator War Council upgrade. {_get_resource_efficiency_desc(item_names.INSTIGATOR)}",
    item_names.ADEPT_DISRUPTIVE_TRANSFER: "Adept War Council upgrade. Adept shades apply a debuff to enemies they touch, increasing damage taken by +5.",
    item_names.SLAYER_PHASE_BLINK: "Slayer War Council upgrade. Slayers can now blink. After blinking, the Slayer's next attack within 8 seconds deals double damage.",
    item_names.AVENGER_KRYHAS_CLOAK: "Avenger War Council upgrade. Avengers are now permanently cloaked.",
    item_names.DARK_TEMPLAR_LESSER_SHADOW_FURY: "Dark Templar War Council upgrade. Dark Templar gain two strikes of their Shadow Fury ability.",
    item_names.DARK_TEMPLAR_GREATER_SHADOW_FURY: "Dark Templar War Council upgrade. Dark Templar gain three strikes of their Shadow Fury ability.",
    item_names.BLOOD_HUNTER_BRUTAL_EFFICIENCY: "Blood Hunter War Council upgrade. Blood Hunters attack over twice as quickly.",
    item_names.SENTRY_DOUBLE_SHIELD_RECHARGE: "Sentry War Council upgrade. Sentries can heal the shields of two targets at once.",
    item_names.ENERGIZER_MOBILE_CHRONO_BEAM: "Energizer War Council upgrade. Allows Energizers to use Chrono Beam in Mobile Mode.",
    item_names.HAVOC_ENDURING_SIGHT: "Havoc War Council upgrade. Havoc Squad Sight stays up indefinitely and no longer takes energy.",
    item_names.HIGH_TEMPLAR_PLASMA_SURGE: "High Templar War Council upgrade. High Templar Psionic Storm will heal fiendly protoss shields under it.",
    # Signifier
    # Ascendant
    item_names.DARK_ARCHON_INDOMITABLE_WILL: "Dark Archon War Council upgrade. Casting Mind Control will no longer deplete the Dark Archon's shields.",
    # Immortal
    # Annihilator
    item_names.VANGUARD_RAPIDFIRE_CANNON: "Vanguard War Council upgrade. Vanguards attack 38% faster.",
    item_names.VANGUARD_FUSION_MORTARS: "Vanguard War Council upgrade. Vanguards deal +7 damage to armored targets per attack.",
    # Stalwart
    # Colossus
    # Wrathwalker
    # Reaver
    # Disruptor
    # Warp Prism
    # Observer
    # Phoenix
    # Corsair
    # Mirage
    item_names.SKIRMISHER_PEER_CONTEMPT: "Skirmisher War Council upgrade. Allows Skirmishers to target air units.",
    # Void Ray
    item_names.DESTROYER_REFORGED_BLOODSHARD_CORE: "Destroyer War Council upgrade. When fully charged, the Destroyer's Destruction Beam weapon does full damage to secondary targets.",
    # Warp Ray
    # Dawnbringer
    item_names.SOA_CHRONO_SURGE: "The Spear of Adun increases a target structure's unit warp in and research speeds by +1000% for 20 seconds.",
    item_names.SOA_PROGRESSIVE_PROXY_PYLON: inspect.cleandoc("""
        Level 1: The Spear of Adun quickly warps in a Pylon to a target location.
        Level 2: The Spear of Adun warps in a Pylon, 2 melee warriors, and 2 ranged warriors to a target location.
    """),
    item_names.SOA_PYLON_OVERCHARGE: "The Spear of Adun temporarily gives a target Pylon increased shields and a powerful attack.",
    item_names.SOA_ORBITAL_STRIKE: "The Spear of Adun fires 5 laser blasts from orbit.",
    item_names.SOA_TEMPORAL_FIELD: "The Spear of Adun creates 3 temporal fields that freeze enemy units and structures in time.",
    item_names.SOA_SOLAR_LANCE: "The Spear of Adun strafes a target area with 3 laser beams.",
    item_names.SOA_MASS_RECALL: "The Spear of Adun warps all units in a target area back to the primary Nexus and gives them a temporary shield.",
    item_names.SOA_SHIELD_OVERCHARGE: "The Spear of Adun gives all friendly units a shield that absorbs 200 damage. Lasts 20 seconds.",
    item_names.SOA_DEPLOY_FENIX: "The Spear of Adun drops Fenix onto the battlefield. Fenix is a powerful warrior who will fight for 30 seconds.",
    item_names.SOA_PURIFIER_BEAM: "The Spear of Adun fires a wide laser that deals large amounts of damage in a moveable area. Lasts 15 seconds.",
    item_names.SOA_TIME_STOP: "The Spear of Adun freezes all enemy units and structures in time for 20 seconds.",
    item_names.SOA_SOLAR_BOMBARDMENT: "The Spear of Adun fires 200 laser blasts randomly over a wide area.",
    item_names.MATRIX_OVERLOAD: "All friendly units gain 25% movement speed and 15% attack speed within a Pylon's power field and for 15 seconds after leaving it.",
    item_names.QUATRO: "All friendly Protoss units gain the equivalent of their +1 armour, attack, and shield upgrades.",
    item_names.NEXUS_OVERCHARGE: "The Protoss Nexus gains a long-range auto-attack.",
    item_names.ORBITAL_ASSIMILATORS: "Assimilators automatically harvest Vespene Gas without the need for Probes.",
    item_names.WARP_HARMONIZATION: "Stargates and Robotics Facilities can transform to utilize Warp In technology. Warp In cooldowns are 20% faster than original build times.",
    item_names.GUARDIAN_SHELL: "The Spear of Adun passively shields friendly Protoss units before death, making them invulnerable for 5 seconds. Each unit can only be shielded once every 60 seconds.",
    item_names.RECONSTRUCTION_BEAM: "The Spear of Adun will passively heal mechanical units for 5 and non-biological structures for 10 life per second. Up to 3 targets can be repaired at once.",
    item_names.OVERWATCH: "Once per second, the Spear of Adun will last-hit a damaged enemy unit that is below 50 health.",
    item_names.SUPERIOR_WARP_GATES: "Protoss Warp Gates can hold up to 3 charges of unit warp-ins.",
    item_names.ENHANCED_TARGETING: "Protoss defensive structures gain +2 range.",
    item_names.OPTIMIZED_ORDNANCE: "Increases the attack speed of Protoss defensive structures by 25%.",
    item_names.KHALAI_INGENUITY: "Pylons, Photon Cannons, Monoliths, and Shield Batteries warp in near-instantly.",
    item_names.AMPLIFIED_ASSIMILATORS: "Assimilators produce Vespene gas 25% faster.",
}
