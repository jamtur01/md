#!/usr/bin/env python3
"""
Weather Plugin - displays temperature in Celsius from NWS forecast.
"""

import dataclasses
import time
from typing import Optional, Tuple

import requests
from PIL import Image, ImageDraw

from mini_display.plugin_base import Plugin
from mini_display.utils import draw_small_text, measure_small_text, center_x


@dataclasses.dataclass
class WeatherPlugin(Plugin):
    """Display current temperature from National Weather Service."""
    
    name: str = "weather"
    zip_code: str = "11201"
    lat: Optional[float] = None
    lon: Optional[float] = None
    fg_temp: Tuple[int, int, int] = (0, 200, 255)
    bg: Tuple[int, int, int] = (0, 0, 0)
    user_agent: str = "mini-display/1.0 (contact: you@example.com)"
    _last_fetch_ts: float = 0.0
    _cache_ttl_sec: int = 300
    _temp_c_text: str = "N/A"

    def _geocode_zip(self, z: str) -> Tuple[float, float]:
        """Convert ZIP code to lat/lon coordinates."""
        if self.lat is not None and self.lon is not None:
            return (self.lat, self.lon)
        try:
            r = requests.get(f"https://api.zippopotam.us/us/{z}", timeout=5)
            if r.ok:
                js = r.json()
                p = js["places"][0]
                return (float(p["latitude"]), float(p["longitude"]))
        except Exception:
            pass
        return (40.6944, -73.9918)  # Default: Brooklyn

    def _fetch(self) -> None:
        """Fetch current temperature from NWS API."""
        lat, lon = self._geocode_zip(self.zip_code)
        headers = {"User-Agent": self.user_agent, "Accept": "application/geo+json"}
        try:
            pt = requests.get(f"https://api.weather.gov/points/{lat},{lon}", headers=headers, timeout=6)
            pt.raise_for_status()
            fx_url = pt.json()["properties"]["forecast"]
            fx = requests.get(fx_url, headers=headers, timeout=6)
            fx.raise_for_status()
            first = fx.json()["properties"]["periods"][0]
            f = float(first["temperature"])
            if first["temperatureUnit"].upper() == "F":
                c = round((f - 32.0) * 5.0 / 9.0)
            else:
                c = int(round(f))
            self._temp_c_text = f"{c}°C"
        except Exception:
            self._temp_c_text = "N/A"

    def tick(self) -> None:
        """Update weather data if cache expired."""
        now = time.time()
        if now - self._last_fetch_ts > self._cache_ttl_sec:
            self._fetch()
            self._last_fetch_ts = now

    def render(self, width: int, height: int) -> Image.Image:
        """Render temperature centered on display."""
        img = Image.new("RGB", (width, height), self.bg)
        d = ImageDraw.Draw(img)
        w, h = measure_small_text(self._temp_c_text, scale=1, spacing=1)
        x = center_x(width, w)
        y = (height - h) // 2
        draw_small_text(d, x, y, self._temp_c_text, self.fg_temp, scale=1, spacing=1)
        return img