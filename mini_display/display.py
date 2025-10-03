#!/usr/bin/env python3
"""
Mini Display (16x32) with tiny pixel font and colored widgets.

Main application logic for cycling through plugins on an LED matrix display.
"""

import argparse
import signal
import sys
import threading
import time
from typing import List

from PIL import Image, ImageDraw, ImageFont

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except Exception as e:
    print("Error: rpi-rgb-led-matrix not available. Build and install the HZeller bindings.", file=sys.stderr)
    raise

from mini_display.plugin_base import Plugin
from mini_display.plugin_adapter import PluginAdapter
from mini_display.utils import draw_text, clamp


def build_matrix_from_args(args) -> RGBMatrix:
    """Build RGB matrix from command line arguments."""
    options = RGBMatrixOptions()
    options.rows = args.rows
    options.cols = args.cols
    options.chain_length = args.chain_length
    options.parallel = args.parallel
    options.hardware_mapping = args.hardware_mapping
    options.gpio_slowdown = args.gpio_slowdown
    options.pwm_bits = args.pwm_bits
    options.brightness = clamp(args.brightness, 1, 100)
    return RGBMatrix(options=options)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    p = argparse.ArgumentParser(description="Mini display with tiny font cycling widgets.")
    p.add_argument("--rows", type=int, default=32, help="Display height in pixels (default: 32)")
    p.add_argument("--cols", type=int, default=64, help="Display width in pixels (default: 64)")
    p.add_argument("--chain-length", type=int, default=1, help="Number of chained panels (default: 1)")
    p.add_argument("--parallel", type=int, default=1, help="Parallel chains (default: 1)")
    p.add_argument("--hardware-mapping", type=str, default="adafruit-hat", help="Hardware mapping (default: adafruit-hat)")
    p.add_argument("--gpio-slowdown", type=int, default=2, help="GPIO slowdown (default: 2)")
    p.add_argument("--pwm-bits", type=int, default=11, help="PWM bits (default: 11)")
    p.add_argument("--brightness", type=int, default=70, help="Brightness 1-100 (default: 70)")
    p.add_argument("--cycle-seconds", type=int, default=6, help="Seconds per widget (default: 6)")
    p.add_argument("--station", action="append", help="Station name filter. Repeat for multiple. Default Jay St-MetroTech.")
    p.add_argument("--routes", type=str, default="A,C,F,R", help="Comma-separated route letters to consider.")
    p.add_argument("--zip", type=str, default="11201")
    p.add_argument("--lat", type=float, default=None)
    p.add_argument("--lon", type=float, default=None)
    return p.parse_args()


def main():
    """Main application entry point."""
    args = parse_args()

    stations = args.station if args.station else None
    route_groups = [r.strip().upper() for r in args.routes.split(",") if r.strip()]

    # Use the plugin adapter to create default plugins
    plugins: List[Plugin] = PluginAdapter.create_default_plugins(
        tz=None,
        zip_code=args.zip,
        lat=args.lat,
        lon=args.lon,
        stations=stations,
        route_groups=route_groups,
    )

    matrix = build_matrix_from_args(args)
    stop_event = threading.Event()

    def handle_sig(signum, frame):
        stop_event.set()

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    idx = 0
    try:
        while not stop_event.is_set():
            plugin = plugins[idx % len(plugins)]
            try:
                plugin.tick()
            except Exception:
                pass

            try:
                img = plugin.render(width=matrix.width, height=matrix.height)
                matrix.SetImage(img, 0, 0)
            except Exception:
                err = Image.new("RGB", (matrix.width, matrix.height), (80, 0, 0))
                d = ImageDraw.Draw(err)
                font = ImageFont.load_default()
                draw_text(d, 1, 5, f"{plugin.name} err", (255, 255, 255), font)
                matrix.SetImage(err, 0, 0)

            end_at = time.time() + max(2, args.cycle_seconds)
            while time.time() < end_at and not stop_event.is_set():
                time.sleep(0.1)

            idx += 1
    finally:
        try:
            matrix.Clear()
        except Exception:
            pass


if __name__ == "__main__":
    main()