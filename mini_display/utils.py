#!/usr/bin/env python3
"""
Utility functions for mini display - font rendering and helpers.
"""

from typing import Dict, Tuple
from PIL import ImageDraw


# Tiny 4x6 pixel font definitions
FONT_4x6: Dict[str, Tuple[int, int, int, int, int, int]] = {
    " ": (0b0000, 0b0000, 0b0000, 0b0000, 0b0000, 0b0000),
    ":": (0b0000, 0b0110, 0b0110, 0b0000, 0b0110, 0b0110),
    "/": (0b0001, 0b0010, 0b0010, 0b0100, 0b0100, 0b1000),
    "°": (0b0110, 0b1001, 0b0110, 0b0000, 0b0000, 0b0000),
    "^": (0b0110, 0b1001, 0b0000, 0b0000, 0b0000, 0b0000),
    "↑": (0b0010, 0b0111, 0b0010, 0b0010, 0b0010, 0b0000),
    "↓": (0b0010, 0b0010, 0b0010, 0b0111, 0b0010, 0b0000),
    "0": (0b0110, 0b1001, 0b1001, 0b1001, 0b0110, 0b0000),
    "1": (0b0010, 0b0110, 0b0010, 0b0010, 0b0111, 0b0000),
    "2": (0b0110, 0b1001, 0b0001, 0b0110, 0b1111, 0b0000),
    "3": (0b1110, 0b0001, 0b0110, 0b0001, 0b1110, 0b0000),
    "4": (0b1001, 0b1001, 0b1111, 0b0001, 0b0001, 0b0000),
    "5": (0b1111, 0b1000, 0b1110, 0b0001, 0b1110, 0b0000),
    "6": (0b0111, 0b1000, 0b1110, 0b1001, 0b0110, 0b0000),
    "7": (0b1111, 0b0001, 0b0010, 0b0100, 0b0100, 0b0000),
    "8": (0b0110, 0b1001, 0b0110, 0b1001, 0b0110, 0b0000),
    "9": (0b0110, 0b1001, 0b0111, 0b0001, 0b1110, 0b0000),
    "a": (0b0000, 0b0110, 0b0001, 0b0111, 0b0111, 0b0000),
    "p": (0b0000, 0b0110, 0b1001, 0b1110, 0b1000, 0b0000),
    "m": (0b0000, 0b1110, 0b1111, 0b1011, 0b1001, 0b0000),
    "A": (0b0110, 0b1001, 0b1111, 0b1001, 0b1001, 0b0000),
    "B": (0b1110, 0b1001, 0b1110, 0b1001, 0b1110, 0b0000),
    "C": (0b0111, 0b1000, 0b1000, 0b1000, 0b0111, 0b0000),
    "D": (0b1110, 0b1001, 0b1001, 0b1001, 0b1110, 0b0000),
    "E": (0b1111, 0b1000, 0b1110, 0b1000, 0b1111, 0b0000),
    "F": (0b1111, 0b1000, 0b1110, 0b1000, 0b1000, 0b0000),
    "G": (0b0111, 0b1000, 0b1011, 0b1001, 0b0111, 0b0000),
    "H": (0b1001, 0b1001, 0b1111, 0b1001, 0b1001, 0b0000),
    "I": (0b0111, 0b0010, 0b0010, 0b0010, 0b0111, 0b0000),
    "J": (0b0001, 0b0001, 0b0001, 0b1001, 0b0110, 0b0000),
    "K": (0b1001, 0b1010, 0b1100, 0b1010, 0b1001, 0b0000),
    "L": (0b1000, 0b1000, 0b1000, 0b1000, 0b1111, 0b0000),
    "M": (0b1001, 0b1111, 0b1111, 0b1001, 0b1001, 0b0000),
    "N": (0b1001, 0b1101, 0b1011, 0b1001, 0b1001, 0b0000),
    "O": (0b0110, 0b1001, 0b1001, 0b1001, 0b0110, 0b0000),
    "P": (0b1110, 0b1001, 0b1110, 0b1000, 0b1000, 0b0000),
    "Q": (0b0110, 0b1001, 0b1001, 0b1010, 0b0101, 0b0000),
    "R": (0b1110, 0b1001, 0b1110, 0b1010, 0b1001, 0b0000),
    "S": (0b0111, 0b1000, 0b0110, 0b0001, 0b1110, 0b0000),
    "T": (0b1111, 0b0010, 0b0010, 0b0010, 0b0010, 0b0000),
    "U": (0b1001, 0b1001, 0b1001, 0b1001, 0b0110, 0b0000),
    "V": (0b1001, 0b1001, 0b1001, 0b0110, 0b0110, 0b0000),
    "W": (0b1001, 0b1001, 0b1111, 0b1111, 0b1001, 0b0000),
    "X": (0b1001, 0b0110, 0b0110, 0b0110, 0b1001, 0b0000),
    "Y": (0b1001, 0b0110, 0b0010, 0b0010, 0b0010, 0b0000),
    "Z": (0b1111, 0b0001, 0b0010, 0b0100, 0b1111, 0b0000),
}


def measure_small_text(text: str, scale: int = 1, spacing: int = 1) -> Tuple[int, int]:
    """
    Return the pixel width and height the 4x6 font would occupy without drawing.
    
    Args:
        text: Text to measure
        scale: Scale factor for each pixel
        spacing: Spacing between characters in pixels
        
    Returns:
        Tuple of (width, height) in pixels
    """
    if not text:
        return 0, 0
    glyph_w = 4 * scale
    glyph_h = 6 * scale
    width = len(text) * glyph_w + (len(text) - 1) * spacing
    return width, glyph_h


def draw_small_text(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    color: Tuple[int, int, int],
    scale: int = 1,
    spacing: int = 1
) -> Tuple[int, int]:
    """
    Draw text using the 4x6 font.
    
    Args:
        draw: PIL ImageDraw instance
        x: X coordinate to start drawing
        y: Y coordinate to start drawing
        text: Text to draw
        color: RGB color tuple
        scale: Scale factor for each pixel
        spacing: Spacing between characters in pixels
        
    Returns:
        Tuple of (width_drawn, height) in pixels
    """
    cursor_x = x
    for ch in text:
        glyph = FONT_4x6.get(ch, FONT_4x6[" "])
        for row, bits in enumerate(glyph):
            for col in range(4):
                if (bits >> (3 - col)) & 1:
                    draw.rectangle(
                        (
                            cursor_x + col * scale,
                            y + row * scale,
                            cursor_x + col * scale + (scale - 1),
                            y + row * scale + (scale - 1)
                        ),
                        fill=color
                    )
        cursor_x += 4 * scale + spacing
    total_w = cursor_x - x - (spacing if text else 0)
    return total_w, 6 * scale


def center_x(panel_w: int, drawn_w: int) -> int:
    """Calculate X coordinate to center content on display."""
    return max(0, (panel_w - drawn_w) // 2)


def clamp(n: int, lo: int, hi: int) -> int:
    """Clamp value between low and high bounds."""
    return max(lo, min(hi, n))