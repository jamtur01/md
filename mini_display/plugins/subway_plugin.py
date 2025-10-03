#!/usr/bin/env python3
"""
Subway Plugin - displays NYC MTA subway arrival times.
"""

import dataclasses
import time
from datetime import datetime as _dt
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

from mini_display.plugin_base import Plugin
from mini_display.utils import draw_text, measure_text, center_x

try:
    from nyct_gtfs import NYCTFeed
except Exception as e:
    print("Error: nyct-gtfs missing. Install with 'pip install nyct-gtfs protobuf'.")
    raise


# MTA official line colors
MTA_COLORS: Dict[str, Tuple[int, int, int]] = {
    "A": (0, 57, 166),
    "C": (0, 57, 166),
    "E": (0, 57, 166),
    "B": (255, 99, 25),
    "D": (255, 99, 25),
    "F": (255, 99, 25),
    "M": (255, 99, 25),
    "N": (252, 204, 10),
    "Q": (252, 204, 10),
    "R": (252, 204, 10),
    "W": (252, 204, 10),
    "1": (238, 53, 46),
    "2": (238, 53, 46),
    "3": (238, 53, 46),
    "4": (0, 147, 60),
    "5": (0, 147, 60),
    "6": (0, 147, 60),
    "7": (185, 51, 173),
    "L": (145, 145, 142),
    "G": (108, 190, 69),
    "J": (153, 102, 51),
    "Z": (153, 102, 51),
    "S": (128, 128, 128),
}


@dataclasses.dataclass
class SubwayPlugin(Plugin):
    """Display next MTA subway arrivals for configured stations and routes."""
    
    name: str = "subway"
    stations: List[str] = dataclasses.field(default_factory=lambda: ["Jay St-MetroTech"])
    route_groups: List[str] = dataclasses.field(default_factory=lambda: ["A", "C", "F", "R"])
    bg: Tuple[int, int, int] = (0, 0, 0)
    text_fg_default: Tuple[int, int, int] = (255, 255, 255)
    max_lines: int = 2
    _cache_ttl_sec: int = 20
    _last_fetch_ts: float = 0.0
    _lines: List[Tuple[str, Tuple[int, int, int]]] = dataclasses.field(default_factory=list)

    @staticmethod
    def _norm(s: str) -> str:
        """Normalize station name for comparison."""
        return "".join(ch for ch in s.lower() if ch.isalnum())

    def _want_station(self, stop_name: str) -> bool:
        """Check if stop matches any configured stations."""
        n = self._norm(stop_name)
        for st in self.stations:
            if self._norm(st) in n:
                return True
        return False

    def _fetch(self) -> None:
        """Fetch next arrivals from MTA GTFS feeds."""
        now = _dt.now()
        results: List[Tuple[_dt, str, Tuple[int, int, int]]] = []
        
        for route in self.route_groups:
            try:
                feed = NYCTFeed(route)
                trains = feed.filter_trips(line_id=route)
                for t in trains:
                    for stu in t.stop_time_updates:
                        nm = getattr(stu, "stop_name", None)
                        if not nm or not self._want_station(nm):
                            continue
                        arr = getattr(stu, "arrival", None) or getattr(stu, "departure", None)
                        if not isinstance(arr, _dt) or arr < now:
                            continue
                        mins = int((arr - now).total_seconds() // 60)
                        arrow = "↑" if t.direction == "N" else "↓"
                        label = f"{route} {mins}{arrow}"
                        color = MTA_COLORS.get(route.upper(), self.text_fg_default)
                        results.append((arr, label, color))
                        break
            except Exception:
                continue
        
        results.sort(key=lambda x: x[0])
        top = results[:max(1, self.max_lines)]
        if not top:
            self._lines = [("MTA N/A", self.text_fg_default)]
        else:
            self._lines = [(lab, col) for _, lab, col in top]

    def tick(self) -> None:
        """Update subway data if cache expired."""
        now = time.time()
        if now - self._last_fetch_ts > self._cache_ttl_sec:
            self._fetch()
            self._last_fetch_ts = now

    def render(self, width: int, height: int) -> Image.Image:
        """Render arrival times with MTA line colors."""
        img = Image.new("RGB", (width, height), self.bg)
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        lines = self._lines or [("MTA ...", self.text_fg_default)]

        y = 0
        used = 0
        for text, color in lines[:2]:
            w, h = measure_text(text, font)
            if used + h > height:
                break
            x = center_x(width, w)
            draw_text(d, x, y, text, color, font)
            y += h
            if y + 1 < height:
                y += 1
            used = y
        return img