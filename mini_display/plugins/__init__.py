#!/usr/bin/env python3
"""
Mini Display Plugins Package

This package contains individual plugin implementations for the mini display.
Each plugin is in its own file following the adapter pattern.
"""

from mini_display.plugins.clock_plugin import ClockPlugin
from mini_display.plugins.weather_plugin import WeatherPlugin
from mini_display.plugins.subway_plugin import SubwayPlugin

__all__ = [
    "ClockPlugin",
    "WeatherPlugin",
    "SubwayPlugin",
]