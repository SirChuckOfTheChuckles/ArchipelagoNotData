import asyncio
import unittest
from contextlib import suppress
from unittest.mock import patch
from uuid import UUID

from BaseClasses import MultiWorld
from test.general import setup_multiworld

from .. import SC2World, get_sc2_world_id
from ..client import SC2Context
from ..options import MissionOrderScouting


class TestWorldIdentity(unittest.TestCase):
    def test_slot_data_shares_stable_world_id(self) -> None:
        multiworld = setup_multiworld(
            [SC2World, SC2World], seed=0,
            options={"mission_order_scouting": MissionOrderScouting.option_none},
        )
        first = multiworld.worlds[1].fill_slot_data()
        second = multiworld.worlds[2].fill_slot_data()

        self.assertEqual(UUID(first["world_id"]).version, 4)
        self.assertEqual(first["world_id"], second["world_id"])
        self.assertEqual(first, multiworld.worlds[1].fill_slot_data())
        self.assertEqual(first["version"], 5)
        self.assertTrue(first["custom_mission_order"])

    def test_separate_generations_have_distinct_world_ids(self) -> None:
        first = MultiWorld(1)
        second = MultiWorld(1)
        first.set_seed(0)
        second.set_seed(0)

        self.assertNotEqual(get_sc2_world_id(first), get_sc2_world_id(second))


class TestClientWorldIdentity(unittest.IsolatedAsyncioTestCase):
    async def test_connected_reads_world_id_and_clears_it_for_legacy_slot_data(self) -> None:
        context = SC2Context()
        slot_data = {
            "version": 5,
            "game_difficulty": 1,
            "all_in_map": 0,
            "custom_mission_order": [],
            "hero_presence": {},
            "world_id": "test-world-id",
        }
        try:
            with (
                patch.object(context, "_apply_host_settings_to_options"),
                patch.object(context, "on_print_json"),
                patch("worlds.sc2.client.is_mod_installed_correctly", return_value=False),
                patch("worlds.sc2.client.os.path.exists", return_value=False),
            ):
                context.on_package("Connected", {"slot_data": slot_data})
                self.assertEqual(context.world_id, "test-world-id")

                del slot_data["world_id"]
                context.on_package("Connected", {"slot_data": slot_data})
                self.assertEqual(context.world_id, "")
        finally:
            context.keep_alive_task.cancel()
            with suppress(asyncio.CancelledError):
                await context.keep_alive_task
