"""
Custom UI Widgets for Space-Frontier
Provides rounded corners and 3D beveled buttons using Canvas + PIL
Author: Claude AI
Created: 2025-12-27
"""

import tkinter as tk
from PIL import Image, ImageDraw
try:
    from PIL import ImageTk
except ImportError:
    import ImageTk
from typing import Callable, Optional, Tuple
import gc

# Image cache to avoid recreating identical shapes
_image_cache = {}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class RoundedRectangleRenderer:
    """Utility class for generating rounded rectangle images"""

    @staticmethod
    def create_rounded_rect(width: int, height: int, radius: int,
                           fill_color: str, border_color: Optional[str] = None,
                           border_width: int = 1) -> ImageTk.PhotoImage:
        """
        Generate PIL image of rounded rectangle with optional border

        Args:
            width: Image width in pixels
            height: Image height in pixels
            radius: Corner radius in pixels
            fill_color: Fill color as hex string
            border_color: Optional border color as hex string
            border_width: Border thickness in pixels

        Returns:
            ImageTk.PhotoImage ready for Canvas display
        """
        # Check cache first
        cache_key = (width, height, radius, fill_color, border_color, border_width)
        if cache_key in _image_cache:
            return _image_cache[cache_key]

        # Supersampled size for anti-aliasing
        ss_width = width * 2
        ss_height = height * 2
        ss_radius = radius * 2

        # Create image with transparency
        img = Image.new('RGBA', (ss_width, ss_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Convert hex colors to RGB
        fill_rgb = hex_to_rgb(fill_color)

        # Draw rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (ss_width - 1, ss_height - 1)],
            radius=ss_radius,
            fill=fill_rgb + (255,),
            outline=None
        )

        # Add border if specified
        if border_color:
            border_rgb = hex_to_rgb(border_color)
            for i in range(border_width):
                offset = i * 2
                draw.rounded_rectangle(
                    [(offset, offset), (ss_width - offset - 1, ss_height - offset - 1)],
                    radius=max(ss_radius - offset, 1),
                    outline=border_rgb + (255,),
                    width=2
                )

        # Downsample for smooth edges
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        photo_img = ImageTk.PhotoImage(img)

        # Cache it
        _image_cache[cache_key] = photo_img
        return photo_img

    @staticmethod
    def create_gradient_rounded_rect(width: int, height: int, radius: int,
                                     color_start: str, color_end: str,
                                     vertical: bool = True) -> ImageTk.PhotoImage:
        """
        Generate rounded rectangle with gradient fill

        Args:
            width: Image width
            height: Image height
            radius: Corner radius
            color_start: Starting gradient color
            color_end: Ending gradient color
            vertical: True for top-to-bottom, False for left-to-right

        Returns:
            ImageTk.PhotoImage with gradient
        """
        # Check cache
        cache_key = ('gradient', width, height, radius, color_start, color_end, vertical)
        if cache_key in _image_cache:
            return _image_cache[cache_key]

        # Supersampled size
        ss_width = width * 2
        ss_height = height * 2
        ss_radius = radius * 2

        # Create base image
        img = Image.new('RGBA', (ss_width, ss_height), (0, 0, 0, 0))

        # Parse colors
        start_rgb = hex_to_rgb(color_start)
        end_rgb = hex_to_rgb(color_end)

        # Create gradient
        for i in range(ss_height if vertical else ss_width):
            ratio = i / (ss_height if vertical else ss_width)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

            draw = ImageDraw.Draw(img)
            if vertical:
                draw.line([(0, i), (ss_width, i)], fill=(r, g, b, 255))
            else:
                draw.line([(i, 0), (i, ss_height)], fill=(r, g, b, 255))

        # Create mask for rounded corners
        mask = Image.new('L', (ss_width, ss_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [(0, 0), (ss_width - 1, ss_height - 1)],
            radius=ss_radius,
            fill=255
        )

        # Apply mask
        img.putalpha(mask)

        # Downsample
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Convert and cache
        photo_img = ImageTk.PhotoImage(img)
        _image_cache[cache_key] = photo_img
        return photo_img


class RoundedFrame(tk.Canvas):
    """Canvas-based frame with rounded corners"""

    def __init__(self, parent, corner_radius=12, bg_color='#3d2614',
                 border_color='#4d3319', border_width=1, **kwargs):
        """
        Initialize rounded frame

        Args:
            parent: Parent widget
            corner_radius: Radius of corners (10-15px recommended)
            bg_color: Background color
            border_color: Border color
            border_width: Border thickness
        """
        # Set canvas background to transparent or match parent
        canvas_bg = kwargs.pop('canvas_bg', bg_color)
        super().__init__(parent, bg=canvas_bg, highlightthickness=0, **kwargs)

        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width

        self._bg_image = None
        self._bg_image_id = None

        # Create background when widget is configured
        self.bind('<Configure>', self._on_configure)

    def _on_configure(self, event=None):
        """Handle widget resize"""
        width = self.winfo_width()
        height = self.winfo_height()

        if width > 1 and height > 1:  # Valid size
            self._create_background()

    def _create_background(self):
        """Create the rounded background image"""
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Generate rounded rectangle
        self._bg_image = RoundedRectangleRenderer.create_rounded_rect(
            width, height, self.corner_radius,
            self.bg_color, self.border_color, self.border_width
        )

        # Remove old background if exists
        if self._bg_image_id:
            self.delete(self._bg_image_id)

        # Draw new background
        self._bg_image_id = self.create_image(0, 0, image=self._bg_image, anchor='nw', tags='background')
        self.tag_lower('background')  # Send to back

    def set_background_color(self, color: str):
        """Change background color dynamically"""
        self.bg_color = color
        self._create_background()


class BeveledButton(tk.Canvas):
    """3D beveled button with spaceship aesthetic"""

    def __init__(self, parent, text, command=None, width=150, height=40,
                 corner_radius=12, style='normal',
                 font=('Consolas', 10, 'bold'), **kwargs):
        """
        Initialize beveled button

        Args:
            parent: Parent widget
            text: Button text
            command: Callback function
            width: Button width in pixels
            height: Button height in pixels
            corner_radius: Corner radius
            style: Button style ('normal', 'success', 'danger', 'warning', 'accent')
            font: Text font
        """
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, **kwargs)

        self.text = text
        self.command = command
        self.corner_radius = corner_radius
        self.style = style
        self.font = font
        self._pressed = False
        self._hover = False

        # Configure canvas background
        self.configure(bg=kwargs.get('bg', self.master['bg'] if 'bg' in self.master.keys() else '#2b1a0a'))

        # Create button layers
        self._images = []  # Prevent garbage collection
        self._create_button_layers()

        # Bind events
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)

        # Make clickable
        self.config(cursor='hand2')

    def _get_style_colors(self):
        """Get colors for current style"""
        # Import COLORS from parent module if available
        try:
            from gui import COLORS
        except:
            # Fallback colors
            COLORS = {
                'bg_light': '#3d2614',
                'button_hover': '#ff8533',
                'text': '#fff5e6',
                'success': '#66cc33',
                'danger': '#ff3333',
                'warning': '#ffaa00',
                'accent': '#ff9933',
                'bg_dark': '#1a0f00',
                'button_highlight': '#ffc266',
                'button_shadow': '#663300',
            }

        styles = {
            'normal': {
                'bg': COLORS.get('bg_light', '#3d2614'),
                'hover': COLORS.get('button_hover', '#ff8533'),
                'fg': COLORS.get('text', '#fff5e6'),
                'highlight': COLORS.get('button_highlight', '#ffc266'),
                'shadow': COLORS.get('button_shadow', '#663300'),
            },
            'success': {
                'bg': COLORS.get('success', '#66cc33'),
                'hover': '#77dd44',
                'fg': COLORS.get('bg_dark', '#1a0f00'),
                'highlight': '#99ff66',
                'shadow': '#447700',
            },
            'danger': {
                'bg': COLORS.get('danger', '#ff3333'),
                'hover': '#ff4444',
                'fg': COLORS.get('text', '#fff5e6'),
                'highlight': '#ff6666',
                'shadow': '#bb0000',
            },
            'warning': {
                'bg': COLORS.get('warning', '#ffaa00'),
                'hover': '#ffbb00',
                'fg': COLORS.get('bg_dark', '#1a0f00'),
                'highlight': '#ffcc33',
                'shadow': '#cc7700',
            },
            'accent': {
                'bg': COLORS.get('accent', '#ff9933'),
                'hover': '#ffaa44',
                'fg': COLORS.get('bg_dark', '#1a0f00'),
                'highlight': '#ffbb66',
                'shadow': '#cc6600',
            },
        }

        return styles.get(self.style, styles['normal'])

    def _create_button_layers(self):
        """Draw multi-layer 3D button structure"""
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        if width <= 1 or height <= 1:
            width = 150 if self.winfo_reqwidth() <= 1 else self.winfo_reqwidth()
            height = 40 if self.winfo_reqheight() <= 1 else self.winfo_reqheight()

        colors = self._get_style_colors()

        # Layer 1: Drop shadow (slight offset)
        shadow_img = RoundedRectangleRenderer.create_rounded_rect(
            width, height, self.corner_radius,
            fill_color=colors['shadow']
        )
        self.create_image(2, 2, image=shadow_img, anchor='nw', tags='shadow')
        self._images.append(shadow_img)

        # Layer 2: Button base
        base_img = RoundedRectangleRenderer.create_rounded_rect(
            width, height, self.corner_radius,
            fill_color=colors['bg']
        )
        self.create_image(0, 0, image=base_img, anchor='nw', tags='base')
        self._images.append(base_img)

        # Layer 3: Highlight edge (top and left)
        # Top highlight
        self.create_line(
            self.corner_radius, 3,
            width - self.corner_radius, 3,
            fill=colors['highlight'], width=3, tags='highlight_top'
        )
        # Left highlight
        self.create_line(
            3, self.corner_radius,
            3, height - self.corner_radius,
            fill=colors['highlight'], width=3, tags='highlight_left'
        )

        # Layer 4: Shadow edge (bottom and right)
        # Bottom shadow
        self.create_line(
            self.corner_radius, height - 3,
            width - self.corner_radius, height - 3,
            fill=colors['shadow'], width=3, tags='shadow_bottom'
        )
        # Right shadow
        self.create_line(
            width - 3, self.corner_radius,
            width - 3, height - self.corner_radius,
            fill=colors['shadow'], width=3, tags='shadow_right'
        )

        # Layer 5: Text label
        self.create_text(
            width / 2, height / 2,
            text=self.text,
            font=self.font,
            fill=colors['fg'],
            tags='label'
        )

    def _on_enter(self, event):
        """Handle mouse hover"""
        if not self._pressed:
            self._hover = True
            colors = self._get_style_colors()
            # Recreate base with hover color
            width = self.winfo_width()
            height = self.winfo_height()
            hover_img = RoundedRectangleRenderer.create_rounded_rect(
                width, height, self.corner_radius,
                fill_color=colors['hover']
            )
            self.delete('base')
            self.create_image(0, 0, image=hover_img, anchor='nw', tags='base')
            self._images.append(hover_img)
            self.tag_raise('highlight_top')
            self.tag_raise('highlight_left')
            self.tag_raise('shadow_bottom')
            self.tag_raise('shadow_right')
            self.tag_raise('label')

    def _on_leave(self, event):
        """Handle mouse leave"""
        if not self._pressed:
            self._hover = False
            colors = self._get_style_colors()
            # Recreate base with normal color
            width = self.winfo_width()
            height = self.winfo_height()
            normal_img = RoundedRectangleRenderer.create_rounded_rect(
                width, height, self.corner_radius,
                fill_color=colors['bg']
            )
            self.delete('base')
            self.create_image(0, 0, image=normal_img, anchor='nw', tags='base')
            self._images.append(normal_img)
            self.tag_raise('highlight_top')
            self.tag_raise('highlight_left')
            self.tag_raise('shadow_bottom')
            self.tag_raise('shadow_right')
            self.tag_raise('label')

    def _on_press(self, event):
        """Handle button press (visual state)"""
        self._pressed = True
        colors = self._get_style_colors()

        # Swap highlight/shadow colors for pressed effect
        self.itemconfig('highlight_top', fill=colors['shadow'])
        self.itemconfig('highlight_left', fill=colors['shadow'])
        self.itemconfig('shadow_bottom', fill=colors['highlight'])
        self.itemconfig('shadow_right', fill=colors['highlight'])

        # Shift text slightly
        self.move('label', 1, 1)

    def _on_release(self, event):
        """Handle button release and execute command"""
        if self._pressed:
            self._pressed = False
            colors = self._get_style_colors()

            # Restore highlight/shadow
            self.itemconfig('highlight_top', fill=colors['highlight'])
            self.itemconfig('highlight_left', fill=colors['highlight'])
            self.itemconfig('shadow_bottom', fill=colors['shadow'])
            self.itemconfig('shadow_right', fill=colors['shadow'])

            # Restore text position
            self.move('label', -1, -1)

            # Execute command if mouse still over button
            if self._hover and self.command:
                self.command()

    def configure_style(self, style: str):
        """Change button style dynamically"""
        self.style = style
        self.delete('all')
        self._images.clear()
        self._create_button_layers()


