"""Mini Display - LED Matrix Display with Widgets."""

__version__ = "0.1.0"

from mini_display.display import main
from mini_display.plugin_base import Plugin
from mini_display.plugin_adapter import PluginAdapter
from mini_display.plugins import ClockPlugin, WeatherPlugin, SubwayPlugin

__all__ = [
    "Plugin",
    "PluginAdapter",
    "ClockPlugin",
    "WeatherPlugin",
    "SubwayPlugin",
    "main",
]