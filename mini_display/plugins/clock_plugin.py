#!/usr/bin/env python3
"""
Clock Plugin - displays time and date for multiple timezones.
"""

import dataclasses
from datetime import datetime
from typing import List, Tuple

from PIL import Image, ImageDraw

from mini_display.plugin_base import Plugin
from mini_display.utils import draw_small_text, measure_small_text

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


@dataclasses.dataclass
class TimezoneConfig:
    """Configuration for a timezone display."""
    city: str
    timezone: str


@dataclasses.dataclass
class ClockPlugin(Plugin):
    """Display current time and date for multiple timezones."""
    
    name: str = "clock"
    timezones: List[TimezoneConfig] = None
    fg_city: Tuple[int, int, int] = (0, 255, 0)
    fg_datetime: Tuple[int, int, int] = (128, 128, 128)
    fg_separator: Tuple[int, int, int] = (64, 64, 64)
    bg: Tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self):
        """Initialize default timezones if none provided."""
        if self.timezones is None:
            self.timezones = [
                TimezoneConfig(city="Melbourne", timezone="Australia/Melbourne"),
                TimezoneConfig(city="New York", timezone="America/New_York"),
            ]

    def _get_time_for_tz(self, timezone: str) -> datetime:
        """Get current time in specified timezone."""
        if ZoneInfo:
            try:
                return datetime.now(ZoneInfo(timezone))
            except Exception:
                pass
        return datetime.now()

    def render(self, width: int, height: int) -> Image.Image:
        """Render multiple timezone displays with separators."""
        img = Image.new("RGB", (width, height), self.bg)
        d = ImageDraw.Draw(img)
        
        # Calculate line height for small text
        _, line_height = measure_small_text("A", scale=1, spacing=1)
        
        # Draw top separator line
        y = 0
        d.line([(0, y), (width - 1, y)], fill=self.fg_separator)
        y += 2
        
        # Draw each timezone
        for tz_config in self.timezones:
            now = self._get_time_for_tz(tz_config.timezone)
            
            # Format: "City  mm/dd/yy at hh:mm am/pm"
            date_str = now.strftime("%m/%d/%y")
            time_str = now.strftime("%I:%M %p").lstrip("0").lower()
            
            # Draw city name
            city_text = tz_config.city
            draw_small_text(d, 1, y, city_text, self.fg_city, scale=1, spacing=1)
            y += line_height + 1
            
            # Draw datetime on next line, slightly indented
            datetime_text = f"{date_str} at {time_str}"
            draw_small_text(d, 2, y, datetime_text, self.fg_datetime, scale=1, spacing=1)
            y += line_height + 2
        
        # Draw bottom separator line
        d.line([(0, height - 1), (width - 1, height - 1)], fill=self.fg_separator)
        
        return img