class RoundedPanel(tk.Frame):
    """Panel container with optional title bar and rounded corners"""

    def __init__(self, parent, title=None, corner_radius=14,
                 show_title_bar=True, **kwargs):
        """
        Initialize rounded panel

        Args:
            parent: Parent widget
            title: Optional title text
            corner_radius: Corner radius
            show_title_bar: Whether to show title bar
        """
        # Panel background color
        bg_color = kwargs.pop('bg', '#3d2614')

        super().__init__(parent, bg=bg_color, **kwargs)

        self.corner_radius = corner_radius
        self.title_text = title
        self.show_title_bar = show_title_bar and title is not None

        # Create outer rounded frame
        self.outer_frame = RoundedFrame(
            self,
            corner_radius=corner_radius,
            bg_color=bg_color,
            border_color='#4d3319',
            border_width=1
        )
        self.outer_frame.pack(fill=tk.BOTH, expand=True)

        # Content container
        self.content_container = tk.Frame(self.outer_frame, bg=bg_color)
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Title bar if needed
        if self.show_title_bar:
            self._create_title_bar()

        # Content frame (what gets returned to user)
        self.content_frame = tk.Frame(self.content_container, bg=bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_title_bar(self):
        """Create title bar section"""
        try:
            from gui import COLORS
        except:
            COLORS = {
                'bg_medium': '#2b1a0a',
                'accent': '#ff9933',
                'text': '#fff5e6',
                'border_glow': '#ff9933',
            }

        title_frame = tk.Frame(self.content_container, bg=COLORS['bg_medium'], height=35)
        title_frame.pack(fill=tk.X, pady=(5, 0))
        title_frame.pack_propagate(False)

        # Icon
        tk.Label(
            title_frame,
            text="▸",
            font=('Arial', 12),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(side=tk.LEFT, padx=(10, 5))

        # Title text
        tk.Label(
            title_frame,
            text=self.title_text.upper() if self.title_text else "",
            font=('Consolas', 11, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(side=tk.LEFT)

        # Separator
        tk.Frame(
            self.content_container,
            bg=COLORS['border_glow'],
            height=1
        ).pack(fill=tk.X, pady=(0, 5))

    def get_content_frame(self):
        """Return the frame where content should be placed"""
        return self.content_frame


class ProgressBar(tk.Canvas):
    """Rounded progress bar with gradient"""

    def __init__(self, parent, width=100, height=16, corner_radius=8,
                 bg_color='#2b1a0a', fill_color='#ff9933', **kwargs):
        """
        Initialize progress bar

        Args:
            parent: Parent widget
            width: Bar width
            height: Bar height
            corner_radius: Corner radius
            bg_color: Background color
            fill_color: Fill color
        """
        super().__init__(parent, width=width, height=height,
                        highlightthickness=1, highlightbackground='#4d3319',
                        **kwargs)

        self.bar_width = width
        self.bar_height = height
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.fill_color = fill_color

        self.configure(bg=bg_color)

        self._bg_image = None
        self._fill_image = None
        self._percentage = 0

        # Create background
        self._create_background()

    def _create_background(self):
        """Create the background container"""
        self._bg_image = RoundedRectangleRenderer.create_rounded_rect(
            self.bar_width, self.bar_height, self.corner_radius,
            fill_color=self.bg_color
        )
        self.create_image(0, 0, image=self._bg_image, anchor='nw', tags='background')

    def set_progress(self, percentage: float):
        """
        Update progress (0-100)

        Args:
            percentage: Progress percentage (0-100)
        """
        self._percentage = max(0, min(100, percentage))
        fill_width = int((self.bar_width - 4) * (self._percentage / 100))

        if fill_width > 0:
            # Delete old fill
            self.delete('fill')

            # Create new fill
            self._fill_image = RoundedRectangleRenderer.create_rounded_rect(
                fill_width, self.bar_height - 4, self.corner_radius - 2,
                fill_color=self.fill_color
            )
            self.create_image(2, 2, image=self._fill_image, anchor='nw', tags='fill')


def clear_image_cache():
    """Clear all cached images (call if memory constrained)"""
    global _image_cache
    _image_cache.clear()
    gc.collect()
