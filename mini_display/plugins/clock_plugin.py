#!/usr/bin/env python3
"""
Clock Plugin - displays time and date in compact format.
"""

import dataclasses
from datetime import datetime
from typing import Optional, Tuple

from PIL import Image, ImageDraw

from mini_display.plugin_base import Plugin
from mini_display.utils import draw_small_text, measure_small_text, center_x

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


@dataclasses.dataclass
class ClockPlugin(Plugin):
    """Display current time and date with configurable timezone."""
    
    name: str = "clock"
    tz: Optional[str] = None
    fg_time: Tuple[int, int, int] = (0, 255, 0)
    fg_date: Tuple[int, int, int] = (128, 128, 128)
    bg: Tuple[int, int, int] = (0, 0, 0)

    def _now(self) -> datetime:
        """Get current time in configured timezone."""
        if self.tz and ZoneInfo:
            try:
                return datetime.now(ZoneInfo(self.tz))
            except Exception:
                pass
        return datetime.now()

    def render(self, width: int, height: int) -> Image.Image:
        """Render time and date centered on display."""
        img = Image.new("RGB", (width, height), self.bg)
        d = ImageDraw.Draw(img)
        now = self._now()

        # Format time: "h:MMa" (e.g., "9:45a" or "11:30p")
        tm = now.strftime("%I:%M%p")
        if tm.startswith("0"):
            tm = tm[1:]
        tm = tm[:-2] + tm[-2:].lower()[0]  # AM->a, PM->p

        # Format date: "MM/DD/YY"
        date = now.strftime("%m/%d/%y")

        # Draw time at top
        w1, h1 = measure_small_text(tm, scale=1, spacing=1)
        x1 = center_x(width, w1)
        y1 = 1
        draw_small_text(d, x1, y1, tm, self.fg_time, scale=1, spacing=1)

        # Draw date at bottom
        w2, h2 = measure_small_text(date, scale=1, spacing=1)
        x2 = center_x(width, w2)
        y2 = height - h2 - 1
        draw_small_text(d, x2, y2, date, self.fg_date, scale=1, spacing=1)

        return img