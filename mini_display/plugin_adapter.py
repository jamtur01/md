#!/usr/bin/env python3
"""
Plugin Adapter - Factory and registry for display plugins.

This module implements the Adapter pattern to provide a unified interface
for creating and managing display plugins.
"""

from typing import Dict, List, Type, Optional

from mini_display.plugin_base import Plugin
from mini_display.plugins import ClockPlugin, WeatherPlugin, SubwayPlugin
from mini_display.plugins.clock_plugin import TimezoneConfig


class PluginAdapter:
    """
    Adapter for managing plugin instances and providing factory methods.
    
    This class follows the Adapter pattern to decouple plugin creation
    from the main display logic.
    """
    
    # Plugin registry mapping plugin names to their classes
    _registry: Dict[str, Type[Plugin]] = {
        "clock": ClockPlugin,
        "weather": WeatherPlugin,
        "subway": SubwayPlugin,
    }
    
    @classmethod
    def register_plugin(cls, name: str, plugin_class: Type[Plugin]) -> None:
        """
        Register a new plugin type.
        
        Args:
            name: Unique identifier for the plugin
            plugin_class: Plugin class to register
        """
        cls._registry[name] = plugin_class
    
    @classmethod
    def get_available_plugins(cls) -> List[str]:
        """Get list of available plugin names."""
        return list(cls._registry.keys())
    
    @classmethod
    def create_plugin(cls, name: str, **kwargs) -> Optional[Plugin]:
        """
        Create a plugin instance by name.
        
        Args:
            name: Plugin name to create
            **kwargs: Arguments to pass to plugin constructor
            
        Returns:
            Plugin instance or None if plugin not found
        """
        plugin_class = cls._registry.get(name)
        if plugin_class is None:
            return None
        return plugin_class(**kwargs)
    
    @classmethod
    def create_default_plugins(
        cls,
        tz: Optional[str] = None,
        zip_code: str = "11201",
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        stations: Optional[List[str]] = None,
        route_groups: Optional[List[str]] = None,
    ) -> List[Plugin]:
        """
        Create the default set of plugins with standard configuration.
        
        Args:
            tz: Timezone for clock plugin
            zip_code: ZIP code for weather plugin
            lat: Latitude for weather (overrides zip_code)
            lon: Longitude for weather (overrides zip_code)
            stations: List of subway stations to monitor
            route_groups: List of subway routes to display
            
        Returns:
            List of configured plugin instances
        """
        plugins = []
        
        # Clock plugin - convert old tz parameter to new timezones format
        if tz:
            # If timezone is specified, use it for both cities
            clock = cls.create_plugin(
                "clock",
                timezones=[
                    TimezoneConfig(city="Local", timezone=tz),
                ]
            )
        else:
            # Use default timezones (Melbourne and New York)
            clock = cls.create_plugin("clock")
        if clock:
            plugins.append(clock)
        
        # Subway plugin
        subway = cls.create_plugin(
            "subway",
            stations=stations or ["Jay St-MetroTech"],
            route_groups=route_groups or ["A", "C", "F", "R"]
        )
        if subway:
            plugins.append(subway)
        
        # Weather plugin
        weather = cls.create_plugin(
            "weather",
            zip_code=zip_code,
            lat=lat,
            lon=lon
        )
        if weather:
            plugins.append(weather)
        
        return plugins