from typing import Union
import settings


class Starcraft2Settings(settings.Group):
    class Sc2InstallPath(str):
        """The path to your sc2 install folder; normally in C:/Program Files (x86)/StarCraft II"""
    
    class Sc2DocumentsPath(str):
        """The path to your sc2 documents folder; normally ~/Documents/StarCraft II"""
    
    class WinePath(str):
        """Non-Windows. The path to your preferred wine executable; defaults to WINE environment variable if not set"""

    class WinePrefix(str):
        """Non-Windows. The path to your preferred wine executable; defaults to WINEPREFIX environment variable if not set"""

    class WindowWidth(int):
        """The starting width the client window in pixels"""

    class WindowHeight(int):
        """The starting height the client window in pixels"""

    class GameWindowedMode(settings.Bool):
        """Controls whether the game should start in windowed mode"""

    class TerranButtonColor(list):
        """Defines the colour of terran mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""

    class ZergButtonColor(list):
        """Defines the colour of zerg mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""

    class ProtossButtonColor(list):
        """Defines the colour of protoss mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""

    class DisableForcedCamera(str):
        """Overrides the disable forced-camera slot option. Possible values: `true`, `false`, `default`. Default uses slot value"""

    class SkipCutscenes(str):
        """Overrides the skip cutscenes slot option. Possible values: `true`, `false`, `default`. Default uses slot value"""

    class GameDifficulty(str):
        """Overrides the slot's difficulty setting. Possible values: `casual`, `normal`, `hard`, `brutal`, `default`. Default uses slot value"""

    class GameSpeed(str):
        """Overrides the slot's gamespeed setting. Possible values: `slower`, `slow`, `normal`, `fast`, `faster`, `default`. Default uses slot value"""

    class ShowTraps(settings.Bool):
        """If set to true, in-client scouting will show traps as distinct from filler"""

    # Client options
    sc2_install_path: Sc2InstallPath = Sc2InstallPath("")
    sc2_documents_path: Sc2InstallPath = Sc2DocumentsPath("")
    wine_path: WinePath = WinePath("")
    wine_prefix: WinePrefix = WinePrefix("")
    window_width: WindowWidth = WindowWidth(1080)
    window_height: WindowHeight = WindowHeight(720)
    game_windowed_mode: Union[GameWindowedMode, bool] = False
    show_traps: Union[ShowTraps, bool] = False

    terran_button_color: TerranButtonColor = TerranButtonColor([0.0838, 0.2898, 0.2346])
    zerg_button_color: ZergButtonColor = ZergButtonColor([0.345, 0.22425, 0.12765])
    protoss_button_color: ProtossButtonColor = ProtossButtonColor([0.18975, 0.2415, 0.345])

    # Options overrides
    disable_forced_camera: DisableForcedCamera = DisableForcedCamera("default")
    skip_cutscenes: SkipCutscenes = SkipCutscenes("default")
    game_difficulty: GameDifficulty = GameDifficulty("default")
    game_speed: GameSpeed = GameSpeed("default")
