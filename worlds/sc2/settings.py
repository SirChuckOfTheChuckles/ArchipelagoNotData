from typing import Union
import settings


class Starcraft2Settings(settings.Group):
    class WindowWidth(int):
        """The starting width the client window in pixels"""
    class WindowHeight(int):
        """The starting height the client window in pixels"""
    class StartMaximized(settings.Bool):
        """Controls whether the client window should start maximized"""
    class GameWindowedMode(settings.Bool):
        """Controls whether the game should start in windowed mode"""

    window_width = WindowWidth(1080)
    window_height = WindowHeight(720)
    window_maximized: Union[StartMaximized, bool] = False
    game_windowed_mode: Union[GameWindowedMode, bool] = False
