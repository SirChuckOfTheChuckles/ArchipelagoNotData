"""
Unit tests for option parsing and validation for custom_mission_order
"""
import unittest

from Options import OptionError

from .. import MissionFlag
from ..item import item_tables, item_names
from BaseClasses import ItemClassification
from .. import options
from ..mission_tables import SC2Mission
from ..tables import HeroFlag
from ..mission_order import options as cmo_options


class CmoOptionTests(unittest.TestCase):
    def test_cmo_option_parse_fails_on_nothing_in_campaign(self) -> None:
        yaml_option = {
            "My Campaign": "",
        }
        try:
            cmo_options.CustomMissionOrder.from_any(yaml_option)
            self.fail("Expected option parse to fail")
        except OptionError as ex:
            self.assertIn("must", str(ex))
            self.assertIn("dictionary", str(ex))

    def test_cmo_option_parse_fails_on_invalid_global_layout_keys(self) -> None:
        yaml_option = {
            "My Campaign": {
                "global": {"<invalid key :P>": 1},
            }
        }
        try:
            cmo_options.CustomMissionOrder.from_any(yaml_option)
            self.fail("Expected option parse to fail")
        except OptionError as ex:
            self.assertIn("<invalid key :P>", str(ex))

    def test_cmo_option_parse_fails_on_nothing_in_layout(self) -> None:
        yaml_option = {
            "My Campaign": {
                "My Layout": "",
            },
        }
        try:
            cmo_options.CustomMissionOrder.from_any(yaml_option)
            self.fail("Expected option parse to fail")
        except OptionError as ex:
            self.assertIn("must", str(ex))
            self.assertIn("dictionar", str(ex))

    def test_cmo_option_parse_fails_on_invalid_preset(self) -> None:
        yaml_option = {
            "My Campaign": {
                "preset": "invalid preset",
                "My Layout": {},
            },
        }
        try:
            cmo_options.CustomMissionOrder.from_any(yaml_option)
            self.fail("Expected option parse to fail")
        except OptionError as ex:
            self.assertIn("preset", str(ex))
            self.assertIn("golden path", str(ex).lower())

    def test_cmo_option_parse_fails_on_invalid_campaign_key(self) -> None:
        yaml_option = {
            "My Campaign": {
                "invalid campaign key": False,
                "My Layout": {},
            },
        }
        try:
            cmo_options.CustomMissionOrder.from_any(yaml_option)
            self.fail("Expected option parse to fail")
        except OptionError as ex:
            self.assertIn("invalid campaign key", str(ex))

    def test_cmo_option_parse_happy_path(self) -> None:
        yaml_option = {
            "My Campaign": {
                "My Layout": {
                    "type": "grid",
                    "size": 9,
                },
            },
        }
        parsed_option = cmo_options.CustomMissionOrder.from_any(yaml_option)
        self.assertIn("My Layout", parsed_option.value["My Campaign"]["layouts"])

    def test_cmo_canvas_parse(self) -> None:
        yaml_option = {
            "My Campaign": {
                "My Layout": {
                    "type": "canvas",
                    "canvas": [
                        "sxxxx",
                        "xxxxx",
                        "xx xx",
                        "xxxxx",
                        "xxxxg",
                    ],
                    "jump_distance_orthogonal": 2,
                },
            },
        }
        parsed_option = cmo_options.CustomMissionOrder.from_any(yaml_option)
        self.assertIn("My Layout", parsed_option.value["My Campaign"]["layouts"])
        self.assertEqual(parsed_option.value["My Campaign"]["layouts"]["My Layout"]["size"], 25)
        self.assertEqual(parsed_option.value["My Campaign"]["layouts"]["My Layout"]["width"], 5)

