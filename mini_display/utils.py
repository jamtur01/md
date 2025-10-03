#!/usr/bin/env python3
"""
Utility functions for mini display - font rendering and helpers.
"""

from typing import Tuple, Optional
from PIL import ImageDraw, ImageFont


def center_x(panel_w: int, drawn_w: int) -> int:
    """Calculate X coordinate to center content on display."""
    return max(0, (panel_w - drawn_w) // 2)


def draw_text(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    color: Tuple[int, int, int],
    font: Optional[ImageFont.ImageFont] = None
) -> Tuple[int, int]:
    """
    Draw text using PIL's font system (supports full character set).
    
    Args:
        draw: PIL ImageDraw instance
        x: X coordinate to start drawing
        y: Y coordinate to start drawing
        text: Text to draw
        color: RGB color tuple
        font: PIL ImageFont to use (None for default)
        
    Returns:
        Tuple of (width, height) in pixels
    """
    if font is None:
        font = ImageFont.load_default()
    
    draw.text((x, y), text, fill=color, font=font)
    bbox = draw.textbbox((x, y), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def measure_text(
    text: str,
    font: Optional[ImageFont.ImageFont] = None
) -> Tuple[int, int]:
    """
    Measure text dimensions without drawing.
    
    Args:
        text: Text to measure
        font: PIL ImageFont to use (None for default)
        
    Returns:
        Tuple of (width, height) in pixels
    """
    if font is None:
        font = ImageFont.load_default()
    
    # Create a temporary draw object to measure
    from PIL import Image
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def clamp(n: int, lo: int, hi: int) -> int:
    """Clamp value between low and high bounds."""
    return max(lo, min(hi, n))