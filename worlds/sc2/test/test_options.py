import unittest
from typing import Dict

from .. import apply_hero_presence_override, calculate_hero_presence, calculate_mission_hero_presence
from .. import options
from ..item import item_parents
from ..mission_tables import SC2Mission
from ..tables import HeroFlag


class TestOptions(unittest.TestCase):

    def test_unit_max_upgrades_matching_items(self) -> None:
        upgrade_group_to_count: Dict[str, int] = {}
        for parent_id, child_list in item_parents.parent_id_to_children.items():
            main_parent = item_parents.parent_present[parent_id].constraint_group
            if main_parent is None:
                continue
            upgrade_group_to_count.setdefault(main_parent, 0)
            upgrade_group_to_count[main_parent] += len(child_list)

        self.assertEqual(options.MAX_UPGRADES_OPTION, max(upgrade_group_to_count.values()))

    def test_kerrigan_presence_override_replaces_preset_kerrigan(self) -> None:
        campaign_presence = calculate_hero_presence(
            options.HeroPresence.option_anywhere,
            {options.HeroOptions.KERRIGAN, options.HeroOptions.NOVA},
        )
        hero_presence = calculate_mission_hero_presence(campaign_presence, [
            SC2Mission.THE_OUTLAWS_P,
            SC2Mission.LIBERATION_DAY_P,
            SC2Mission.RENDEZVOUS_T,
            SC2Mission.RENDEZVOUS,
        ])

        apply_hero_presence_override(
            hero_presence,
            HeroFlag.KERRIGAN,
            {"Wings of Liberty Protoss", "Heart of the Swarm Terran"},
            True,
        )

        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.THE_OUTLAWS_P])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.LIBERATION_DAY_P])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS_T])
        self.assertNotIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS])
        self.assertIn(HeroFlag.NOVA, hero_presence[SC2Mission.RENDEZVOUS])

    def test_kerrigan_presence_override_empty_keeps_preset(self) -> None:
        campaign_presence = calculate_hero_presence(
            options.HeroPresence.option_vanilla,
            {options.HeroOptions.KERRIGAN},
        )
        hero_presence = calculate_mission_hero_presence(campaign_presence, [SC2Mission.RENDEZVOUS])

        apply_hero_presence_override(hero_presence, HeroFlag.KERRIGAN, set(), True)

        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS])

    def test_kerrigan_presence_override_can_target_build_missions(self) -> None:
        hero_presence = calculate_mission_hero_presence(
            calculate_hero_presence(options.HeroPresence.option_vanilla, {options.HeroOptions.KERRIGAN}),
            [SC2Mission.THE_OUTLAWS_P, SC2Mission.LIBERATION_DAY_P],
        )

        apply_hero_presence_override(
            hero_presence,
            HeroFlag.KERRIGAN,
            {"Wings of Liberty Protoss Build"},
            True,
        )

        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.THE_OUTLAWS_P])
        self.assertNotIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.LIBERATION_DAY_P])

    def test_kerrigan_presence_override_can_target_no_build_missions(self) -> None:
        hero_presence = calculate_mission_hero_presence(
            calculate_hero_presence(options.HeroPresence.option_vanilla, {options.HeroOptions.KERRIGAN}),
            [SC2Mission.THE_OUTLAWS_P, SC2Mission.LIBERATION_DAY_P],
        )

        apply_hero_presence_override(
            hero_presence,
            HeroFlag.KERRIGAN,
            {"Wings of Liberty Protoss No Build"},
            True,
        )

        self.assertNotIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.THE_OUTLAWS_P])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.LIBERATION_DAY_P])

    def test_kerrigan_presence_override_can_target_full_campaign(self) -> None:
        hero_presence = calculate_mission_hero_presence(
            calculate_hero_presence(options.HeroPresence.option_vanilla, {options.HeroOptions.KERRIGAN}),
            [SC2Mission.RENDEZVOUS_T, SC2Mission.RENDEZVOUS, SC2Mission.RENDEZVOUS_P],
        )

        apply_hero_presence_override(
            hero_presence,
            HeroFlag.KERRIGAN,
            {"Heart of the Swarm"},
            True,
        )

        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS_T])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS_P])

    def test_kerrigan_presence_override_can_target_campaign_build_type(self) -> None:
        hero_presence = calculate_mission_hero_presence(
            calculate_hero_presence(options.HeroPresence.option_vanilla, {options.HeroOptions.KERRIGAN}),
            [SC2Mission.RENDEZVOUS, SC2Mission.ENEMY_WITHIN, SC2Mission.ENEMY_WITHIN_T],
        )

        apply_hero_presence_override(
            hero_presence,
            HeroFlag.KERRIGAN,
            {"Heart of the Swarm No Build"},
            True,
        )

        self.assertNotIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.RENDEZVOUS])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.ENEMY_WITHIN])
        self.assertIn(HeroFlag.KERRIGAN, hero_presence[SC2Mission.ENEMY_WITHIN_T])
