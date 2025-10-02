#!/usr/bin/env python3
"""
Base plugin interface for mini display plugins.
"""

from PIL import Image


class Plugin:
    """Base plugin interface that all display plugins must implement."""
    name: str = "base"
    
    def tick(self) -> None:
        """Called periodically to update plugin state (e.g., fetch data)."""
        pass
    
    def render(self, width: int, height: int) -> Image.Image:
        """Render the plugin's display content.
        
        Args:
            width: Display width in pixels
            height: Display height in pixels
            
        Returns:
            PIL Image with the rendered content
        """
        raise NotImplementedError