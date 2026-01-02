#!/usr/bin/env python3
"""
Void Dominion - Standalone GUI Application
Torn-style interface with clickable buttons
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import time
import cv2
from PIL import Image, ImageTk
from game_engine import GameEngine
from data import LOCATIONS, RESOURCES, MODULES, SKILLS, FACTIONS, VESSEL_CLASSES, SHIP_COMPONENTS, RAW_RESOURCES, REFINING_YIELD_RANGES
from save_system import save_exists
from volume_system import can_add_item
from icon_manager import get_icon_manager
from symbols import get_symbol
from ui_widgets import RoundedFrame, BeveledButton, RoundedPanel, ProgressBar

# Color Scheme (Modern Sci-Fi theme)
COLORS = {
    # Background colors
    'bg_dark': '#0a0e17',           # Deep space black
    'bg_medium': '#12182b',         # Dark blue-grey
    'bg_light': '#1a2332',          # Lighter panel background
    'sidebar': '#0d1117',           # Sidebar background

    # Accent colors (Cyan/Blue sci-fi theme)
    'accent': '#00d9ff',            # Bright cyan
    'accent_dim': '#0099cc',        # Dimmed cyan
    'accent_hover': '#00ffff',      # Bright cyan glow
    'secondary': '#7b2cbf',         # Purple accent

    # Text colors
    'text': '#e6edf3',              # Bright white text
    'text_dim': '#8b949e',          # Dimmed grey text
    'text_accent': '#00d9ff',       # Cyan text

    # Status colors
    'success': '#00ff88',           # Bright green
    'danger': '#ff3366',            # Bright red
    'warning': '#ffaa00',           # Bright orange
    'info': '#00d9ff',              # Bright cyan

    # UI elements
    'header': '#0d1117',            # Top bar background
    'border': '#30363d',            # Panel borders
    'border_glow': '#00d9ff',       # Glowing borders
    'button_bg': '#1a2332',         # Button background
    'button_hover': '#243447',      # Button hover
    'button_active': '#00d9ff',     # Active button

    # 3D Button effects
    'button_highlight': '#00ffff',  # Top-left bevel edge (bright cyan)
    'button_shadow': '#001f33',     # Bottom-right bevel edge (dark blue)
    'button_pressed_highlight': '#001f33',  # Inverted when pressed
    'button_pressed_shadow': '#00ffff',     # Inverted when pressed

    # Panel effects
    'panel_highlight': '#2a3f5f',   # Panel top edge
    'panel_shadow': '#0a0e17',      # Panel bottom edge

    # Special effects
    'shadow': '#000000',
    'glow': '#00d9ff40',            # Semi-transparent cyan glow

    # Faction colors
    'faction_meridian': '#4a90e2',      # Blue - Democratic traders
    'faction_technocrat': '#9b59b6',    # Purple - Scientific cabal
    'faction_cipher': '#e74c3c',        # Red - Militaristic empire
    'faction_corsairs': '#e67e22',      # Orange - Pirates
    'faction_neutral': '#95a5a6',       # Grey - Neutral zones
}

# Universe map configuration
MAP_ZOOM_MIN = 0.5            # Minimum zoom level (zoomed out)
MAP_ZOOM_MAX = 4.0            # Maximum zoom level (zoomed in)
MAP_ZOOM_STEP = 0.1           # Zoom increment per mouse wheel tick
MAP_CANVAS_WIDTH = 750        # Base canvas width (50% larger)
MAP_CANVAS_HEIGHT = 600       # Base canvas height (50% larger)


def format_module_specs(module_data: dict) -> str:
    """Format module specifications into a readable string"""
    specs = []

    # Weapon stats
    if 'damage' in module_data:
        damage = module_data['damage']
        fire_rate = module_data.get('fire_rate', 1.0)
        dps = damage * fire_rate
        specs.append(f"DMG: {damage:.0f}")
        specs.append(f"DPS: {dps:.0f}")

    if 'accuracy' in module_data:
        specs.append(f"ACC: {module_data['accuracy']*100:.0f}%")

    if 'fire_rate' in module_data:
        specs.append(f"Rate: {module_data['fire_rate']:.1f}/s")

    # Defense stats
    if 'shield_boost' in module_data:
        specs.append(f"Shield: +{module_data['shield_boost']:.0f}")

    if 'recharge_rate' in module_data:
        specs.append(f"Recharge: {module_data['recharge_rate']:.0f}/s")

    if 'armor_boost' in module_data:
        specs.append(f"Armor: +{module_data['armor_boost']:.0f}")

    if 'damage_reduction' in module_data:
        specs.append(f"Dmg Reduction: {module_data['damage_reduction']*100:.0f}%")

    if 'evasion_boost' in module_data:
        specs.append(f"Evasion: +{module_data['evasion_boost']*100:.0f}%")

    # Utility stats
    if 'scan_range' in module_data:
        specs.append(f"Scan: {module_data['scan_range']:.0f}")

    if 'detection_boost' in module_data:
        specs.append(f"Detection: +{module_data['detection_boost']*100:.0f}%")

    if 'mining_yield' in module_data:
        specs.append(f"Mining Yield: {module_data['mining_yield']*100:.0f}%")

    if 'mining_speed' in module_data:
        specs.append(f"Mining Speed: {module_data['mining_speed']*100:.0f}%")

    if 'speed_boost' in module_data:
        specs.append(f"Speed: +{module_data['speed_boost']*100:.0f}%")

    if 'refining_speed' in module_data:
        specs.append(f"Refining Speed: {module_data['refining_speed']*100:.0f}%")

    if 'refining_efficiency' in module_data:
        specs.append(f"Refining Eff: {module_data['refining_efficiency']*100:.0f}%")

    if 'manufacturing_speed' in module_data:
        specs.append(f"Mfg Speed: {module_data['manufacturing_speed']*100:.0f}%")

    # Power usage (all modules)
    if 'power_usage' in module_data:
        specs.append(f"Power: {module_data['power_usage']:.0f}W")

    return " | ".join(specs) if specs else "No stats available"


class VoidDominionGUI:
    """Main GUI Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Void Dominion")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['bg_dark'])

        self.engine = GameEngine()
        self.current_view = "main"
        self.update_running = False

        # Icon manager for graphics
        self.icon_manager = get_icon_manager()
        self.icon_manager.preload_common_icons()

        # Notification system
        self.notification_container = None
        self.active_notifications = []
        self.last_training_state = set()

        # Status view widget references for live updates
        self.status_training_content = None

        # Market category tracking
        self.current_market_category = 'all'

        # Universe map view state
        self.map_zoom_level = 1.0      # Default zoom (1.0 = normal)
        self.map_pan_offset_x = 0.0    # Pan offset in world coordinates
        self.map_pan_offset_y = 0.0    # Pan offset in world coordinates
        self.map_drag_start = None     # (x, y) mouse position when drag started
        self.map_canvas = None         # Reference to canvas for event binding

        # Video player state
        self.video_cap = None          # cv2.VideoCapture object
        self.video_label = None        # Label to display video frames
        self.video_playing = False     # Whether video is currently playing
        self.video_path = "/home/darenf/Desktop/Claude_Projects/Space-Frontier/Straight_On_Warp_Travel_Video.mp4"

        # Configure styles
        self.setup_styles()

        # Show start screen
        self.show_start_screen()

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        style.configure('TFrame', background=COLORS['bg_medium'])
        style.configure('TLabel', background=COLORS['bg_medium'], foreground=COLORS['text'])
        style.configure('TButton', background=COLORS['button_bg'], foreground=COLORS['text'])
        style.map('TButton', background=[('active', COLORS['button_hover'])])

        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground=COLORS['accent'])
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground=COLORS['accent'])
        style.configure('Stat.TLabel', font=('Arial', 10), foreground=COLORS['text_dim'])

    def show_start_screen(self):
        """Show initial start/load screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        container.pack(expand=True)

        # Title
        title = tk.Label(
            container,
            text="VOID DOMINION",
            font=('Arial', 36, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        )
        title.pack(pady=50)

        subtitle = tk.Label(
            container,
            text="Navigate. Trade. Conquer. Survive.",
            font=('Arial', 14),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_dark']
        )
        subtitle.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(container, bg=COLORS['bg_dark'])
        btn_frame.pack(pady=50)

        # Check for save file
        if save_exists():
            self.create_button(
                btn_frame,
                "Continue Game",
                lambda: self.load_game(),
                width=20
            ).pack(pady=10)

        self.create_button(
            btn_frame,
            "New Game",
            lambda: self.show_new_game_screen(),
            width=20
        ).pack(pady=10)

        self.create_button(
            btn_frame,
            "Exit",
            self.root.quit,
            width=20
        ).pack(pady=10)

    def show_new_game_screen(self):
        """Show new game creation screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        container.pack(expand=True)

        title = tk.Label(
            container,
            text="New Game",
            font=('Arial', 24, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        )
        title.pack(pady=30)

        # Name entry
        tk.Label(
            container,
            text="Commander Name:",
            font=('Arial', 12),
            fg=COLORS['text'],
            bg=COLORS['bg_dark']
        ).pack(pady=10)

        name_entry = tk.Entry(
            container,
            font=('Arial', 14),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            width=30
        )
        name_entry.pack(pady=10)
        name_entry.focus()

        def start_game():
            name = name_entry.get().strip()
            if not name:
                name = "Commander"
            self.engine.new_game(name)
            self.show_main_game()

        self.create_button(
            container,
            "Start Game",
            start_game,
            width=20
        ).pack(pady=30)

        self.create_button(
            container,
            "Back",
            self.show_start_screen,
            width=20
        ).pack(pady=10)

        # Bind enter key
        name_entry.bind('<Return>', lambda e: start_game())

    def load_game(self):
        """Load saved game"""
        if self.engine.load_saved_game():
            self.show_main_game()
        else:
            messagebox.showerror("Error", "Failed to load saved game")

    def show_main_game(self):
        """Show main game interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Start update thread
        self.update_running = True
        self.update_thread = threading.Thread(target=self.game_update_loop, daemon=True)
        self.update_thread.start()

        # Main layout: Top bar + Sidebar + Content area
        self.create_top_bar()
        self.create_main_layout()

        # Create notification overlay
        self.notification_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        self.notification_container.place(relx=0.98, rely=0.08, anchor=tk.NE)

        # Initialize training state to avoid false notifications on load
        if self.engine.player.skill_training:
            for training in self.engine.player.skill_training:
                self.last_training_state.add(training["skill_id"])

        # Show initial view
        self.show_status_view()

    def create_top_bar(self):
        """Create modern top status bar"""
        # Main top bar
        top_bar = tk.Frame(self.root, bg=COLORS['header'], height=50)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        # Add subtle bottom border glow
        border = tk.Frame(self.root, bg=COLORS['border_glow'], height=1)
        border.pack(fill=tk.X)

        # Left side - Commander info
        left_frame = tk.Frame(top_bar, bg=COLORS['header'])
        left_frame.pack(side=tk.LEFT, padx=20, pady=8)

        # Commander name with icon
        commander_container = tk.Frame(left_frame, bg=COLORS['header'])
        commander_container.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(
            commander_container,
            text="◆",
            font=('Arial', 14),
            fg=COLORS['accent'],
            bg=COLORS['header']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.player_name_label = tk.Label(
            commander_container,
            text=f"CMDR {self.engine.player.name.upper()}",
            font=('Consolas', 11, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['header']
        )
        self.player_name_label.pack(side=tk.LEFT)

        # Level and XP
        level_container = tk.Frame(left_frame, bg=COLORS['header'])
        level_container.pack(side=tk.LEFT, padx=(0, 20))

        self.level_label = tk.Label(
            level_container,
            text=f"LVL {self.engine.player.level}",
            font=('Consolas', 10, 'bold'),
            fg=COLORS['warning'],
            bg=COLORS['header']
        )
        self.level_label.pack(side=tk.LEFT, padx=(0, 8))

        # XP progress bar
        xp_bar_container = tk.Frame(level_container, bg=COLORS['bg_dark'], width=100, height=16, highlightthickness=1, highlightbackground=COLORS['border'])
        xp_bar_container.pack(side=tk.LEFT)
        xp_bar_container.pack_propagate(False)

        xp_progress = (self.engine.player.experience / self.engine.player.experience_to_next) * 100
        self.xp_progress_bar = tk.Frame(
            xp_bar_container,
            bg=COLORS['warning'],
            width=int(xp_progress),
            height=16
        )
        self.xp_progress_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.xp_label = tk.Label(
            xp_bar_container,
            text=f"{int(xp_progress)}%",
            font=('Consolas', 8),
            fg=COLORS['text'],
            bg=COLORS['bg_dark']
        )
        self.xp_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Center - Location
        center_frame = tk.Frame(top_bar, bg=COLORS['header'])
        center_frame.pack(side=tk.LEFT, expand=True)

        location_container = tk.Frame(center_frame, bg=COLORS['header'])
        location_container.pack()

        tk.Label(
            location_container,
            text="⬢",
            font=('Arial', 12),
            fg=COLORS['accent'],
            bg=COLORS['header']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.location_label = tk.Label(
            location_container,
            text=f"{LOCATIONS[self.engine.player.location]['name'].upper()}",
            font=('Consolas', 11, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['header']
        )
        self.location_label.pack(side=tk.LEFT)

        # Right side - Credits and Cargo
        right_frame = tk.Frame(top_bar, bg=COLORS['header'])
        right_frame.pack(side=tk.RIGHT, padx=20, pady=8)

        # Credits
        credits_container = tk.Frame(right_frame, bg=COLORS['header'])
        credits_container.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(
            credits_container,
            text="⬡",
            font=('Arial', 12),
            fg=COLORS['success'],
            bg=COLORS['header']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.credits_label = tk.Label(
            credits_container,
            text=f"{self.engine.player.credits:,} CR",
            font=('Consolas', 11, 'bold'),
            fg=COLORS['success'],
            bg=COLORS['header']
        )
        self.credits_label.pack(side=tk.LEFT)

        # Cargo
        cargo_used = self.engine.player.get_cargo_volume()
        cargo_capacity = self.engine.vessel.cargo_capacity
        cargo_percent = (cargo_used / cargo_capacity * 100) if cargo_capacity > 0 else 0
        cargo_color = COLORS['success'] if cargo_percent < 70 else COLORS['warning'] if cargo_percent < 90 else COLORS['danger']

        cargo_container = tk.Frame(right_frame, bg=COLORS['header'])
        cargo_container.pack(side=tk.LEFT)

        tk.Label(
            cargo_container,
            text="⬢",
            font=('Arial', 12),
            fg=cargo_color,
            bg=COLORS['header']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.cargo_label = tk.Label(
            cargo_container,
            text=f"{cargo_used:.0f}/{cargo_capacity:.0f} ({cargo_percent:.0f}%)",
            font=('Consolas', 10),
            fg=cargo_color,
            bg=COLORS['header']
        )
        self.cargo_label.pack(side=tk.LEFT)

        # Save and Exit button
        save_exit_container = tk.Frame(right_frame, bg=COLORS['header'])
        save_exit_container.pack(side=tk.LEFT, padx=(20, 0))

        self.create_button(
            save_exit_container,
            "💾 Save & Exit",
            self.save_and_exit,
            width=12,
            style='danger'
        ).pack()

    def create_main_layout(self):
        """Create main layout with sidebar and content area"""
        # Container for sidebar + content
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar for navigation
        self.create_sidebar(main_container)

        # Right content area
        self.create_content_area(main_container)

    def get_filtered_nav_buttons(self):
        """Get navigation buttons filtered by current location services"""
        location_data = LOCATIONS[self.engine.player.location]
        services = location_data.get("services", [])

        # Define all possible navigation buttons with their service requirements
        # Organized by logical grouping for better flow
        all_nav_buttons = [
            # Player Status
            ("◈ STATUS", "status", self.show_status_view, None),  # Always available
            ("", None, None, None),  # Spacer

            # Navigation & Exploration
            ("◈ TRAVEL", "travel", self.show_travel_view, None),  # Always available
            ("◈ MINING", "mining", self.show_mining_view, None),  # Always available
            ("◈ SCANNING", "scanning", self.show_scanning_view, None),  # Always available
            ("", None, None, None),  # Spacer

            # Ship Management
            ("◈ VESSEL", "vessel", self.show_vessel_view, None),  # Always available
            ("◈ SHIPYARD", "shipyard", self.show_shipyard_view, ["shipyard"]),
            ("◈ MODULES", "modules", self.show_modules_view, ["market", "black_market"]),
            ("", None, None, None),  # Spacer

            # Markets & Trading
            ("◈ MARKET", "market", self.show_market_view, ["market", "black_market"]),
            ("◈ COMPONENTS", "components", self.show_components_view, ["market", "black_market"]),
            ("◈ CONTRACTS", "contracts", self.show_contracts_view, ["contracts"]),
            ("", None, None, None),  # Spacer

            # Production & Storage
            ("◈ MANUFACTURE", "manufacture", self.show_manufacturing_view, ["manufacturing"]),
            ("◈ REFINE", "refine", self.show_refine_view, ["refinery"]),
            ("◈ RECYCLE", "recycle", self.show_recycle_view, ["manufacturing"]),
            ("◈ STORAGE", "storage", self.show_storage_view, None),  # Always available
            ("", None, None, None),  # Spacer

            # Character Development
            ("◈ SKILLS", "skills", self.show_skills_view, None),  # Always available
            ("", None, None, None),  # Spacer

            # System
            ("◆ SAVE GAME", "save", self.save_game, None),  # Always available
        ]

        # Filter buttons based on available services
        filtered_buttons = []
        prev_was_spacer = False

        for text, view_id, command, required_services in all_nav_buttons:
            # Handle spacers
            if not text:
                # Only add spacer if previous wasn't a spacer and we have items after it
                if not prev_was_spacer and filtered_buttons:
                    filtered_buttons.append((text, view_id, command))
                    prev_was_spacer = True
                continue

            # Check if button should be shown
            if required_services is None:
                # Always show
                filtered_buttons.append((text, view_id, command))
                prev_was_spacer = False
            else:
                # Check if any required service is available
                if any(service in services for service in required_services):
                    filtered_buttons.append((text, view_id, command))
                    prev_was_spacer = False

        # Remove trailing spacers
        while filtered_buttons and not filtered_buttons[-1][0]:
            filtered_buttons.pop()

        return filtered_buttons

    def create_sidebar(self, parent):
        """Create left navigation sidebar"""
        self.sidebar = tk.Frame(parent, bg=COLORS['sidebar'], width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Add right border glow
        self.sidebar_border = tk.Frame(parent, bg=COLORS['border_glow'], width=1)
        self.sidebar_border.pack(side=tk.LEFT, fill=tk.Y)

        # Title section
        title_frame = tk.Frame(self.sidebar, bg=COLORS['sidebar'])
        title_frame.pack(fill=tk.X, pady=20, padx=15)

        tk.Label(
            title_frame,
            text="NAVIGATION",
            font=('Consolas', 12, 'bold'),
            fg=COLORS['text_accent'],
            bg=COLORS['sidebar']
        ).pack()

        tk.Frame(title_frame, bg=COLORS['border_glow'], height=1).pack(fill=tk.X, pady=(5, 0))

        # Navigation buttons container
        self.nav_container = tk.Frame(self.sidebar, bg=COLORS['sidebar'])
        self.nav_container.pack(fill=tk.BOTH, expand=True)

        # Initialize current nav if not set
        if not hasattr(self, 'current_nav'):
            self.current_nav = "status"  # Track current view

        self.nav_buttons = {}  # Store button references for highlighting
        self.refresh_navigation()

    def refresh_navigation(self):
        """Rebuild navigation buttons based on current location"""
        # Clear existing buttons
        for widget in self.nav_container.winfo_children():
            widget.destroy()

        self.nav_buttons = {}

        # Get filtered buttons for current location
        nav_buttons = self.get_filtered_nav_buttons()

        for text, view_id, command in nav_buttons:
            if not text:  # Spacer
                tk.Frame(self.nav_container, bg=COLORS['sidebar'], height=10).pack()
                continue

            btn = self.create_nav_button(self.nav_container, text, command, view_id)
            btn.pack(fill=tk.X, padx=10, pady=2)
            if view_id:
                self.nav_buttons[view_id] = btn

        # Check if current view is still available, if not switch to status
        if self.current_nav not in self.nav_buttons and self.current_nav != "save":
            self.current_nav = "status"
            self.show_status_view()
        elif self.current_nav in self.nav_buttons:
            self.highlight_nav_button(self.current_nav)

    def create_nav_button(self, parent, text, command, view_id):
        """Create sidebar navigation button with 3D effect"""
        def on_click():
            # Update current view
            if view_id and view_id != "save":
                self.current_nav = view_id
                self.highlight_nav_button(view_id)
            if command:
                command()

        btn = BeveledButton(
            parent,
            text=text,
            command=on_click,
            width=200,
            height=44,
            corner_radius=10,
            style='normal',
            font=('Consolas', 10, 'bold')
        )

        return btn

    def highlight_nav_button(self, view_id):
        """Highlight the active navigation button"""
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                btn.configure_style('accent')
            else:
                btn.configure_style('normal')

    def create_content_area(self, parent):
        """Create main content area"""
        self.content_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)

    def clear_content(self):
        """Clear content area"""
        self.map_canvas = None  # Clear canvas reference
        self.stop_video_playback()  # Stop any playing video
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_button(self, parent, text, command, width=15, style='normal'):
        """Create 3D beveled button with rounded corners"""
        # Convert character width to pixel width (approximate)
        pixel_width = width * 10

        btn = BeveledButton(
            parent,
            text=text,
            command=command,
            width=pixel_width,
            height=40,
            corner_radius=12,
            style=style,
            font=('Consolas', 9, 'bold')
        )

        return btn

    def create_panel(self, parent, title=None):
        """Create rounded panel with optional title bar"""
        panel = RoundedPanel(
            parent,
            title=title,
            corner_radius=14,
            show_title_bar=(title is not None),
            bg=COLORS['bg_light']
        )

        content = panel.get_content_frame()
        return panel, content

    def create_scrollable_frame(self, parent, bg_color=None):
        """
        Create a scrollable frame that expands to fill available width
        Returns: (canvas, scrollbar, scrollable_frame)
        """
        if bg_color is None:
            bg_color = COLORS['bg_medium']

        canvas = tk.Canvas(parent, bg=bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg_color)

        # Update scroll region when content changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
        )

        # Create window and make it expand to canvas width
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind canvas width changes to update scrollable frame width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        return canvas, scrollbar, scrollable_frame

    def bind_mousewheel(self, canvas, frame):
        """Bind mouse wheel scrolling to canvas"""
        def on_mousewheel(event):
            # Windows/Mac
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")

        def bind_wheel(event):
            canvas.bind_all("<Button-4>", on_mousewheel)  # Linux scroll up
            canvas.bind_all("<Button-5>", on_mousewheel)  # Linux scroll down
            canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac

        def unbind_wheel(event):
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
            canvas.unbind_all("<MouseWheel>")

        # Bind/unbind on mouse enter/leave
        canvas.bind("<Enter>", bind_wheel)
        canvas.bind("<Leave>", unbind_wheel)
        frame.bind("<Enter>", bind_wheel)
        frame.bind("<Leave>", unbind_wheel)

    def on_map_mousewheel(self, event):
        """Handle mouse wheel for zooming the universe map"""
        # Determine scroll direction (cross-platform)
        if event.num == 4 or event.delta > 0:
            zoom_delta = MAP_ZOOM_STEP  # Zoom in
        elif event.num == 5 or event.delta < 0:
            zoom_delta = -MAP_ZOOM_STEP  # Zoom out
        else:
            return

        # Calculate new zoom level
        new_zoom = self.map_zoom_level + zoom_delta
        new_zoom = max(MAP_ZOOM_MIN, min(MAP_ZOOM_MAX, new_zoom))

        if new_zoom == self.map_zoom_level:
            return  # Already at min/max

        # Get mouse position on canvas
        canvas_x = event.x
        canvas_y = event.y

        # Convert to world coordinates (before zoom)
        world_x = (canvas_x - MAP_CANVAS_WIDTH/2 - self.map_pan_offset_x) / self.map_zoom_level
        world_y = (canvas_y - MAP_CANVAS_HEIGHT/2 - self.map_pan_offset_y) / self.map_zoom_level

        # Update zoom level
        old_zoom = self.map_zoom_level
        self.map_zoom_level = new_zoom

        # Adjust pan offset to keep mouse position stable (zoom to cursor)
        # New screen position should match old screen position
        new_screen_x = world_x * self.map_zoom_level + MAP_CANVAS_WIDTH/2 + self.map_pan_offset_x
        new_screen_y = world_y * self.map_zoom_level + MAP_CANVAS_HEIGHT/2 + self.map_pan_offset_y

        self.map_pan_offset_x += canvas_x - new_screen_x
        self.map_pan_offset_y += canvas_y - new_screen_y

        # Redraw map
        self.redraw_universe_map()

    def on_map_button_press(self, event):
        """Handle mouse button press for starting pan drag"""
        # Store drag start position
        self.map_drag_start = (event.x, event.y)
        # Change cursor to indicate dragging
        if self.map_canvas:
            self.map_canvas.config(cursor="fleur")  # Four-way arrow cursor

    def on_map_motion(self, event):
        """Handle mouse motion for panning the map"""
        if self.map_drag_start is None:
            return  # Not dragging

        # Calculate delta from drag start
        dx = event.x - self.map_drag_start[0]
        dy = event.y - self.map_drag_start[1]

        # Update pan offset
        self.map_pan_offset_x += dx
        self.map_pan_offset_y += dy

        # Update drag start for next motion event
        self.map_drag_start = (event.x, event.y)

        # Redraw map
        self.redraw_universe_map()

    def on_map_button_release(self, event):
        """Handle mouse button release for ending pan drag"""
        self.map_drag_start = None
        # Reset cursor
        if self.map_canvas:
            self.map_canvas.config(cursor="")

    def redraw_universe_map(self):
        """Redraw the universe map with current zoom/pan settings"""
        if self.map_canvas is None:
            return  # Canvas not initialized yet

        # Clear canvas
        self.map_canvas.delete("all")

        # Define coordinates for each location (x, y) - normalized 0-1
        # Complete galaxy map with all 58 locations organized by faction territories
        location_coords = {
            # ========== NEUTRAL ZONE - CENTER (4 core locations) ==========
            "nexus_prime": (0.50, 0.50),  # Starting location
            "starlight_waystation": (0.45, 0.45),
            "freeport_exchange": (0.55, 0.55),
            "tranquil_belt": (0.50, 0.40),

            # ========== MERIDIAN COLLECTIVE - UPPER RIGHT (9 locations) ==========
            "meridian_gates": (0.65, 0.35),
            "titan_alpha": (0.70, 0.50),
            "aurora_reach": (0.75, 0.40),
            "prosperity_hub": (0.80, 0.35),
            "eden_prime": (0.85, 0.45),
            "explorer_outpost": (0.90, 0.40),
            "horizon_vista": (0.85, 0.30),
            "merchant_corridor": (0.75, 0.30),

            # ========== CIPHER DOMINION - LOWER RIGHT (10 locations) ==========
            "crimson_expanse": (0.65, 0.65),
            "ironhold_sectors": (0.70, 0.70),
            "ironhold_world": (0.75, 0.75),
            "bastion_prime": (0.80, 0.70),
            "garrison_outpost": (0.85, 0.75),
            "conquest_reach": (0.90, 0.70),
            "vanguard_citadel": (0.85, 0.85),
            "dreadnought_yards": (0.90, 0.80),
            "supremacy_throne": (0.95, 0.85),
            "contested_zone": (0.70, 0.60),

            # ========== TECHNOCRAT UNION - UPPER LEFT (11 locations) ==========
            "forge_station": (0.35, 0.35),
            "synthesis_planet": (0.25, 0.30),
            "neural_network": (0.20, 0.35),
            "axiom_labs": (0.15, 0.30),
            "datacore_prime": (0.10, 0.35),
            "protocol_labs": (0.15, 0.25),
            "singularity_reach": (0.10, 0.20),
            "void_forge": (0.20, 0.20),
            "silicon_spire": (0.25, 0.15),
            "convergence_nexus": (0.30, 0.20),
            "algorithm_expanse": (0.05, 0.25),

            # ========== VOID CORSAIRS - LOWER LEFT (6 locations) ==========
            "shadow_nebula": (0.30, 0.70),
            "corsair_haven": (0.25, 0.75),
            "blackmarket_dock": (0.30, 0.80),
            "phantom_reach": (0.20, 0.70),
            "oblivion_gate": (0.15, 0.75),
            "dread_maw": (0.10, 0.80),

            # ========== NEUTRAL ASTEROIDS - SCATTERED (22 locations) ==========
            # Upper edge
            "pristine_fields": (0.60, 0.10),
            "circuit_fields": (0.50, 0.15),
            "crystal_gardens": (0.40, 0.10),

            # Right edge
            "harvest_fields": (0.95, 0.60),
            "sapphire_fields": (0.95, 0.50),
            "verdant_belt": (0.90, 0.55),

            # Bottom edge
            "dead_zone_asteroids": (0.50, 0.90),
            "outer_belts": (0.60, 0.85),
            "reaver_belt": (0.40, 0.90),
            "bloodstone_fields": (0.35, 0.85),

            # Left edge
            "chronos_expanse": (0.05, 0.45),
            "quantum_drift": (0.05, 0.55),
            "recursion_point": (0.05, 0.65),

            # Between territories (connectors)
            "iron_expanse": (0.60, 0.75),
            "warforge_belt": (0.75, 0.65),
            "sovereign_belt": (0.80, 0.80),
            "binary_belt": (0.35, 0.25),
            "uncharted_expanse": (0.45, 0.60),
            "abyss_edge": (0.15, 0.85),
        }

        # Helper function: Transform normalized coords to screen coords
        def to_screen_coords(norm_x, norm_y):
            # Convert normalized (0-1) to world coordinates (-1 to 1 centered)
            world_x = (norm_x - 0.5) * 1000  # Scale to larger world space
            world_y = (norm_y - 0.5) * 800

            # Apply zoom
            zoomed_x = world_x * self.map_zoom_level
            zoomed_y = world_y * self.map_zoom_level

            # Apply pan and center in canvas
            screen_x = zoomed_x + MAP_CANVAS_WIDTH/2 + self.map_pan_offset_x
            screen_y = zoomed_y + MAP_CANVAS_HEIGHT/2 + self.map_pan_offset_y

            return screen_x, screen_y

        # Get player data
        visited = self.engine.player.visited_locations
        current_location = self.engine.player.location

        # Draw connections first (as lines)
        for loc_id, loc_data in LOCATIONS.items():
            if loc_id not in location_coords:
                continue

            x1, y1 = to_screen_coords(*location_coords[loc_id])
            loc_visible = loc_id in visited

            for connected_id in loc_data.get("connections", []):
                if connected_id not in location_coords:
                    continue

                connected_visible = connected_id in visited
                x2, y2 = to_screen_coords(*location_coords[connected_id])

                # Show line if either endpoint is visited
                if loc_visible or connected_visible:
                    line_color = COLORS['text_dim'] if (loc_visible and connected_visible) else '#2a2a2a'
                    self.map_canvas.create_line(
                        x1, y1, x2, y2,
                        fill=line_color,
                        width=1,
                        dash=(2, 2) if not (loc_visible and connected_visible) else ()
                    )

        # Draw locations (as circles)
        for loc_id, loc_data in LOCATIONS.items():
            if loc_id not in location_coords:
                continue

            x, y = to_screen_coords(*location_coords[loc_id])
            is_visited = loc_id in visited
            is_current = loc_id == current_location

            # Determine if location should be visible
            if is_visited:
                # Get faction color
                faction = loc_data.get("faction")
                if faction == "meridian_collective":
                    base_color = COLORS['faction_meridian']
                elif faction == "technocrat_union":
                    base_color = COLORS['faction_technocrat']
                elif faction == "cipher_dominion":
                    base_color = COLORS['faction_cipher']
                elif faction == "void_corsairs":
                    base_color = COLORS['faction_corsairs']
                else:
                    base_color = COLORS['faction_neutral']

                # Visited location - faction colored
                if is_current:
                    fill_color = COLORS['success']
                    outline_color = COLORS['accent']
                    radius = 8
                else:
                    fill_color = base_color
                    outline_color = COLORS['text']
                    radius = 6 if loc_data.get("type") == "station" else 5

                # Draw circle
                self.map_canvas.create_oval(
                    x - radius, y - radius, x + radius, y + radius,
                    fill=fill_color, outline=outline_color, width=2
                )

                # Draw name (full name) with background for visibility
                self.map_canvas.create_text(
                    x, y - radius - 12,
                    text=loc_data["name"],
                    fill=COLORS['text'],
                    font=('Arial', 9, 'bold'),
                    anchor='s'
                )

                # If current, add pulsing indicator
                if is_current:
                    self.map_canvas.create_text(
                        x, y,
                        text="◉",
                        fill=COLORS['accent'],
                        font=('Arial', 12)
                    )

            else:
                # Check if any connected location is visited (to show fog partially)
                has_visited_neighbor = any(conn in visited for conn in loc_data.get("connections", []))

                if has_visited_neighbor:
                    # Partially visible (fogged)
                    fill_color = '#1a1a1a'
                    outline_color = '#3a3a3a'
                    radius = 4
                    self.map_canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius,
                        fill=fill_color, outline=outline_color, width=1, dash=(2, 2)
                    )
                    self.map_canvas.create_text(
                        x, y - radius - 10,
                        text="?",
                        fill='#5a5a5a',
                        font=('Arial', 9, 'bold'),
                        anchor='s'
                    )
                # else: completely hidden

        # Add legend (FIXED position - bottom-left, not transformed)
        legend_x = 10
        legend_y = MAP_CANVAS_HEIGHT - 100

        self.map_canvas.create_text(
            legend_x, legend_y,
            text="Factions:",
            fill=COLORS['text'],
            font=('Arial', 10, 'bold'),
            anchor='w'
        )

        # Faction legend - Row 1
        factions_row1 = [
            (COLORS['faction_meridian'], "Meridian", legend_x + 5),
            (COLORS['faction_technocrat'], "Technocrat", legend_x + 110),
            (COLORS['faction_cipher'], "Cipher", legend_x + 220),
        ]

        y_pos = legend_y + 18
        for color, name, x_start in factions_row1:
            self.map_canvas.create_oval(
                x_start, y_pos - 4, x_start + 8, y_pos + 4,
                fill=color, outline=COLORS['text'], width=1
            )
            self.map_canvas.create_text(
                x_start + 13, y_pos,
                text=name,
                fill=COLORS['text'],
                font=('Arial', 8),
                anchor='w'
            )

        # Faction legend - Row 2
        factions_row2 = [
            (COLORS['faction_corsairs'], "Corsairs", legend_x + 5),
            (COLORS['faction_neutral'], "Neutral", legend_x + 110),
            (COLORS['success'], "Current", legend_x + 220),
        ]

        y_pos = legend_y + 35
        for color, name, x_start in factions_row2:
            outline = COLORS['accent'] if name == "Current" else COLORS['text']
            width = 2 if name == "Current" else 1
            self.map_canvas.create_oval(
                x_start, y_pos - 4, x_start + 8, y_pos + 4,
                fill=color, outline=outline, width=width
            )
            self.map_canvas.create_text(
                x_start + 13, y_pos,
                text=name,
                fill=COLORS['text'],
                font=('Arial', 8),
                anchor='w'
            )

        # Unexplored
        self.map_canvas.create_oval(
            legend_x + 330, y_pos - 4, legend_x + 338, y_pos + 4,
            fill='#1a1a1a', outline='#3a3a3a', width=1, dash=(2, 2)
        )
        self.map_canvas.create_text(
            legend_x + 343, y_pos,
            text="Unknown",
            fill=COLORS['text'],
            font=('Arial', 8),
            anchor='w'
        )

        # Add exploration stats (FIXED position - top-right, not transformed)
        total_locations = len(LOCATIONS)
        visited_count = len(visited)
        exploration_pct = (visited_count / total_locations * 100) if total_locations > 0 else 0

        self.map_canvas.create_text(
            MAP_CANVAS_WIDTH - 10, 15,
            text=f"Explored: {visited_count}/{total_locations} ({exploration_pct:.0f}%)",
            fill=COLORS['text_accent'],
            font=('Arial', 9, 'bold'),
            anchor='e'
        )

    def draw_universe_map(self, parent):
        """Draw universe map with fog of war - setup and event binding"""
        # Create canvas (store reference for event handlers)
        self.map_canvas = tk.Canvas(
            parent,
            bg=COLORS['bg_dark'],
            width=MAP_CANVAS_WIDTH,
            height=MAP_CANVAS_HEIGHT,
            highlightthickness=1,
            highlightbackground=COLORS['text_dim']
        )
        self.map_canvas.pack(pady=10, padx=10)

        # Bind mouse events
        self.map_canvas.bind("<Button-4>", self.on_map_mousewheel)  # Linux scroll up
        self.map_canvas.bind("<Button-5>", self.on_map_mousewheel)  # Linux scroll down
        self.map_canvas.bind("<MouseWheel>", self.on_map_mousewheel)  # Windows/Mac
        self.map_canvas.bind("<ButtonPress-1>", self.on_map_button_press)  # Left click
        self.map_canvas.bind("<B1-Motion>", self.on_map_motion)  # Drag
        self.map_canvas.bind("<ButtonRelease-1>", self.on_map_button_release)  # Release

        # Initial draw
        self.redraw_universe_map()

        # Add info text (below canvas)
        info_text = tk.Label(
            parent,
            text="🗺️ Scroll to zoom, drag to pan | Travel to new locations to reveal more of the universe",
            font=('Arial', 8, 'italic'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        )
        info_text.pack(pady=(0, 5))

    def show_status_view(self):
        """Show status overview"""
        self.current_view = "status"
        self.clear_content()

        # Reset map zoom/pan state
        self.map_zoom_level = 1.0
        self.map_pan_offset_x = 0.0
        self.map_pan_offset_y = 0.0

        # Left column - Player & Vessel status
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Player panel
        player_panel, player_content = self.create_panel(left_col, "Commander Status")
        player_panel.pack(fill=tk.X, pady=5)

        stats = [
            ("Name", self.engine.player.name),
            ("Level", f"{self.engine.player.level}"),
            ("Experience", f"{self.engine.player.experience} / {self.engine.player.experience_to_next} XP"),
            ("Credits", f"{self.engine.player.credits:,} CR"),
            ("Location", LOCATIONS[self.engine.player.location]['name']),
            ("Contracts Completed", self.engine.player.stats['contracts_completed']),
            ("Enemies Destroyed", self.engine.player.stats['enemies_destroyed']),
            ("Resources Mined", self.engine.player.stats['resources_mined'])
        ]

        for label, value in stats:
            row = tk.Frame(player_content, bg=COLORS['bg_medium'])
            row.pack(fill=tk.X, pady=2)

            tk.Label(
                row,
                text=f"{label}:",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium'],
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=str(value),
                font=('Arial', 10, 'bold'),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                anchor='w'
            ).pack(side=tk.LEFT)

        # Vessel panel
        vessel_panel, vessel_content = self.create_panel(left_col, "Vessel Status")
        vessel_panel.pack(fill=tk.X, pady=5)

        vessel = self.engine.vessel
        cargo_used = self.engine.player.get_cargo_volume()
        cargo_capacity = vessel.cargo_capacity
        cargo_percent = (cargo_used / cargo_capacity * 100) if cargo_capacity > 0 else 0

        vessel_stats = [
            ("Name", vessel.name),
            ("Class", vessel.class_name),
            ("Hull", f"{vessel.current_hull_hp:.0f}/{vessel.max_hull_hp:.0f} ({vessel.get_hull_percentage():.1f}%)"),
            ("Shields", f"{vessel.current_shields:.0f}/{vessel.get_total_shield_capacity():.0f} ({vessel.get_shield_percentage():.1f}%)"),
            ("Armor", f"{vessel.get_total_armor():.0f}"),
            ("Speed", f"{vessel.get_effective_speed():.0f}"),
            ("Cargo", f"{cargo_used:.1f}/{cargo_capacity:.0f} ({cargo_percent:.1f}%)")
        ]

        for label, value in vessel_stats:
            row = tk.Frame(vessel_content, bg=COLORS['bg_medium'])
            row.pack(fill=tk.X, pady=2)

            tk.Label(
                row,
                text=f"{label}:",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium'],
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=str(value),
                font=('Arial', 10, 'bold'),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                anchor='w'
            ).pack(side=tk.LEFT)

        # Right column - Active info
        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Universe Map
        map_panel, map_content = self.create_panel(right_col, "⭐ Universe Map")
        map_panel.pack(fill=tk.BOTH, expand=True, pady=5)

        self.draw_universe_map(map_content)

        # Active contracts
        contracts_panel, contracts_content = self.create_panel(right_col, "📋 Active Contracts")
        contracts_panel.pack(fill=tk.BOTH, expand=True, pady=5)

        active_contracts = self.engine.contract_board.get_active_contracts()

        if active_contracts:
            for contract in active_contracts:
                contract_frame = tk.Frame(contracts_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                contract_frame.pack(fill=tk.X, pady=8, padx=5)

                # Header with contract name and type
                header_frame = tk.Frame(contract_frame, bg=COLORS['bg_medium'])
                header_frame.pack(fill=tk.X, padx=0, pady=0)

                tk.Label(
                    header_frame,
                    text=contract.name,
                    font=('Arial', 12, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_medium']
                ).pack(anchor='w', padx=10, pady=5)

                tk.Label(
                    header_frame,
                    text=f"Type: {contract.type.replace('_', ' ').title()}",
                    font=('Arial', 9, 'italic'),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_medium']
                ).pack(anchor='w', padx=10, pady=(0, 5))

                # Contract details
                details_frame = tk.Frame(contract_frame, bg=COLORS['bg_light'])
                details_frame.pack(fill=tk.X, padx=10, pady=8)

                # Description
                tk.Label(
                    details_frame,
                    text=contract.description,
                    font=('Arial', 9),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light'],
                    wraplength=400,
                    justify='left'
                ).pack(anchor='w', pady=3)

                # Progress
                progress_frame = tk.Frame(details_frame, bg=COLORS['bg_light'])
                progress_frame.pack(fill=tk.X, pady=5)

                tk.Label(
                    progress_frame,
                    text="Progress:",
                    font=('Arial', 9, 'bold'),
                    fg=COLORS['text_accent'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT)

                tk.Label(
                    progress_frame,
                    text=contract.get_progress_text(),
                    font=('Arial', 9),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT, padx=5)

                # Time and reward info
                info_frame = tk.Frame(details_frame, bg=COLORS['bg_light'])
                info_frame.pack(fill=tk.X, pady=3)

                time_remaining = contract.get_time_remaining()
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)

                tk.Label(
                    info_frame,
                    text=f"⏱️ Time Remaining: {minutes}m {seconds}s",
                    font=('Arial', 9),
                    fg=COLORS['warning'] if time_remaining < 300 else COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    info_frame,
                    text=f"💰 Reward: {contract.reward:,} CR",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=2)

                # Location if applicable
                if hasattr(contract, 'target_location') and contract.target_location:
                    location_name = LOCATIONS.get(contract.target_location, {}).get('name', contract.target_location)
                    tk.Label(
                        info_frame,
                        text=f"📍 Target: {location_name}",
                        font=('Arial', 9),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)

                # Delivery destination info
                if contract.objectives.get("type") == "transport_cargo":
                    from data import COMMODITIES
                    dest_id = contract.objectives.get("destination")
                    dest_name = LOCATIONS.get(dest_id, {}).get("name", dest_id)
                    item_id = contract.objectives.get("resource_id")
                    item_type = contract.objectives.get("item_type", "resource")
                    quantity = contract.objectives.get("quantity", 0)

                    # Get item name
                    if item_type == "commodity":
                        item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
                    else:
                        item_name = RESOURCES.get(item_id, {}).get("name", item_id)

                    # Source location name
                    source_name = LOCATIONS.get(contract.location_id, {}).get("name", contract.location_id)

                    tk.Label(
                        info_frame,
                        text=f"🎯 Deliver to: {dest_name}",
                        font=('Arial', 9, 'bold'),
                        fg=COLORS['accent'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)

                    tk.Label(
                        info_frame,
                        text=f"📦 Cargo: {quantity}x {item_name}",
                        font=('Arial', 9),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)

                    tk.Label(
                        info_frame,
                        text=f"💾 Items stored at: {source_name} (check STORAGE tab)",
                        font=('Arial', 9, 'italic'),
                        fg=COLORS['warning'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)

                # Action buttons
                button_frame = tk.Frame(contract_frame, bg=COLORS['bg_light'])
                button_frame.pack(fill=tk.X, padx=10, pady=8)

                # Delivery completion button for cargo transport contracts
                if contract.objectives.get("type") == "transport_cargo":
                    self.create_button(
                        button_frame,
                        "Deliver Cargo",
                        lambda c=contract: self.complete_delivery_contract(c),
                        width=15,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)

                # Abandon button
                self.create_button(
                    button_frame,
                    "Abandon",
                    lambda c=contract: self.abandon_contract(c),
                    width=12,
                    style='danger'
                ).pack(side=tk.LEFT, padx=2)

        else:
            # No contracts message
            no_contract_frame = tk.Frame(contracts_content, bg=COLORS['bg_medium'])
            no_contract_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=10)

            tk.Label(
                no_contract_frame,
                text="📋 No Active Contracts",
                font=('Arial', 12, 'bold'),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=(10, 5))

            tk.Label(
                no_contract_frame,
                text="Visit the Contracts page to accept new missions",
                font=('Arial', 9, 'italic'),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=(0, 10))

        # Skill training
        training_panel, training_content = self.create_panel(right_col, "⚡ Skill Training")
        training_panel.pack(fill=tk.X, pady=5)

        # Store reference for live updates
        self.status_training_content = training_content

        # Initial render
        self.update_status_training_panel()

    def update_status_training_panel(self):
        """Update just the training panel on status view without rebuilding entire screen"""
        if not self.status_training_content or not self.status_training_content.winfo_exists():
            return

        # Clear existing content
        for widget in self.status_training_content.winfo_children():
            widget.destroy()

        training = self.engine.player.get_training_progress()

        if training:
            # Show header with slot usage
            max_slots = self.engine.player.get_max_training_slots()
            tk.Label(
                self.status_training_content,
                text=f"Training {len(training)} of {max_slots} slots",
                font=('Arial', 9, 'italic'),
                fg=COLORS['text_accent'],
                bg=COLORS['bg_medium']
            ).pack(anchor='w', padx=5, pady=(5, 10))

            # Show each training skill
            for idx, skill_training in enumerate(training):
                skill_frame = tk.Frame(self.status_training_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                skill_frame.pack(fill=tk.X, pady=3, padx=5)

                # Skill name and level
                header_frame = tk.Frame(skill_frame, bg=COLORS['bg_light'])
                header_frame.pack(fill=tk.X, padx=8, pady=5)

                # Training position indicator (1st, 2nd, etc.)
                position_label = tk.Label(
                    header_frame,
                    text=f"#{idx+1}",
                    font=('Arial', 9, 'bold'),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light'],
                    width=3
                )
                position_label.pack(side=tk.LEFT, padx=(0, 5))

                tk.Label(
                    header_frame,
                    text=f"{skill_training['skill_name']} → Lvl {skill_training['target_level']}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT)

                # Progress bar
                progress_frame = tk.Frame(skill_frame, bg=COLORS['bg_dark'], height=16)
                progress_frame.pack(fill=tk.X, padx=8, pady=3)

                progress_bar = tk.Frame(
                    progress_frame,
                    bg=COLORS['success'],
                    width=int(skill_training['progress'] * 3),
                    height=16
                )
                progress_bar.pack(side=tk.LEFT)

                # Time remaining
                minutes = int(skill_training['remaining_seconds']) // 60
                seconds = int(skill_training['remaining_seconds']) % 60
                time_text = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

                tk.Label(
                    skill_frame,
                    text=f"{skill_training['progress']:.1f}% - {time_text} remaining",
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', padx=8, pady=(0, 5))
        else:
            tk.Label(
                self.status_training_content,
                text="No skill training active",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

        # Show recently completed skills (last 3)
        recent = self.engine.player.recently_completed_skills
        if recent:
            # Separator
            separator = tk.Frame(self.status_training_content, bg=COLORS['border'], height=2)
            separator.pack(fill=tk.X, pady=10, padx=5)

            # Header
            tk.Label(
                self.status_training_content,
                text="Recently Completed",
                font=('Arial', 10, 'bold'),
                fg=COLORS['success'],
                bg=COLORS['bg_medium']
            ).pack(anchor='w', padx=5, pady=(5, 10))

            # Show each completed skill
            for completed in recent:
                skill_frame = tk.Frame(self.status_training_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                skill_frame.pack(fill=tk.X, pady=2, padx=5)

                # Skill name and level
                header_frame = tk.Frame(skill_frame, bg=COLORS['bg_light'])
                header_frame.pack(fill=tk.X, padx=8, pady=5)

                # Checkmark
                tk.Label(
                    header_frame,
                    text="✓",
                    font=('Arial', 12, 'bold'),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light'],
                    width=2
                ).pack(side=tk.LEFT, padx=(0, 5))

                tk.Label(
                    header_frame,
                    text=f"{completed['skill_name']} → Lvl {completed['level']}",
                    font=('Arial', 9),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT)

                # Time since completion
                elapsed = time.time() - completed['completion_time']
                if elapsed < 60:
                    time_ago = "just now"
                elif elapsed < 3600:
                    time_ago = f"{int(elapsed / 60)}m ago"
                else:
                    time_ago = f"{int(elapsed / 3600)}h ago"

                tk.Label(
                    header_frame,
                    text=time_ago,
                    font=('Arial', 8, 'italic'),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.RIGHT, padx=5)

    def show_mining_view(self):
        """Show mining operations view"""
        self.current_view = "mining"
        self.clear_content()

        # Title panel
        title_panel, title_content = self.create_panel(self.content_frame, "⛏️ MINING OPERATIONS")
        title_panel.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(
            title_content,
            text="Extract valuable resources from asteroid fields and mineral deposits",
            font=('Arial', 11, 'italic'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Mining info panel
        info_panel, info_content = self.create_panel(self.content_frame, "📊 Mining Equipment Status")
        info_panel.pack(fill=tk.X, pady=(0, 20), padx=20)

        # Get mining capabilities
        mining_efficiency = self.engine.vessel.get_mining_efficiency()
        mining_tier = self.engine.vessel.get_mining_tier()

        info_text = f"Mining Tier: {mining_tier}\n"
        info_text += f"Mining Efficiency: {mining_efficiency:.2f}x\n"
        info_text += f"Current Location: {LOCATIONS[self.engine.player.location]['name']}"

        tk.Label(
            info_content,
            text=info_text,
            font=('Arial', 11),
            fg=COLORS['text'],
            bg=COLORS['bg_medium'],
            justify=tk.LEFT
        ).pack(pady=10, padx=20)

        # Mining action panel
        action_panel, action_content = self.create_panel(self.content_frame, "⚡ Mining Actions")
        action_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 20), padx=20)

        # Center the button
        button_frame = tk.Frame(action_content, bg=COLORS['bg_medium'])
        button_frame.pack(expand=True)

        mine_btn = self.create_button(
            button_frame,
            "⛏️ MINE RESOURCES",
            self.mine_resources,
            width=30,
            style='warning'
        )
        mine_btn.pack(pady=50)

        # Help text
        tk.Label(
            action_content,
            text="Click the button above to mine resources at your current location.\nMining equipment efficiency and bonuses affect your yield.",
            font=('Arial', 10, 'italic'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium'],
            justify=tk.CENTER
        ).pack(pady=(0, 20))

    def show_scanning_view(self):
        """Show scanning operations view"""
        self.current_view = "scanning"
        self.clear_content()

        # Title panel
        title_panel, title_content = self.create_panel(self.content_frame, "🔍 SCANNING OPERATIONS")
        title_panel.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(
            title_content,
            text="Scan your surroundings for resources, anomalies, and hidden discoveries",
            font=('Arial', 11, 'italic'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Scanner info panel
        info_panel, info_content = self.create_panel(self.content_frame, "📡 Scanner Equipment Status")
        info_panel.pack(fill=tk.X, pady=(0, 20), padx=20)

        # Get scanning capabilities
        scan_range = self.engine.vessel.get_scan_range()

        info_text = f"Scan Range: {scan_range:.0f} km\n"
        info_text += f"Current Location: {LOCATIONS[self.engine.player.location]['name']}"

        tk.Label(
            info_content,
            text=info_text,
            font=('Arial', 11),
            fg=COLORS['text'],
            bg=COLORS['bg_medium'],
            justify=tk.LEFT
        ).pack(pady=10, padx=20)

        # Scanning actions panel
        action_panel, action_content = self.create_panel(self.content_frame, "⚡ Scanning Actions")
        action_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 20), padx=20)

        # Center the buttons
        button_frame = tk.Frame(action_content, bg=COLORS['bg_medium'])
        button_frame.pack(expand=True)

        scan_area_btn = self.create_button(
            button_frame,
            "🔍 SCAN AREA",
            self.scan_area,
            width=30,
            style='success'
        )
        scan_area_btn.pack(pady=20)

        anomaly_btn = self.create_button(
            button_frame,
            "🌟 SCAN ANOMALY",
            self.scan_anomaly,
            width=30,
            style='normal'
        )
        anomaly_btn.pack(pady=20)

        # Help text
        tk.Label(
            action_content,
            text="Scan Area: Detect nearby resources and points of interest\nScan Anomaly: Investigate anomalies for research data and discoveries",
            font=('Arial', 10, 'italic'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium'],
            justify=tk.CENTER
        ).pack(pady=(0, 20))

    def show_travel_view(self):
        """Show travel/map view"""
        self.current_view = "travel"
        self.status_training_content = None  # Clear reference when leaving status view
        self.clear_content()

        # Reset map zoom/pan state
        self.map_zoom_level = 1.0
        self.map_pan_offset_x = 0.0
        self.map_pan_offset_y = 0.0

        # Create two-column layout for map and connections
        left_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # LEFT: Universe Map
        map_panel, map_content = self.create_panel(left_frame, "⭐ Universe Map")
        map_panel.pack(fill=tk.BOTH, expand=True)

        # Create line and ball map display
        self.draw_universe_map(map_content)

        # RIGHT: Video Player
        video_panel, video_content = self.create_panel(right_frame, "🚀 Warp Travel")
        video_panel.pack(fill=tk.BOTH, expand=True)

        # Video display label
        self.video_label = tk.Label(video_content, bg=COLORS['bg_dark'])
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Start video playback
        self.start_video_playback()

    def start_video_playback(self):
        """Start playing the warp travel video"""
        # Stop any existing video
        self.stop_video_playback()

        # Open video file
        self.video_cap = cv2.VideoCapture(self.video_path)
        if not self.video_cap.isOpened():
            print(f"Error: Could not open video file: {self.video_path}")
            return

        self.video_playing = True
        self.update_video_frame()

    def stop_video_playback(self):
        """Stop video playback and release resources"""
        self.video_playing = False
        if self.video_cap is not None:
            self.video_cap.release()
            self.video_cap = None

    def update_video_frame(self):
        """Update video frame in the label"""
        if not self.video_playing or self.video_cap is None:
            return

        ret, frame = self.video_cap.read()

        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame to fit the label while maintaining aspect ratio
            if self.video_label and self.video_label.winfo_exists():
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()

                if label_width > 1 and label_height > 1:  # Ensure label is rendered
                    # Calculate scaling to fit
                    frame_height, frame_width = frame_rgb.shape[:2]
                    scale = min(label_width / frame_width, label_height / frame_height)
                    new_width = int(frame_width * scale)
                    new_height = int(frame_height * scale)

                    # Resize frame
                    frame_resized = cv2.resize(frame_rgb, (new_width, new_height))

                    # Convert to PIL Image then to PhotoImage
                    img = Image.fromarray(frame_resized)
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Update label
                    self.video_label.imgtk = imgtk  # Keep reference to prevent garbage collection
                    self.video_label.configure(image=imgtk)

            # Schedule next frame (30 FPS = ~33ms delay)
            self.root.after(33, self.update_video_frame)
        else:
            # End of video - loop back to start
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.root.after(33, self.update_video_frame)

    def show_market_view(self, category='all'):
        """Show market/trading view with category filtering"""
        self.current_view = "market"
        self.current_market_category = category  # Store current category
        self.status_training_content = None  # Clear reference when leaving status view
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            tk.Label(
                self.content_frame,
                text="No market available at this location",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        market = self.engine.economy.get_market(self.engine.player.location)

        if not market:
            tk.Label(
                self.content_frame,
                text="Market data unavailable",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        # Left - Market listings
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        market_panel, market_content = self.create_panel(left_col, f"Market - {location_data['name']}")
        market_panel.pack(fill=tk.BOTH, expand=True)

        # Search bar
        search_frame = tk.Frame(market_content, bg=COLORS['bg_medium'])
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(
            search_frame,
            text="Search:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(side=tk.LEFT, padx=(5, 5))

        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            font=('Arial', 10),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text']
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Store reference for filtering
        self.market_search_var = search_var

        # Category filter buttons
        filter_frame = tk.Frame(market_content, bg=COLORS['bg_medium'])
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        categories = [
            ('All', 'all'),
            ('Raw Materials', 'raw'),
            ('Refined', 'refined'),
            ('Special', 'special'),
            ('Commodities', 'commodities')
        ]

        for label, cat in categories:
            style = 'success' if cat == category else 'normal'
            self.create_button(
                filter_frame,
                label,
                lambda c=cat: self.show_market_view(c),
                width=12,
                style=style
            ).pack(side=tk.LEFT, padx=2)

        # Scrollable market list
        canvas, scrollbar, scrollable_frame = self.create_scrollable_frame(market_content)

        # Get and filter listings
        from data import RESOURCES, COMMODITIES
        listings = []

        # Add resource listings (raw materials, refined, special)
        if category in ['all', 'raw', 'refined', 'special']:
            all_listings = market.get_market_listing()
            for listing in all_listings:
                res_id = listing['id']
                if res_id not in RESOURCES:
                    if category == 'all':
                        listings.append(listing)
                    continue

                res_data = RESOURCES[res_id]

                # Determine category
                if 'raw_' in res_id or res_data.get('refines_to'):
                    item_cat = 'raw'
                elif any(res_id in RESOURCES.get(r, {}).get('refines_to', '') for r in RESOURCES):
                    item_cat = 'refined'
                else:
                    item_cat = 'special'

                # Filter by category
                if category == 'all' or category == item_cat:
                    listings.append(listing)

        # Add commodity listings
        if category in ['all', 'commodities']:
            commodity_overview = self.engine.commodity_market.get_market_overview(self.engine.player.location)
            for comm_data in commodity_overview:
                comm_data_with_type = comm_data.copy()
                comm_data_with_type['type'] = 'commodity'
                listings.append(comm_data_with_type)

        # Store original listings for search filtering
        self.market_all_listings = listings
        self.market_scrollable_frame = scrollable_frame

        # Function to render filtered listings
        def render_market_listings(search_query=""):
            # Clear existing widgets
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Filter listings by search query
            search_lower = search_query.lower()
            filtered_listings = [
                listing for listing in listings
                if search_lower in listing['name'].lower() or search_lower in listing['id'].lower()
            ] if search_query else listings

            # Show count
            if search_query:
                count_label = tk.Label(
                    scrollable_frame,
                    text=f"Found {len(filtered_listings)} items",
                    font=('Arial', 9, 'italic'),
                    fg=COLORS['text_accent'],
                    bg=COLORS['bg_medium']
                )
                count_label.pack(anchor='w', padx=10, pady=5)

            # Render filtered listings
            for listing in filtered_listings:
                item_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                item_frame.pack(fill=tk.X, pady=3, padx=5)

                # Icon (left side)
                icon_frame = tk.Frame(item_frame, bg=COLORS['bg_light'])
                icon_frame.pack(side=tk.LEFT, padx=(10, 5), pady=8)

                # Get icon for this resource/commodity
                item_id = listing['id']
                rarity = listing.get('rarity', None)
                icon = self.icon_manager.get_icon('resource', item_id, size='medium', rarity=rarity)
                if icon:
                    icon_label = tk.Label(icon_frame, image=icon, bg=COLORS['bg_light'])
                    icon_label.image = icon  # Keep a reference
                    icon_label.pack()
                else:
                    # Fallback to text symbol
                    symbol = get_symbol('resource', item_id)
                    tk.Label(
                        icon_frame,
                        text=symbol,
                        font=('Arial', 16),
                        fg=COLORS['accent'],
                        bg=COLORS['bg_light']
                    ).pack()

                # Item info
                info = tk.Frame(item_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=8)

                tk.Label(
                    info,
                    text=listing['name'],
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    info,
                    text=f"Buy: {listing['buy_price']:,} CR | Sell: {listing['sell_price']:,} CR | Stock: {listing['stock']}",
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Buy/Sell buttons
                btn_frame = tk.Frame(item_frame, bg=COLORS['bg_light'])
                btn_frame.pack(side=tk.RIGHT, padx=10)

                # Determine if this is a commodity or resource
                is_commodity = listing.get('type') == 'commodity'

                if is_commodity:
                    self.create_button(
                        btn_frame,
                        "Buy",
                        lambda r=listing['id']: self.buy_commodity(r),
                        width=8,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)

                    self.create_button(
                        btn_frame,
                        "Sell",
                        lambda r=listing['id']: self.sell_commodity(r),
                        width=8,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)
                else:
                    self.create_button(
                        btn_frame,
                        "Buy",
                        lambda r=listing['id']: self.buy_resource(r),
                        width=8,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)

                    self.create_button(
                        btn_frame,
                        "Sell",
                        lambda r=listing['id']: self.sell_resource(r),
                        width=8,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)

        # Initial render with no search
        render_market_listings()

        # Bind search updates with debouncing
        def on_search_change(*args):
            # Use after_idle to debounce
            if hasattr(self, 'market_search_timer'):
                self.root.after_cancel(self.market_search_timer)
            self.market_search_timer = self.root.after(300, lambda: render_market_listings(search_var.get()))

        search_var.trace('w', on_search_change)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

        # Right - Inventory (Ship Cargo + Station Storage)
        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # SHIP CARGO Panel (Top Half)
        ship_panel, ship_content = self.create_panel(right_col, "🚀 Ship Cargo")
        ship_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Import all item types
        from data import MODULES, COMMODITIES, RESOURCES

        if self.engine.player.inventory:
            total_value = 0

            # Create scrollable frame for ship cargo
            ship_canvas = tk.Canvas(ship_content, bg=COLORS['bg_medium'], highlightthickness=0, height=200)
            ship_scrollbar = tk.Scrollbar(ship_content, orient="vertical", command=ship_canvas.yview)
            ship_scrollable = tk.Frame(ship_canvas, bg=COLORS['bg_medium'])

            ship_scrollable.bind(
                "<Configure>",
                lambda e: ship_canvas.configure(scrollregion=(0, 0, ship_canvas.winfo_width(), ship_scrollable.winfo_reqheight()))
            )

            ship_canvas.create_window((0, 0), window=ship_scrollable, anchor="nw")
            ship_canvas.configure(yscrollcommand=ship_scrollbar.set)
            self.bind_mousewheel(ship_canvas, ship_scrollable)

            for item_id, quantity in sorted(self.engine.player.inventory.items()):
                item_name = None
                item_value = 0
                item_type = None

                # Check if it's a resource
                if item_id in RESOURCES:
                    item_name = RESOURCES[item_id]['name']
                    item_value = RESOURCES[item_id]["base_price"] * quantity
                    item_type = "Resource"
                # Check if it's a commodity
                elif item_id in COMMODITIES:
                    item_name = COMMODITIES[item_id]['name']
                    item_value = COMMODITIES[item_id]["base_price"] * quantity
                    item_type = "Commodity"
                # Check if it's a module
                elif item_id in MODULES:
                    item_name = MODULES[item_id]['name']
                    item_value = MODULES[item_id].get("manufacturing_cost", 1000) * quantity
                    item_type = "Module"
                else:
                    # Unknown item
                    item_name = item_id
                    item_value = 0
                    item_type = "Unknown"

                total_value += item_value

                item_frame = tk.Frame(ship_scrollable, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                item_frame.pack(fill=tk.X, pady=3, padx=5)

                # Left side - name and quantity
                left_info = tk.Frame(item_frame, bg=COLORS['bg_light'])
                left_info.pack(side=tk.LEFT, padx=10, pady=5)

                tk.Label(
                    left_info,
                    text=f"{item_name}: {quantity}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    left_info,
                    text=f"[{item_type}]",
                    font=('Arial', 8),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Right side - value, buy and sell buttons
                right_frame = tk.Frame(item_frame, bg=COLORS['bg_light'])
                right_frame.pack(side=tk.RIGHT, padx=10, pady=5)

                tk.Label(
                    right_frame,
                    text=f"~{item_value:,} CR",
                    font=('Arial', 9),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT, padx=(0, 10))

                # Add buy and sell buttons for commodities and resources
                if item_id in COMMODITIES:
                    self.create_button(
                        right_frame,
                        "Buy",
                        lambda i=item_id: self.buy_commodity(i),
                        width=6,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)
                    self.create_button(
                        right_frame,
                        "Sell",
                        lambda i=item_id: self.sell_commodity(i),
                        width=6,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)
                elif item_id in RESOURCES:
                    self.create_button(
                        right_frame,
                        "Buy",
                        lambda i=item_id: self.buy_resource(i),
                        width=6,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)
                    self.create_button(
                        right_frame,
                        "Sell",
                        lambda i=item_id: self.sell_resource(i),
                        width=6,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)

            ship_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # ship_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

            # Total value
            tk.Label(
                ship_content,
                text=f"Total Value: {total_value:,} CR",
                font=('Arial', 10, 'bold'),
                fg=COLORS['success'],
                bg=COLORS['bg_medium']
            ).pack(pady=5)
        else:
            tk.Label(
                ship_content,
                text="Cargo hold is empty",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

        # STATION STORAGE Panel (Bottom Half)
        station_panel, station_content = self.create_panel(right_col, "🏪 Station Storage")
        station_panel.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        station_inventory = self.engine.player.get_station_inventory(self.engine.player.location)

        if station_inventory:
            total_station_value = 0

            # Create scrollable frame for station storage
            station_canvas = tk.Canvas(station_content, bg=COLORS['bg_medium'], highlightthickness=0, height=200)
            station_scrollbar = tk.Scrollbar(station_content, orient="vertical", command=station_canvas.yview)
            station_scrollable = tk.Frame(station_canvas, bg=COLORS['bg_medium'])

            station_scrollable.bind(
                "<Configure>",
                lambda e: station_canvas.configure(scrollregion=(0, 0, station_canvas.winfo_width(), station_scrollable.winfo_reqheight()))
            )

            station_canvas.create_window((0, 0), window=station_scrollable, anchor="nw")
            station_canvas.configure(yscrollcommand=station_scrollbar.set)
            self.bind_mousewheel(station_canvas, station_scrollable)

            for item_id, quantity in sorted(station_inventory.items()):
                item_name = None
                item_value = 0
                item_type = None

                # Check if it's a resource
                if item_id in RESOURCES:
                    item_name = RESOURCES[item_id]['name']
                    item_value = RESOURCES[item_id]["base_price"] * quantity
                    item_type = "Resource"
                # Check if it's a commodity
                elif item_id in COMMODITIES:
                    item_name = COMMODITIES[item_id]['name']
                    item_value = COMMODITIES[item_id]["base_price"] * quantity
                    item_type = "Commodity"
                # Check if it's a module
                elif item_id in MODULES:
                    item_name = MODULES[item_id]['name']
                    item_value = MODULES[item_id].get("manufacturing_cost", 1000) * quantity
                    item_type = "Module"
                else:
                    # Unknown item
                    item_name = item_id
                    item_value = 0
                    item_type = "Unknown"

                total_station_value += item_value

                item_frame = tk.Frame(station_scrollable, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                item_frame.pack(fill=tk.X, pady=3, padx=5)

                # Left side - name and quantity
                left_info = tk.Frame(item_frame, bg=COLORS['bg_light'])
                left_info.pack(side=tk.LEFT, padx=10, pady=5)

                tk.Label(
                    left_info,
                    text=f"{item_name}: {quantity}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    left_info,
                    text=f"[{item_type}]",
                    font=('Arial', 8),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Right side - value, buy, sell, and load buttons
                right_frame = tk.Frame(item_frame, bg=COLORS['bg_light'])
                right_frame.pack(side=tk.RIGHT, padx=10, pady=5)

                tk.Label(
                    right_frame,
                    text=f"~{item_value:,} CR",
                    font=('Arial', 9),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT, padx=(0, 10))

                # Add buy and sell buttons for commodities and resources
                if item_id in COMMODITIES:
                    self.create_button(
                        right_frame,
                        "Buy",
                        lambda i=item_id: self.buy_commodity(i),
                        width=6,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)
                    self.create_button(
                        right_frame,
                        "Sell",
                        lambda i=item_id: self.sell_commodity(i),
                        width=6,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)
                elif item_id in RESOURCES:
                    self.create_button(
                        right_frame,
                        "Buy",
                        lambda i=item_id: self.buy_resource(i),
                        width=6,
                        style='success'
                    ).pack(side=tk.LEFT, padx=2)
                    self.create_button(
                        right_frame,
                        "Sell",
                        lambda i=item_id: self.sell_resource(i),
                        width=6,
                        style='warning'
                    ).pack(side=tk.LEFT, padx=2)

                # Add load button to transfer from station to ship
                self.create_button(
                    right_frame,
                    "Load",
                    lambda i=item_id: self.load_from_station(i),
                    width=6,
                    style='info'
                ).pack(side=tk.LEFT, padx=2)

            station_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # station_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

            # Total value
            tk.Label(
                station_content,
                text=f"Total Value: {total_station_value:,} CR",
                font=('Arial', 10, 'bold'),
                fg=COLORS['success'],
                bg=COLORS['bg_medium']
            ).pack(pady=5)
        else:
            tk.Label(
                station_content,
                text="No items in station storage",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

    def show_contracts_view(self):
        """Show contracts view"""
        self.current_view = "contracts"
        self.status_training_content = None  # Clear reference when leaving status view
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        # DELIVER CARGO BUTTON - Always shown at top
        action_panel, action_content = self.create_panel(self.content_frame, "⚡ CONTRACT ACTIONS")
        action_panel.pack(fill=tk.X, pady=(0, 10), padx=10)

        button_container = tk.Frame(action_content, bg=COLORS['bg_medium'])
        button_container.pack(pady=15, padx=20)

        deliver_btn = self.create_button(
            button_container,
            "📦 DELIVER CARGO",
            self.deliver_cargo,
            width=25,
            style='success'
        )
        deliver_btn.pack(padx=10, pady=5)

        tk.Label(
            action_content,
            text="Complete active transport contracts by delivering cargo",
            font=('Arial', 10, 'italic'),
            fg=COLORS['text_accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=(0, 10))

        if "contracts" not in location_data.get("services", []):
            tk.Label(
                self.content_frame,
                text="No contracts available at this location",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        # Get contracts for current location (generates if needed)
        available_contracts = self.engine.contract_board.get_available_contracts(self.engine.player.location)

        panel, content = self.create_panel(self.content_frame, "Available Contracts")
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable contracts list
        canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind canvas width changes to update scrollable frame width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        for contract in available_contracts:
            contract_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
            contract_frame.pack(fill=tk.X, pady=10, padx=10)

            # Header
            header = tk.Frame(contract_frame, bg=COLORS['bg_light'])
            header.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(
                header,
                text=contract.name,
                font=('Arial', 13, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(side=tk.LEFT)

            difficulty_colors = ['#4caf50', '#ff9800', '#f44336']
            diff_color = difficulty_colors[min(contract.difficulty - 1, 2)]

            tk.Label(
                header,
                text=f"Difficulty: {'★' * contract.difficulty}",
                font=('Arial', 10),
                fg=diff_color,
                bg=COLORS['bg_light']
            ).pack(side=tk.RIGHT)

            # Description
            desc_label = tk.Label(
                contract_frame,
                text=contract.description,
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_light'],
                justify=tk.LEFT
            )
            desc_label.pack(anchor='w', fill=tk.X, padx=15, pady=5)

            # Update wraplength dynamically
            def update_wraplength(event, label=desc_label):
                label.configure(wraplength=event.width - 30)
            contract_frame.bind('<Configure>', update_wraplength)

            # Objective
            tk.Label(
                contract_frame,
                text=f"Objective: {contract.get_progress_text()}",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(anchor='w', padx=15, pady=5)

            # Footer
            footer = tk.Frame(contract_frame, bg=COLORS['bg_light'])
            footer.pack(fill=tk.X, padx=15, pady=10)

            tk.Label(
                footer,
                text=f"Reward: {contract.reward:,} CR",
                font=('Arial', 11, 'bold'),
                fg=COLORS['success'],
                bg=COLORS['bg_light']
            ).pack(side=tk.LEFT)

            tk.Label(
                footer,
                text=f"Time Limit: {contract.time_limit // 60} minutes",
                font=('Arial', 9),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(side=tk.LEFT, padx=20)

            self.create_button(
                footer,
                "Accept Contract",
                lambda c=contract: self.accept_contract(c),
                width=15,
                style='success'
            ).pack(side=tk.RIGHT)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

    def show_skills_view(self, filter_category='all'):
        """Show skills view with category filtering"""
        self.current_view = "skills"
        self.status_training_content = None  # Clear reference when leaving status view
        self.clear_content()

        panel, content = self.create_panel(self.content_frame, "Skills & Training")
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Current training status at the top
        training_progress = self.engine.player.get_training_progress()
        if training_progress:
            training_frame = tk.Frame(content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
            training_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(
                training_frame,
                text=f"⚡ CURRENTLY TRAINING ({len(training_progress)}/{self.engine.player.get_max_training_slots()} slots)",
                font=('Arial', 11, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(anchor='w', padx=10, pady=(5, 2))

            for progress in training_progress:
                skill_row = tk.Frame(training_frame, bg=COLORS['bg_light'])
                skill_row.pack(fill=tk.X, padx=15, pady=3)

                # Skill name and level
                name_label = tk.Label(
                    skill_row,
                    text=f"{progress['skill_name']} → Level {progress['target_level']}",
                    font=('Arial', 10),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light'],
                    width=30,
                    anchor='w'
                )
                name_label.pack(side=tk.LEFT)

                # Progress bar
                progress_frame = tk.Frame(skill_row, bg=COLORS['bg_dark'], width=200, height=12)
                progress_frame.pack(side=tk.LEFT, padx=5)
                progress_frame.pack_propagate(False)

                progress_width = int((progress['progress'] / 100) * 200)
                if progress_width > 0:
                    progress_bar = tk.Frame(progress_frame, bg=COLORS['accent'], width=progress_width, height=12)
                    progress_bar.pack(side=tk.LEFT)

                # Timer
                time_label = tk.Label(
                    skill_row,
                    text=f"{progress['progress']:.1f}% - {int(progress['remaining_seconds'])}s",
                    font=('Arial', 9),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                )
                time_label.pack(side=tk.LEFT, padx=5)

        # Organize skills by category
        skills_by_category = {}
        all_categories = set()
        for skill_id, level in self.engine.player.skills.items():
            skill_data = SKILLS[skill_id]
            category = skill_data["category"]
            all_categories.add(category)

            if category not in skills_by_category:
                skills_by_category[category] = []

            skills_by_category[category].append((skill_id, skill_data, level))

        # Category filter buttons
        filter_frame = tk.Frame(content, bg=COLORS['bg_medium'])
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create filter buttons
        filter_buttons = [('All', 'all')]
        for cat in sorted(all_categories):
            cat_label = cat.replace('_', ' ').title()
            filter_buttons.append((cat_label, cat))

        for label, cat in filter_buttons:
            style = 'success' if cat == filter_category else 'normal'
            self.create_button(
                filter_frame,
                label,
                lambda c=cat: self.show_skills_view(c),
                width=10,
                style=style
            ).pack(side=tk.LEFT, padx=2)

        # Create scrollable content
        canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind canvas width changes to update scrollable frame width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        # Filter and display categories
        categories_to_show = sorted(skills_by_category.items()) if filter_category == 'all' else \
                            [(filter_category, skills_by_category[filter_category])] if filter_category in skills_by_category else []

        for category, skills in categories_to_show:
            # Category header
            cat_header = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], height=40)
            cat_header.pack(fill=tk.X, pady=5, padx=10)

            tk.Label(
                cat_header,
                text=category.upper().replace('_', ' '),
                font=('Arial', 12, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(side=tk.LEFT, padx=15, pady=8)

            # Skills in category
            for skill_id, skill_data, level in skills:
                # Check if this skill is currently training
                training = self.engine.player.get_training_progress(skill_id)
                is_training = training is not None

                skill_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                skill_frame.pack(fill=tk.X, pady=3, padx=20)

                # Skill info
                info = tk.Frame(skill_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                # Skill name with training indicator
                name_text = skill_data['name']
                if is_training:
                    name_text += " ⚡ TRAINING"

                tk.Label(
                    info,
                    text=name_text,
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'] if is_training else COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    info,
                    text=skill_data['description'],
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light'],
                    wraplength=500
                ).pack(anchor='w', pady=2)

                # Progress bar
                progress_frame = tk.Frame(info, bg=COLORS['bg_dark'], width=200, height=15)
                progress_frame.pack(anchor='w', pady=5)
                progress_frame.pack_propagate(False)

                progress_width = int((level / skill_data['max_level']) * 200)
                if progress_width > 0:
                    progress_bar = tk.Frame(progress_frame, bg=COLORS['success'], width=progress_width, height=15)
                    progress_bar.pack(side=tk.LEFT)

                # Level display with training progress
                level_text = f"Level {level}/{skill_data['max_level']}"
                if is_training:
                    level_text += f" → {training['target_level']} ({training['progress']:.1f}% - {int(training['remaining_seconds'])}s)"

                tk.Label(
                    info,
                    text=level_text,
                    font=('Arial', 9),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Train button
                btn_frame = tk.Frame(skill_frame, bg=COLORS['bg_light'])
                btn_frame.pack(side=tk.RIGHT, padx=10)

                if is_training:
                    tk.Label(
                        btn_frame,
                        text="TRAINING...",
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['accent'],
                        bg=COLORS['bg_light']
                    ).pack()
                elif level < skill_data['max_level']:
                    self.create_button(
                        btn_frame,
                        "Train",
                        lambda s=skill_id: self.train_skill(s),
                        width=10,
                        style='success'
                    ).pack()
                else:
                    tk.Label(
                        btn_frame,
                        text="MAX",
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['success'],
                        bg=COLORS['bg_light']
                    ).pack()

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

    def show_vessel_view(self):
        """Show vessel info and modules"""
        self.current_view = "vessel"
        self.status_training_content = None  # Clear reference when leaving status view
        self.clear_content()

        vessel = self.engine.vessel

        # Left - Vessel status
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        status_panel, status_content = self.create_panel(left_col, f"Vessel: {vessel.name}")
        status_panel.pack(fill=tk.X, pady=5)

        stats = [
            ("Class", vessel.class_name),
            ("Type", vessel.class_type.upper()),
            ("", ""),
            ("Hull HP", f"{vessel.current_hull_hp:.0f} / {vessel.max_hull_hp:.0f}"),
            ("Hull %", f"{vessel.get_hull_percentage():.1f}%"),
            ("Shields", f"{vessel.current_shields:.0f} / {vessel.get_total_shield_capacity():.0f}"),
            ("Shield %", f"{vessel.get_shield_percentage():.1f}%"),
            ("Armor Rating", f"{vessel.get_total_armor():.0f}"),
            ("", ""),
            ("Speed", f"{vessel.get_effective_speed():.0f}"),
            ("Cargo Capacity", f"{vessel.cargo_capacity:.0f}"),
            ("Weapon Damage", f"{vessel.get_total_weapon_damage():.0f}"),
        ]

        for label, value in stats:
            if not label:
                tk.Frame(status_content, bg=COLORS['bg_medium'], height=10).pack()
                continue

            row = tk.Frame(status_content, bg=COLORS['bg_medium'])
            row.pack(fill=tk.X, pady=3)

            tk.Label(
                row,
                text=f"{label}:",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium'],
                width=18,
                anchor='w'
            ).pack(side=tk.LEFT, padx=10)

            tk.Label(
                row,
                text=str(value),
                font=('Arial', 10, 'bold'),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                anchor='w'
            ).pack(side=tk.LEFT)

        # Right - Installed modules
        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        modules_panel, modules_content = self.create_panel(right_col, "Installed Modules")
        modules_panel.pack(fill=tk.BOTH, expand=True, pady=5)

        for mod_type, modules in vessel.installed_modules.items():
            type_frame = tk.Frame(modules_content, bg=COLORS['bg_medium'])
            type_frame.pack(fill=tk.X, pady=5)

            slots_used = len(modules)
            slots_max = vessel.module_slots[mod_type]

            tk.Label(
                type_frame,
                text=f"{mod_type.upper()} ({slots_used}/{slots_max}):",
                font=('Arial', 11, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_medium']
            ).pack(anchor='w', padx=10, pady=5)

            if modules:
                for mod_id in modules:
                    module_data = MODULES[mod_id]

                    mod_frame = tk.Frame(type_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                    mod_frame.pack(fill=tk.X, pady=2, padx=20)

                    tk.Label(
                        mod_frame,
                        text=module_data['name'],
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', padx=10, pady=5)

                    tk.Label(
                        mod_frame,
                        text=module_data['description'],
                        font=('Arial', 9),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', padx=10, pady=2)
            else:
                tk.Label(
                    type_frame,
                    text="  No modules installed",
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_medium']
                ).pack(anchor='w', padx=30)

    def show_shipyard_view(self):
        """Show shipyard - ship construction blueprints - REORGANIZED WITH REPAIR FIRST"""
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        # Create scrollable container for entire shipyard view
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

        # Info message
        info_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        tk.Label(
            info_frame,
            text="ℹ️ Buy pre-built ships (expensive) or manufacture from components (cheaper). Manufacturing > Ships.",
            font=('Arial', 10),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10, padx=10)

        # Check if shipyard is available at this location
        has_shipyard = "shipyard" in location_data.get("services", [])

        # ===== 🔧 REPAIR PANEL - ALWAYS SHOWN FIRST (TOP PRIORITY) =====
        if has_shipyard:
            repair_panel, repair_content = self.create_panel(scrollable_frame, "🔧 Vessel Repair & Maintenance")
            repair_panel.pack(fill=tk.X, pady=(0, 10))

            repair_info = self.engine.get_repair_cost()

            # Current vessel status
            vessel_status_frame = tk.Frame(repair_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
            vessel_status_frame.pack(fill=tk.X, padx=10, pady=10)

            status_left = tk.Frame(vessel_status_frame, bg=COLORS['bg_light'])
            status_left.pack(side=tk.LEFT, padx=15, pady=10)

            tk.Label(
                status_left,
                text=f"Current Vessel: {self.engine.vessel.name}",
                font=('Arial', 12, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(anchor='w', pady=2)

            # Hull status
            hull_pct = self.engine.vessel.get_hull_percentage()
            hull_color = COLORS['success'] if hull_pct >= 75 else (COLORS['warning'] if hull_pct >= 40 else COLORS['danger'])
            tk.Label(
                status_left,
                text=f"Hull: {self.engine.vessel.current_hull_hp:.0f}/{self.engine.vessel.max_hull_hp:.0f} ({hull_pct:.1f}%)",
                font=('Arial', 10),
                fg=hull_color,
                bg=COLORS['bg_light']
            ).pack(anchor='w', pady=2)

            # Shield status
            shield_pct = self.engine.vessel.get_shield_percentage()
            shield_color = COLORS['success'] if shield_pct >= 75 else (COLORS['warning'] if shield_pct >= 40 else COLORS['danger'])
            tk.Label(
                status_left,
                text=f"Shields: {self.engine.vessel.current_shields:.0f}/{self.engine.vessel.get_total_shield_capacity():.0f} ({shield_pct:.1f}%)",
                font=('Arial', 10),
                fg=shield_color,
                bg=COLORS['bg_light']
            ).pack(anchor='w', pady=2)

            # Repair costs
            status_right = tk.Frame(vessel_status_frame, bg=COLORS['bg_light'])
            status_right.pack(side=tk.RIGHT, padx=15, pady=10)

            if repair_info['hull_damage'] > 0 or repair_info['shield_damage'] > 0:
                tk.Label(
                    status_right,
                    text="Repair Costs:",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=2)

                if repair_info['hull_damage'] > 0:
                    tk.Label(
                        status_right,
                        text=f"Hull: {repair_info['hull_cost']:,} CR",
                        font=('Arial', 9),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=1)

                if repair_info['shield_damage'] > 0:
                    tk.Label(
                        status_right,
                        text=f"Shields: {repair_info['shield_cost']:,} CR",
                        font=('Arial', 9),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=1)

                tk.Label(
                    status_right,
                    text=f"Total: {repair_info['total_cost']:,} CR",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=5)

                # Repair buttons
                button_frame = tk.Frame(status_right, bg=COLORS['bg_light'])
                button_frame.pack(pady=5)

                self.create_button(
                    button_frame,
                    "Repair All",
                    lambda: self.repair_vessel_action(True, True),
                    width=12,
                    style='success'
                ).pack(side=tk.LEFT, padx=3)

                if repair_info['hull_damage'] > 0:
                    self.create_button(
                        button_frame,
                        "Hull Only",
                        lambda: self.repair_vessel_action(True, False),
                        width=12,
                        style='info'
                    ).pack(side=tk.LEFT, padx=3)

                if repair_info['shield_damage'] > 0:
                    self.create_button(
                        button_frame,
                        "Shields Only",
                        lambda: self.repair_vessel_action(False, True),
                        width=12,
                        style='info'
                    ).pack(side=tk.LEFT, padx=3)
            else:
                tk.Label(
                    status_right,
                    text="✓ Vessel at full condition",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(pady=10)

        # ===== EXPANDABLE SECTIONS - BEHIND BUTTONS =====
        # Create expand/collapse function generator
        def create_toggle_section(parent, title, build_content_func):
            """Creates an expandable section with a toggle button"""
            # Container for the whole section
            section_container = tk.Frame(parent, bg=COLORS['bg_dark'])
            section_container.pack(fill=tk.X, pady=(0, 10))
            
            # State tracker
            is_expanded = [False]
            content_frame_holder = [None]  # To store the content frame
            
            # Header button
            header_frame = tk.Frame(section_container, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=2)
            header_frame.pack(fill=tk.X)
            
            def toggle():
                is_expanded[0] = not is_expanded[0]
                if is_expanded[0]:
                    # Show content
                    arrow_label.config(text="▼")
                    if content_frame_holder[0] is None:
                        content_frame_holder[0] = tk.Frame(section_container, bg=COLORS['bg_dark'])
                        content_frame_holder[0].pack(fill=tk.BOTH, expand=True)
                        build_content_func(content_frame_holder[0])
                    else:
                        content_frame_holder[0].pack(fill=tk.BOTH, expand=True)
                else:
                    # Hide content
                    arrow_label.config(text="▶")
                    if content_frame_holder[0]:
                        content_frame_holder[0].pack_forget()
            
            # Header content
            header_content = tk.Frame(header_frame, bg=COLORS['bg_medium'])
            header_content.pack(fill=tk.X, pady=10, padx=10)
            
            arrow_label = tk.Label(
                header_content,
                text="▶",
                font=('Arial', 12, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_medium']
            )
            arrow_label.pack(side=tk.LEFT, padx=(0, 10))
            
            title_label = tk.Label(
                header_content,
                text=title,
                font=('Arial', 12, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_medium']
            )
            title_label.pack(side=tk.LEFT)
            
            # Make the whole header clickable
            for widget in [header_frame, header_content, arrow_label, title_label]:
                widget.bind('<Button-1>', lambda e: toggle())
                widget.config(cursor='hand2')
            
            return section_container

        # ===== 🏠 BERTH MANAGEMENT - EXPANDABLE =====
        if has_shipyard:
            def build_berth_content(parent_frame):
                berth_content = parent_frame
                
                berth_overview = self.engine.berth_manager.get_berth_overview(self.engine.player.location)

                # Header with berth stats
                header_frame = tk.Frame(berth_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

                berth_status_text = f"Berths at this location: {berth_overview['used']}/{berth_overview['total']} occupied"
                if berth_overview['total'] < berth_overview['max_berths']:
                    berth_status_text += f" | Can purchase up to {berth_overview['max_berths']} total"

                tk.Label(
                    header_frame,
                    text=berth_status_text,
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(pady=8)

                # Get current ship ID
                current_ship_id = self.engine.vessel.vessel_class_id

                # Show all berths (including empty ones)
                all_berths = berth_overview['berths']  # List of ship_ids or None

                if all_berths:
                    # Display each berth
                    for berth_idx, ship_id in enumerate(all_berths):
                        berth_num = berth_idx + 1
                        is_current_ship = (ship_id == current_ship_id)

                        # Create berth card
                        berth_frame = tk.Frame(berth_content, bg=COLORS['bg_medium'])
                        berth_frame.pack(fill=tk.X, padx=10, pady=5)

                        # Berth header
                        berth_header_bg = COLORS['success'] if is_current_ship else COLORS['bg_light']
                        berth_header = tk.Frame(berth_frame, bg=berth_header_bg, relief=tk.RIDGE, bd=2)
                        berth_header.pack(fill=tk.X)

                        header_text = f"🏠 BERTH #{berth_num}"
                        if is_current_ship:
                            header_text += " ⭐ (CURRENTLY PILOTING)"
                        elif ship_id is None:
                            header_text += " - EMPTY"

                        tk.Label(
                            berth_header,
                            text=header_text,
                            font=('Arial', 10, 'bold'),
                            fg=COLORS['text'] if is_current_ship else COLORS['accent'],
                            bg=berth_header_bg
                        ).pack(anchor='w', padx=10, pady=8)

                        # Berth content
                        if ship_id and ship_id in VESSEL_CLASSES:
                            ship_data = VESSEL_CLASSES[ship_id]

                            ship_card = tk.Frame(berth_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                            ship_card.pack(fill=tk.X, padx=2, pady=2)

                            # Left side - ship info
                            left_frame = tk.Frame(ship_card, bg=COLORS['bg_light'])
                            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

                            # Ship name
                            tk.Label(
                                left_frame,
                                text=ship_data['name'],
                                font=('Arial', 11, 'bold'),
                                fg=COLORS['accent'],
                                bg=COLORS['bg_light']
                            ).pack(anchor='w')

                            # Ship class and tier
                            tk.Label(
                                left_frame,
                                text=f"{ship_data['class_type'].title()} | Tier {ship_data['tier_num']} | Level {ship_data['level_requirement']}+",
                                font=('Arial', 9),
                                fg=COLORS['text_dim'],
                                bg=COLORS['bg_light']
                            ).pack(anchor='w', pady=(2, 5))

                            # Stats in compact format
                            stats_text = f"Hull: {ship_data['hull_hp']:,} | Shield: {ship_data['shield_capacity']:,} | Speed: {ship_data['base_speed']} | Cargo: {ship_data['cargo_capacity']:,}"
                            tk.Label(
                                left_frame,
                                text=stats_text,
                                font=('Arial', 9),
                                fg=COLORS['text'],
                                bg=COLORS['bg_light']
                            ).pack(anchor='w')

                            # Module slots
                            slots = ship_data['module_slots']
                            slots_text = f"Slots: W:{slots['weapon']} D:{slots['defense']} U:{slots['utility']} E:{slots['engine']}"
                            tk.Label(
                                left_frame,
                                text=slots_text,
                                font=('Arial', 9),
                                fg=COLORS['text_dim'],
                                bg=COLORS['bg_light']
                            ).pack(anchor='w', pady=(2, 0))

                            # Right side - actions
                            right_frame = tk.Frame(ship_card, bg=COLORS['bg_light'])
                            right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

                            if not is_current_ship:
                                self.create_button(
                                    right_frame,
                                    "Pilot Ship",
                                    lambda s=ship_id: self.switch_ship_action(s),
                                    width=12,
                                    style='info'
                                ).pack()
                        else:
                            # Empty berth
                            empty_frame = tk.Frame(berth_frame, bg=COLORS['bg_dark'], relief=tk.SUNKEN, bd=1)
                            empty_frame.pack(fill=tk.X, padx=2, pady=2)

                            tk.Label(
                                empty_frame,
                                text="[ Empty Berth - Available for Ship Storage ]",
                                font=('Arial', 10, 'italic'),
                                fg=COLORS['text_dim'],
                                bg=COLORS['bg_dark']
                            ).pack(pady=30)
                else:
                    tk.Label(
                        berth_content,
                        text="No berths owned at this location. Purchase berths below to store ships.",
                        font=('Arial', 10),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_medium']
                    ).pack(pady=20)

            create_toggle_section(scrollable_frame, "🏠 Berth Management & Fleet", build_berth_content)

        # ===== ⚙️ MODULE MANAGEMENT - EXPANDABLE =====
        if has_shipyard:
            def build_modules_content(parent_frame):
                modules_content = parent_frame
                
                # Current ship info header
                ship_info_frame = tk.Frame(modules_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                ship_info_frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(
                    ship_info_frame,
                    text=f"Configuring: {self.engine.vessel.name}",
                    font=('Arial', 12, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(pady=5)

                # Module slot summary
                vessel = self.engine.vessel
                slots_text = f"Weapon: {len(vessel.installed_modules['weapon'])}/{vessel.module_slots['weapon']} | " \
                            f"Defense: {len(vessel.installed_modules['defense'])}/{vessel.module_slots['defense']} | " \
                            f"Utility: {len(vessel.installed_modules['utility'])}/{vessel.module_slots['utility']} | " \
                            f"Engine: {len(vessel.installed_modules['engine'])}/{vessel.module_slots['engine']}"
                tk.Label(
                    ship_info_frame,
                    text=slots_text,
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(pady=5)

                # Two-column layout: Installed modules | Available modules
                columns_frame = tk.Frame(modules_content, bg=COLORS['bg_medium'])
                columns_frame.pack(fill=tk.X, padx=10, pady=5)

                # Left column: Installed modules
                installed_frame = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
                installed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

                tk.Label(
                    installed_frame,
                    text="📦 Installed Modules",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_medium']
                ).pack(pady=5)

                # Scrollable installed modules list
                installed_canvas = tk.Canvas(installed_frame, bg=COLORS['bg_medium'], highlightthickness=0, height=250)
                installed_scrollbar = tk.Scrollbar(installed_frame, orient="vertical", command=installed_canvas.yview)
                installed_scrollable = tk.Frame(installed_canvas, bg=COLORS['bg_medium'])

                installed_scrollable.bind(
                    "<Configure>",
                    lambda e: installed_canvas.configure(scrollregion=(0, 0, installed_canvas.winfo_width(), installed_scrollable.winfo_reqheight()))
                )

                installed_canvas_window = installed_canvas.create_window((0, 0), window=installed_scrollable, anchor="nw")

                # Make scrollable frame expand to canvas width
                def on_installed_canvas_configure(event):
                    installed_canvas.itemconfig(installed_canvas_window, width=event.width)
                installed_canvas.bind('<Configure>', on_installed_canvas_configure)

                installed_canvas.configure(yscrollcommand=installed_scrollbar.set)
                self.bind_mousewheel(installed_canvas, installed_scrollable)

                # Display installed modules by type
                has_modules = False
                for module_type in ['weapon', 'defense', 'utility', 'engine']:
                    installed = vessel.installed_modules[module_type]
                    if installed:
                        has_modules = True
                        type_header = tk.Label(
                            installed_scrollable,
                            text=f"▸ {module_type.title()}",
                            font=('Arial', 10, 'bold'),
                            fg=COLORS['text_accent'],
                            bg=COLORS['bg_medium']
                        )
                        type_header.pack(anchor='w', padx=5, pady=(5, 2))

                        for module_id in installed:
                            if module_id in MODULES:
                                module_data = MODULES[module_id]

                                module_frame = tk.Frame(installed_scrollable, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                                module_frame.pack(fill=tk.X, padx=5, pady=2)

                                # Remove button (right side)
                                self.create_button(
                                    module_frame,
                                    "Remove",
                                    lambda m=module_id, t=module_type: self.remove_module_action(m, t),
                                    width=10,
                                    style='danger'
                                ).pack(side=tk.RIGHT, padx=5, pady=5)

                                # Info frame (fills remaining space)
                                info_frame = tk.Frame(module_frame, bg=COLORS['bg_light'])
                                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

                                tk.Label(
                                    info_frame,
                                    text=module_data['name'],
                                    font=('Arial', 9, 'bold'),
                                    fg=COLORS['text'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                                # Show module specs using helper function
                                specs_text = format_module_specs(module_data)
                                tk.Label(
                                    info_frame,
                                    text=specs_text,
                                    font=('Arial', 8),
                                    fg=COLORS['text_dim'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                if not has_modules:
                    tk.Label(
                        installed_scrollable,
                        text="No modules installed",
                        font=('Arial', 10),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_medium']
                    ).pack(pady=20)

                installed_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                # installed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

                # Right column: Available modules (in inventory)
                available_frame = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
                available_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

                tk.Label(
                    available_frame,
                    text="🎒 Available Modules (In Inventory)",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_medium']
                ).pack(pady=5)

                # Scrollable available modules list
                available_canvas = tk.Canvas(available_frame, bg=COLORS['bg_medium'], highlightthickness=0, height=250)
                available_scrollbar = tk.Scrollbar(available_frame, orient="vertical", command=available_canvas.yview)
                available_scrollable = tk.Frame(available_canvas, bg=COLORS['bg_medium'])

                available_scrollable.bind(
                    "<Configure>",
                    lambda e: available_canvas.configure(scrollregion=(0, 0, available_canvas.winfo_width(), available_scrollable.winfo_reqheight()))
                )

                available_canvas_window = available_canvas.create_window((0, 0), window=available_scrollable, anchor="nw")

                # Make scrollable frame expand to canvas width
                def on_available_canvas_configure(event):
                    available_canvas.itemconfig(available_canvas_window, width=event.width)
                available_canvas.bind('<Configure>', on_available_canvas_configure)

                available_canvas.configure(yscrollcommand=available_scrollbar.set)
                self.bind_mousewheel(available_canvas, available_scrollable)

                # Get modules from player inventory
                available_modules = {}
                for item_id, quantity in self.engine.player.ship_cargo.items():
                    if item_id in MODULES:
                        module_data = MODULES[item_id]
                        module_type = module_data['type']
                        if module_type not in available_modules:
                            available_modules[module_type] = []
                        available_modules[module_type].append((item_id, module_data, quantity))

                if available_modules:
                    for module_type in ['weapon', 'defense', 'utility', 'engine']:
                        if module_type in available_modules:
                            type_header = tk.Label(
                                available_scrollable,
                                text=f"▸ {module_type.title()}",
                                font=('Arial', 10, 'bold'),
                                fg=COLORS['text_accent'],
                                bg=COLORS['bg_medium']
                            )
                            type_header.pack(anchor='w', padx=5, pady=(5, 2))

                            for module_id, module_data, quantity in available_modules[module_type]:
                                module_frame = tk.Frame(available_scrollable, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                                module_frame.pack(fill=tk.X, padx=5, pady=2)

                                # Check if slots available
                                current_count = len(vessel.installed_modules[module_type])
                                max_slots = vessel.module_slots[module_type]
                                can_install = current_count < max_slots

                                # Install button (right side)
                                if can_install:
                                    self.create_button(
                                        module_frame,
                                        "Install",
                                        lambda m=module_id: self.install_module_action(m),
                                        width=10,
                                        style='success'
                                    ).pack(side=tk.RIGHT, padx=5, pady=5)
                                else:
                                    tk.Label(
                                        module_frame,
                                        text="No Slots",
                                        font=('Arial', 8),
                                        fg=COLORS['danger'],
                                        bg=COLORS['bg_light'],
                                        width=10
                                    ).pack(side=tk.RIGHT, padx=5, pady=5)

                                # Info frame (fills remaining space)
                                info_frame = tk.Frame(module_frame, bg=COLORS['bg_light'])
                                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

                                tk.Label(
                                    info_frame,
                                    text=f"{module_data['name']} (x{quantity})",
                                    font=('Arial', 9, 'bold'),
                                    fg=COLORS['text'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                                # Show module specs using helper function
                                specs_text = format_module_specs(module_data)
                                tk.Label(
                                    info_frame,
                                    text=specs_text,
                                    font=('Arial', 8),
                                    fg=COLORS['text_dim'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                else:
                    tk.Label(
                        available_scrollable,
                        text="No modules in inventory\n\nPurchase modules from the Module Market",
                        font=('Arial', 10),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_medium'],
                        justify=tk.CENTER
                    ).pack(pady=20)

                available_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                # available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

                # Bottom row: Station inventory
                station_frame = tk.Frame(modules_content, bg=COLORS['bg_medium'])
                station_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

                tk.Label(
                    station_frame,
                    text="🏢 Station Storage Modules",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_medium']
                ).pack(pady=5)

                # Scrollable station modules list
                station_canvas = tk.Canvas(station_frame, bg=COLORS['bg_medium'], highlightthickness=0, height=200)
                station_scrollbar = tk.Scrollbar(station_frame, orient="vertical", command=station_canvas.yview)
                station_scrollable = tk.Frame(station_canvas, bg=COLORS['bg_medium'])

                station_scrollable.bind(
                    "<Configure>",
                    lambda e: station_canvas.configure(scrollregion=(0, 0, station_canvas.winfo_width(), station_scrollable.winfo_reqheight()))
                )

                station_canvas_window = station_canvas.create_window((0, 0), window=station_scrollable, anchor="nw")

                # Make scrollable frame expand to canvas width
                def on_station_canvas_configure(event):
                    station_canvas.itemconfig(station_canvas_window, width=event.width)
                station_canvas.bind('<Configure>', on_station_canvas_configure)

                station_canvas.configure(yscrollcommand=station_scrollbar.set)
                self.bind_mousewheel(station_canvas, station_scrollable)

                # Get modules from station inventory
                current_location = self.engine.player.location
                station_inventory = self.engine.player.station_inventories.get(current_location, {})
                station_modules = {}
                
                for item_id, quantity in station_inventory.items():
                    if item_id in MODULES:
                        module_data = MODULES[item_id]
                        module_type = module_data['type']
                        if module_type not in station_modules:
                            station_modules[module_type] = []
                        station_modules[module_type].append((item_id, module_data, quantity))

                if station_modules:
                    for module_type in ['weapon', 'defense', 'utility', 'engine']:
                        if module_type in station_modules:
                            type_header = tk.Label(
                                station_scrollable,
                                text=f"▸ {module_type.title()}",
                                font=('Arial', 10, 'bold'),
                                fg=COLORS['text_accent'],
                                bg=COLORS['bg_medium']
                            )
                            type_header.pack(anchor='w', padx=5, pady=(5, 2))

                            for module_id, module_data, quantity in station_modules[module_type]:
                                module_frame = tk.Frame(station_scrollable, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                                module_frame.pack(fill=tk.X, padx=5, pady=2)

                                # Transfer to ship button (right side)
                                self.create_button(
                                    module_frame,
                                    "➜ Ship",
                                    lambda m=module_id: self.transfer_module_to_ship(m),
                                    width=10,
                                    style='info'
                                ).pack(side=tk.RIGHT, padx=5, pady=5)

                                # Info frame (fills remaining space)
                                info_frame = tk.Frame(module_frame, bg=COLORS['bg_light'])
                                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

                                tk.Label(
                                    info_frame,
                                    text=f"{module_data['name']} (x{quantity})",
                                    font=('Arial', 9, 'bold'),
                                    fg=COLORS['text'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                                # Show module specs using helper function
                                specs_text = format_module_specs(module_data)
                                tk.Label(
                                    info_frame,
                                    text=specs_text,
                                    font=('Arial', 8),
                                    fg=COLORS['text_dim'],
                                    bg=COLORS['bg_light']
                                ).pack(anchor='w')

                else:
                    tk.Label(
                        station_scrollable,
                        text="No modules stored at this station\n\nUse Status > Transfer to move items to station storage",
                        font=('Arial', 10),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_medium'],
                        justify=tk.CENTER
                    ).pack(pady=20)

                station_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
                # station_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

            create_toggle_section(scrollable_frame, "⚙️ Module Management", build_modules_content)

        # ===== 🚀 SHIPS FOR SALE - EXPANDABLE =====
        def build_ships_for_sale_content(parent_frame):
            ships_content = parent_frame
            
            # Get available ships from marketplace
            available_ships = self.engine.ship_market.get_available_ships(
                self.engine.player.location,
                self.engine.player.credits,
                self.engine.player.level,
                self.engine.player.skills
            )

            if available_ships:
                # Info about current credits
                credits_frame = tk.Frame(ships_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                credits_frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(
                    credits_frame,
                    text=f"Your Credits: {self.engine.player.credits:,} CR | Level: {self.engine.player.level}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(pady=5)

                # Group ships by class
                ships_by_class = {}
                for ship in available_ships:
                    class_type = ship['class_type']
                    if class_type not in ships_by_class:
                        ships_by_class[class_type] = []
                    ships_by_class[class_type].append(ship)

                # Class navigation buttons
                class_buttons_frame = tk.Frame(ships_content, bg=COLORS['bg_medium'])
                class_buttons_frame.pack(fill=tk.X, padx=10, pady=5)

                # Container for ship display (will be updated when class is selected)
                ships_display_frame = tk.Frame(ships_content, bg=COLORS['bg_medium'])
                ships_display_frame.pack(fill=tk.BOTH, expand=True)

                # Create function to display ships of a specific class
                def show_class_ships(class_type):
                    # Clear existing display
                    for widget in ships_display_frame.winfo_children():
                        widget.destroy()

                    ships_to_show = ships_by_class.get(class_type, [])

                    if ships_to_show:
                        # Scrollable ship list
                        canvas = tk.Canvas(ships_display_frame, bg=COLORS['bg_medium'], highlightthickness=0, height=300)
                        scrollbar = tk.Scrollbar(ships_display_frame, orient="vertical", command=canvas.yview)
                        scrollable_frame_inner = tk.Frame(canvas, bg=COLORS['bg_medium'])

                        scrollable_frame_inner.bind(
                            "<Configure>",
                            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame_inner.winfo_reqheight()))
                        )

                        canvas.create_window((0, 0), window=scrollable_frame_inner, anchor="nw")
                        canvas.configure(yscrollcommand=scrollbar.set)
                        self.bind_mousewheel(canvas, scrollable_frame_inner)

                        for ship in ships_to_show:
                            ship_frame = tk.Frame(scrollable_frame_inner, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                            ship_frame.pack(fill=tk.X, pady=3, padx=10)

                            # Ship icon
                            icon_frame = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                            icon_frame.pack(side=tk.LEFT, padx=(10, 5), pady=10)

                            icon = self.icon_manager.get_icon('ship', ship['class_type'], size='large')
                            if icon:
                                icon_label = tk.Label(icon_frame, image=icon, bg=COLORS['bg_light'])
                                icon_label.image = icon
                                icon_label.pack()
                            else:
                                symbol = get_symbol('ship', ship['class_type'])
                                tk.Label(
                                    icon_frame,
                                    text=symbol,
                                    font=('Arial', 20),
                                    fg=COLORS['accent'],
                                    bg=COLORS['bg_light']
                                ).pack()

                            info_frame = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

                            # Determine ship status color
                            if not ship.get("in_stock", True):
                                name_color = COLORS['text_dim']
                                status_symbol = "🚫 NOT IN STOCK"
                            elif ship["can_purchase"]:
                                name_color = COLORS['success']
                                status_symbol = "✓"
                            elif not ship["can_pilot"]:
                                name_color = COLORS['text_dim']
                                status_symbol = f"🔒 Req Lv{ship['level_req']}"
                            elif not ship["can_afford"]:
                                name_color = COLORS['warning']
                                status_symbol = "💰 Insufficient Credits"
                            else:
                                name_color = COLORS['text']
                                status_symbol = ""

                            # Ship name with status
                            tk.Label(
                                info_frame,
                                text=f"{ship['name']} [{status_symbol}]",
                                font=('Arial', 11, 'bold'),
                                fg=name_color,
                                bg=COLORS['bg_light']
                            ).pack(anchor='w')

                            # Ship details with stock indicator
                            stock_qty = ship['stock']
                            if stock_qty == 0:
                                stock_indicator = "Stock: OUT OF STOCK"
                                stock_color = COLORS['danger']
                            elif stock_qty == 1:
                                stock_indicator = "Stock: 1 (LAST ONE!)"
                                stock_color = COLORS['warning']
                            elif stock_qty <= 2:
                                stock_indicator = f"Stock: {stock_qty} (Low)"
                                stock_color = COLORS['warning']
                            else:
                                stock_indicator = f"Stock: {stock_qty}"
                                stock_color = COLORS['text_dim']

                            details = f"T{ship['tier_num']} {ship['class_type'].title()} | {stock_indicator} | Cost: {ship['cost']:,} CR"
                            tk.Label(
                                info_frame,
                                text=details,
                                font=('Arial', 9),
                                fg=stock_color,
                                bg=COLORS['bg_light']
                            ).pack(anchor='w')

                            # Stats
                            stats = ship['stats']
                            stats_text = f"Hull: {stats['hull_hp']} | Shield: {stats['shield_capacity']} | Speed: {stats['base_speed']} | Cargo: {stats['cargo_capacity']}"
                            tk.Label(
                                info_frame,
                                text=stats_text,
                                font=('Arial', 8),
                                fg=COLORS['text_dim'],
                                bg=COLORS['bg_light']
                            ).pack(anchor='w', pady=(3, 0))

                            # Buy button
                            button_frame = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                            button_frame.pack(side=tk.RIGHT, padx=10)

                            if not ship.get("in_stock", True):
                                tk.Label(
                                    button_frame,
                                    text="OUT OF\nSTOCK",
                                    font=('Arial', 9, 'bold'),
                                    fg=COLORS['danger'],
                                    bg=COLORS['bg_light'],
                                    justify=tk.CENTER
                                ).pack()
                            elif ship["can_purchase"]:
                                self.create_button(
                                    button_frame,
                                    "Buy",
                                    lambda s=ship['id']: self.buy_ship_action(s),
                                    width=8,
                                    style='success'
                                ).pack()
                            elif not ship["can_pilot"]:
                                tk.Label(
                                    button_frame,
                                    text=f"Level {ship['level_req']}\nRequired",
                                    font=('Arial', 8),
                                    fg=COLORS['danger'],
                                    bg=COLORS['bg_light'],
                                    justify=tk.CENTER
                                ).pack()
                            else:
                                tk.Label(
                                    button_frame,
                                    text="Can't\nAfford",
                                    font=('Arial', 8),
                                    fg=COLORS['warning'],
                                    bg=COLORS['bg_light'],
                                    justify=tk.CENTER
                                ).pack()

                        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

                # Create buttons for each class with ship count
                class_names = {
                    'fighter': '⚔️ Fighters',
                    'cruiser': '🚢 Cruisers',
                    'battleship': '⚓ Battleships',
                    'carrier': '🛸 Carriers',
                    'destroyer': '💥 Destroyers',
                    'hauler': '📦 Haulers',
                    'refinery': '⚗️ Refineries',
                    'scout': '🔍 Scouts'
                }

                selected_class = [None]  # Mutable to track selection

                for class_type in sorted(ships_by_class.keys()):
                    ship_count = len(ships_by_class[class_type])
                    button_text = f"{class_names.get(class_type, class_type.title())} ({ship_count})"

                    btn = self.create_button(
                        class_buttons_frame,
                        button_text,
                        lambda c=class_type: show_class_ships(c),
                        width=15,
                        style='info'
                    )
                    btn.pack(side=tk.LEFT, padx=3, pady=5)

                    # Auto-select first class
                    if selected_class[0] is None:
                        selected_class[0] = class_type

                # Show the first class by default
                if selected_class[0]:
                    show_class_ships(selected_class[0])

            else:
                tk.Label(
                    ships_content,
                    text="No ships for sale at this station",
                    font=('Arial', 11),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_medium']
                ).pack(pady=20)

        create_toggle_section(scrollable_frame, "🚀 Ships For Sale", build_ships_for_sale_content)

        # ===== 📐 SHIP CONSTRUCTION BLUEPRINTS - EXPANDABLE =====
        def build_blueprints_content(parent_frame):
            content = parent_frame
            
            # Current ship info
            current_frame = tk.Frame(content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
            current_frame.pack(fill=tk.X, pady=10, padx=10)

            tk.Label(
                current_frame,
                text=f"Current Ship: {self.engine.vessel.name}",
                font=('Arial', 13, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(pady=10)

            ship_data = VESSEL_CLASSES[self.engine.vessel.vessel_class_id]
            stats_text = f"Hull: {ship_data['hull_hp']} | Shield: {ship_data['shield_capacity']} | " \
                        f"Speed: {ship_data['base_speed']} | Cargo: {ship_data['cargo_capacity']}"
            tk.Label(
                current_frame,
                text=stats_text,
                font=('Arial', 9),
                fg=COLORS['text'],
                bg=COLORS['bg_light']
            ).pack(pady=5)

            # Filter ships by player level
            from data import SHIP_RECIPES

            available_ships = []
            for ship_id, ship_data in list(VESSEL_CLASSES.items())[:30]:  # Limit display
                if ship_data['level_requirement'] <= self.engine.player.level + 5:  # Show some ahead
                    available_ships.append({
                        'id': ship_id,
                        'name': ship_data['name'],
                        'level_req': ship_data['level_requirement'],
                        'type': ship_data['class_type'],
                        'variant': ship_data.get('variant', 'standard'),
                        'tier_num': ship_data.get('tier_num', 1),
                        'stats': ship_data
                    })

            if not available_ships:
                tk.Label(
                    content,
                    text="No ship blueprints available",
                    font=('Arial', 11),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_medium']
                ).pack(pady=20)
                return

            # Scrollable ship list
            canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame_inner = tk.Frame(canvas, bg=COLORS['bg_medium'])

            scrollable_frame_inner.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame_inner.winfo_reqheight()))
            )

            canvas.create_window((0, 0), window=scrollable_frame_inner, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            self.bind_mousewheel(canvas, scrollable_frame_inner)

            for ship in available_ships:
                ship_frame = tk.Frame(scrollable_frame_inner, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                ship_frame.pack(fill=tk.X, pady=5, padx=10)

                # Ship info
                info_frame = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

                # Indicate if locked by level or faction
                locked = ship['level_req'] > self.engine.player.level
                is_faction = ship['stats'].get('faction') is not None
                name_color = COLORS['text_dim'] if locked else (COLORS['warning'] if is_faction else COLORS['accent'])
                lock_symbol = "🔒 " if locked else ""
                faction_symbol = "⭐ " if is_faction else ""

                tk.Label(
                    info_frame,
                    text=f"{lock_symbol}{faction_symbol}{ship['name']}",
                    font=('Arial', 11, 'bold'),
                    fg=name_color,
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                variant_text = f"{ship['variant'].title()} {ship['type'].title()} T{ship['tier_num']} | Level: {ship['level_req']}"
                if is_faction:
                    faction_name = ship['stats'].get('faction', '').replace('_', ' ').title()
                    variant_text += f" | {faction_name} FACTION"

                tk.Label(
                    info_frame,
                    text=variant_text,
                    font=('Arial', 9),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=2)

                stats_text = f"Hull: {ship['stats']['hull_hp']} | Shield: {ship['stats']['shield_capacity']} | " \
                            f"Speed: {ship['stats']['base_speed']} | Cargo: {ship['stats']['cargo_capacity']}"
                tk.Label(
                    info_frame,
                    text=stats_text,
                    font=('Arial', 8),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=2)

                # Component requirements (only for non-faction ships)
                if is_faction:
                    tk.Label(
                        info_frame,
                        text="⚠️ UNCRAFTABLE - Obtained from missions and combat only",
                        font=('Arial', 8),
                        fg=COLORS['warning'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)
                elif ship['id'] in SHIP_RECIPES:
                    recipe = SHIP_RECIPES[ship['id']]
                    components_needed = len(recipe['components'])
                    components_have = sum(1 for comp_id in recipe['components'].keys()
                                         if self.engine.player.ship_cargo.get(comp_id, 0) >= 1)

                    comp_color = COLORS['success'] if components_have == components_needed else COLORS['danger']
                    tk.Label(
                        info_frame,
                        text=f"Components: {components_have}/{components_needed} | Build time: {recipe['time']//60}m",
                        font=('Arial', 8),
                        fg=comp_color,
                        bg=COLORS['bg_light']
                    ).pack(anchor='w', pady=2)

                # Action buttons
                btn_frame = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                btn_frame.pack(side=tk.RIGHT, padx=15, pady=10)

                if locked:
                    tk.Label(
                        btn_frame,
                        text="Locked",
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack()
                else:
                    # Show purchase price
                    purchase_price = self.engine.ship_market.calculate_ship_cost(ship['id'])
                    tk.Label(
                        btn_frame,
                        text=f"Buy: {purchase_price:,} CR",
                        font=('Arial', 9),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(pady=2)

                    # Buy button
                    self.create_button(
                        btn_frame,
                        "Buy Ship",
                        lambda s=ship['id']: self.buy_ship_action(s),
                        width=12,
                        style='success'
                    ).pack(pady=2)

                    # Show sell price if player owns this ship
                    if self.engine.player.has_item(ship['id'], 1):
                        sell_price = self.engine.ship_market.calculate_ship_value(ship['id'])
                        tk.Label(
                            btn_frame,
                            text=f"Sell: {sell_price:,} CR",
                            font=('Arial', 9),
                            fg=COLORS['warning'],
                            bg=COLORS['bg_light']
                        ).pack(pady=2)

                        self.create_button(
                            btn_frame,
                            "Sell Ship",
                            lambda s=ship['id']: self.sell_ship_action(s),
                            width=12,
                            style='warning'
                        ).pack(pady=2)

                    # Manufacturing option (only for non-faction ships)
                    if not is_faction:
                        self.create_button(
                            btn_frame,
                            "View Recipe",
                            lambda: self.show_manufacturing_view('ships'),
                            width=12,
                            style='normal'
                        ).pack(pady=2)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

        create_toggle_section(scrollable_frame, "📐 Ship Construction Blueprints", build_blueprints_content)

    def show_components_view(self):
        """Show component marketplace"""
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            tk.Label(
                self.content_frame,
                text="No component market at this location",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        # Two column layout
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Left: Available components for purchase
        market_panel, market_content = self.create_panel(left_col, "Component Market")
        market_panel.pack(fill=tk.BOTH, expand=True)

        available_components = self.engine.component_market.get_available_components(
            self.engine.player.level,
            location_data.get("services", [])
        )

        canvas1 = tk.Canvas(market_content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar1 = tk.Scrollbar(market_content, orient="vertical", command=canvas1.yview)
        scrollable_frame1 = tk.Frame(canvas1, bg=COLORS['bg_medium'])

        scrollable_frame1.bind(
            "<Configure>",
            lambda e: canvas1.configure(scrollregion=(0, 0, canvas1.winfo_width(), scrollable_frame1.winfo_reqheight()))
        )

        canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
        canvas1.configure(yscrollcommand=scrollbar1.set)
        self.bind_mousewheel(canvas1, scrollable_frame1)

        for component in available_components[:24]:  # Show all components
            comp_frame = tk.Frame(scrollable_frame1, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
            comp_frame.pack(fill=tk.X, pady=3, padx=5)

            info = tk.Frame(comp_frame, bg=COLORS['bg_light'])
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

            tk.Label(
                info,
                text=f"{component['name']}",
                font=('Arial', 10, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            tk.Label(
                info,
                text=f"{component['type'].replace('_', ' ').title()} T{component['tier']} | Level: {component['level_req']} | {component['cost']:,} CR",
                font=('Arial', 8),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            self.create_button(
                comp_frame,
                "Buy",
                lambda c=component['id']: self.buy_component_action(c),
                width=8,
                style='success'
            ).pack(side=tk.RIGHT, padx=10)

        canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        # Right: Player's component inventory
        inv_panel, inv_content = self.create_panel(right_col, "Component Inventory")
        inv_panel.pack(fill=tk.BOTH, expand=True)

        component_inventory = {k: v for k, v in self.engine.player.ship_cargo.items() if k in SHIP_COMPONENTS}

        if component_inventory:
            canvas2 = tk.Canvas(inv_content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar2 = tk.Scrollbar(inv_content, orient="vertical", command=canvas2.yview)
            scrollable_frame2 = tk.Frame(canvas2, bg=COLORS['bg_medium'])

            scrollable_frame2.bind(
                "<Configure>",
                lambda e: canvas2.configure(scrollregion=(0, 0, canvas2.winfo_width(), scrollable_frame2.winfo_reqheight()))
            )

            canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
            canvas2.configure(yscrollcommand=scrollbar2.set)
            self.bind_mousewheel(canvas2, scrollable_frame2)

            for comp_id, quantity in sorted(component_inventory.items()):
                comp_data = SHIP_COMPONENTS[comp_id]
                comp_frame = tk.Frame(scrollable_frame2, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                comp_frame.pack(fill=tk.X, pady=3, padx=5)

                info = tk.Frame(comp_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                tk.Label(
                    info,
                    text=f"{comp_data['name']} x{quantity}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                value = self.engine.component_market.get_component_value(comp_id)
                tk.Label(
                    info,
                    text=f"Sell value: {value:,} CR each",
                    font=('Arial', 8),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                self.create_button(
                    comp_frame,
                    "Sell",
                    lambda c=comp_id: self.sell_component_action(c),
                    width=8,
                    style='warning'
                ).pack(side=tk.RIGHT, padx=10)

            canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                inv_content,
                text="No components in inventory",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

    def buy_component_action(self, comp_id):
        """Buy a ship component"""
        success, message = self.engine.buy_component(comp_id)

        if success:
            messagebox.showinfo("Purchase Complete", message)
            self.update_top_bar()
            self.show_components_view()
        else:
            messagebox.showerror("Purchase Failed", message)

    def sell_component_action(self, comp_id):
        """Sell a ship component"""
        success, message = self.engine.sell_component(comp_id)

        if success:
            messagebox.showinfo("Sale Complete", message)
            self.update_top_bar()
            self.show_components_view()
        else:
            messagebox.showerror("Sale Failed", message)

    def switch_ship_action(self, ship_id):
        """Switch to a different ship from berths"""
        success, message = self.engine.switch_ship(ship_id)

        if success:
            messagebox.showinfo("Ship Switched", message)
            self.update_top_bar()
            self.show_shipyard_view()
        else:
            messagebox.showerror("Switch Failed", message)

    def buy_ship_action(self, ship_id):
        """Buy a complete ship"""
        success, message = self.engine.buy_ship(ship_id)

        if success:
            messagebox.showinfo("Purchase Complete", message)
            self.update_top_bar()
            self.show_shipyard_view()
        elif message == "NO_BERTH":
            # No berth available - offer to purchase one
            berth_overview = self.engine.berth_manager.get_berth_overview(self.engine.player.location)
            berth_cost = berth_overview["purchase_cost"]

            if berth_overview["can_purchase"]:
                max_purchasable = berth_overview['max_berths'] - berth_overview['total']

                # Calculate cost for multiple berths
                def calculate_multi_berth_cost(quantity):
                    total = 0
                    for i in range(quantity):
                        current_berths = berth_overview['total'] + i
                        location_type = self.engine.berth_manager.shipyards[self.engine.player.location].get("location_type", "standard_station")
                        base_price = self.engine.berth_manager.BERTH_PRICES.get(location_type, 35000)
                        multiplier = 1.0 + (current_berths * 0.2)
                        total += int(base_price * multiplier)
                    return total

                # Ask how many berths to purchase
                quantity = simpledialog.askinteger(
                    "Purchase Berths",
                    f"Current berths: {berth_overview['used']}/{berth_overview['total']}\n"
                    f"Maximum berths: {berth_overview['max_berths']}\n"
                    f"Available to purchase: {max_purchasable}\n\n"
                    f"First berth cost: {berth_cost:,} CR\n\n"
                    f"How many berths would you like to purchase?",
                    minvalue=1,
                    maxvalue=max_purchasable,
                    initialvalue=1
                )

                if quantity:
                    # Calculate total cost
                    total_cost = calculate_multi_berth_cost(quantity)

                    # Confirm purchase
                    berth_word = "berth" if quantity == 1 else "berths"
                    response = messagebox.askyesno(
                        "Confirm Purchase",
                        f"Purchase {quantity} {berth_word} for {total_cost:,} CR?"
                    )

                    if response:
                        # Purchase berths
                        purchased = 0
                        total_spent = 0
                        for i in range(quantity):
                            success_berth, msg_berth, cost = self.engine.purchase_berth()
                            if success_berth:
                                purchased += 1
                                total_spent += cost
                            else:
                                if purchased > 0:
                                    messagebox.showinfo("Partial Purchase",
                                        f"Purchased {purchased} {berth_word} for {total_spent:,} CR\n\n{msg_berth}")
                                else:
                                    messagebox.showerror("Purchase Failed", msg_berth)
                                break

                        if purchased == quantity:
                            berth_word = "berth" if purchased == 1 else "berths"
                            messagebox.showinfo("Berths Purchased",
                                f"Successfully purchased {purchased} {berth_word} for {total_spent:,} CR")

                        self.update_top_bar()
                        # Retry ship purchase
                        if purchased > 0:
                            self.buy_ship_action(ship_id)
            else:
                messagebox.showerror(
                    "No Berths Available",
                    f"No empty berths at this location.\n\n"
                    f"Current berths: {berth_overview['used']}/{berth_overview['total']}\n"
                    f"Maximum berths: {berth_overview['max_berths']}\n\n"
                    f"You've reached the maximum number of berths at this location."
                )
        else:
            messagebox.showerror("Purchase Failed", message)

    def sell_ship_action(self, ship_id):
        """Sell a ship"""
        # Confirm before selling
        ship_name = VESSEL_CLASSES[ship_id]["name"]
        if not messagebox.askyesno("Confirm Sale", f"Sell {ship_name}?"):
            return

        success, message = self.engine.sell_ship(ship_id)

        if success:
            messagebox.showinfo("Sale Complete", message)
            self.update_top_bar()
            self.show_shipyard_view()
        else:
            messagebox.showerror("Sale Failed", message)

    def repair_vessel_action(self, repair_hull: bool, repair_shields: bool):
        """Repair vessel hull and/or shields"""
        repair_info = self.engine.get_repair_cost()

        # Confirm repair
        repair_type = "all systems" if repair_hull and repair_shields else ("hull" if repair_hull else "shields")
        cost = repair_info['total_cost'] if repair_hull and repair_shields else (
            repair_info['hull_cost'] if repair_hull else repair_info['shield_cost']
        )

        if not messagebox.askyesno("Confirm Repair", f"Repair {repair_type} for {cost:,} CR?"):
            return

        success, message = self.engine.repair_vessel(repair_hull, repair_shields)

        if success:
            messagebox.showinfo("Repair Complete", message)
            self.update_top_bar()
            self.show_shipyard_view()
        else:
            messagebox.showerror("Repair Failed", message)

    def install_module_action(self, module_id):
        """Install a module from inventory to the current ship"""
        # Check if player has the module in inventory
        if not self.engine.player.has_item(module_id, 1):
            messagebox.showerror("Installation Failed", "Module not found in inventory")
            return

        # Get module info
        if module_id not in MODULES:
            messagebox.showerror("Installation Failed", "Invalid module")
            return

        module_data = MODULES[module_id]
        module_type = module_data["type"]

        # Check if slots are full
        vessel = self.engine.vessel
        current_count = len(vessel.installed_modules[module_type])
        max_slots = vessel.module_slots[module_type]

        replace_module_id = None

        if current_count >= max_slots:
            # Slots are full, ask which module to replace
            installed_modules = vessel.installed_modules[module_type]

            if not installed_modules:
                messagebox.showerror("Installation Failed", f"No {module_type} slots available")
                return

            # Create selection dialog
            replace_window = tk.Toplevel(self.root)
            replace_window.title("Replace Module")
            replace_window.geometry("500x400")
            replace_window.configure(bg=COLORS['bg_dark'])
            replace_window.transient(self.root)
            replace_window.grab_set()

            tk.Label(
                replace_window,
                text=f"All {module_type} slots are full.\nSelect a module to replace:",
                font=('Arial', 11, 'bold'),
                fg=COLORS['text'],
                bg=COLORS['bg_dark']
            ).pack(pady=15)

            # Scrollable list of installed modules
            canvas = tk.Canvas(replace_window, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar = tk.Scrollbar(replace_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

            selected_module = [None]  # Use list to allow modification in nested function

            def select_and_close(mod_id):
                selected_module[0] = mod_id
                replace_window.destroy()

            # Display each installed module
            for installed_mod_id in installed_modules:
                if installed_mod_id in MODULES:
                    installed_mod_data = MODULES[installed_mod_id]

                    mod_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                    mod_frame.pack(fill=tk.X, padx=10, pady=5)

                    info_frame = tk.Frame(mod_frame, bg=COLORS['bg_light'])
                    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

                    tk.Label(
                        info_frame,
                        text=installed_mod_data['name'],
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                    # Show module specs
                    from utils import format_module_specs
                    specs_text = format_module_specs(installed_mod_data)
                    tk.Label(
                        info_frame,
                        text=specs_text,
                        font=('Arial', 8),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                    self.create_button(
                        mod_frame,
                        "Replace",
                        lambda m=installed_mod_id: select_and_close(m),
                        width=10,
                        style='warning'
                    ).pack(side=tk.RIGHT, padx=10, pady=10)

            # Cancel button
            button_frame = tk.Frame(replace_window, bg=COLORS['bg_dark'])
            button_frame.pack(pady=10)

            self.create_button(
                button_frame,
                "Cancel",
                replace_window.destroy,
                width=15,
                style='normal'
            ).pack()

            # Wait for window to close
            self.root.wait_window(replace_window)

            replace_module_id = selected_module[0]

            if replace_module_id is None:
                # User cancelled
                return

        # Try to install the module
        success, message, replaced_mod = self.engine.vessel.install_module(module_id, replace_module_id)

        if success:
            # Remove from inventory
            self.engine.player.remove_item(module_id, 1)

            # If a module was replaced, add it to station inventory
            if replaced_mod:
                station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
                if replaced_mod in station_inv:
                    station_inv[replaced_mod] += 1
                else:
                    station_inv[replaced_mod] = 1

                replaced_name = MODULES[replaced_mod]["name"]
                messagebox.showinfo("Module Installed",
                    f"{message}\n\n{replaced_name} moved to station inventory")
            else:
                messagebox.showinfo("Module Installed", message)

            self.update_top_bar()
            self.show_shipyard_view()
        else:
            messagebox.showerror("Installation Failed", message)

    def remove_module_action(self, module_id, module_type):
        """Remove a module from the current ship and return it to inventory"""
        # Try to uninstall the module
        success, message = self.engine.vessel.uninstall_module(module_id, module_type)

        if success:
            # Add to inventory (no cargo capacity check for modules)
            self.engine.player.add_item(module_id, 1)
            messagebox.showinfo("Module Removed", f"{message} - Returned to inventory")
            self.update_top_bar()
            self.show_shipyard_view()
        else:
            messagebox.showerror("Removal Failed", message)

    def transfer_module_to_ship(self, module_id):
        """Transfer a module from station storage to ship cargo"""
        current_location = self.engine.player.location
        station_inventory = self.engine.player.station_inventories.get(current_location, {})
        
        # Check if module exists in station inventory
        if module_id not in station_inventory or station_inventory[module_id] <= 0:
            messagebox.showerror("Transfer Failed", "Module not found in station storage")
            return
        
        # Get module info
        if module_id not in MODULES:
            messagebox.showerror("Transfer Failed", "Invalid module")
            return
        
        module_data = MODULES[module_id]
        
        # Check cargo capacity
        cargo_capacity = self.engine.vessel.cargo_capacity
        can_add, message = can_add_item(self.engine.player.ship_cargo, cargo_capacity, module_id, 1)
        
        if not can_add:
            messagebox.showerror("Transfer Failed", f"Insufficient cargo space: {message}")
            return
        
        # Transfer the module
        # Remove from station
        station_inventory[module_id] -= 1
        if station_inventory[module_id] == 0:
            del station_inventory[module_id]
        
        # Add to ship cargo
        self.engine.player.add_item(module_id, 1)
        
        messagebox.showinfo("Transfer Complete", f"{module_data['name']} transferred to ship cargo")
        self.update_top_bar()
        self.show_shipyard_view()

    def show_modules_view(self):
        """Show module marketplace"""
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            tk.Label(
                self.content_frame,
                text="No module market at this location",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        # Two column layout
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Left: Available modules for purchase
        market_panel, market_content = self.create_panel(left_col, "Module Market")
        market_panel.pack(fill=tk.BOTH, expand=True)

        available_modules = self.engine.module_market.get_available_modules(
            self.engine.player.level,
            location_data.get("services", [])
        )

        canvas1 = tk.Canvas(market_content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar1 = tk.Scrollbar(market_content, orient="vertical", command=canvas1.yview)
        scrollable_frame1 = tk.Frame(canvas1, bg=COLORS['bg_medium'])

        scrollable_frame1.bind(
            "<Configure>",
            lambda e: canvas1.configure(scrollregion=(0, 0, canvas1.winfo_width(), scrollable_frame1.winfo_reqheight()))
        )

        canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
        canvas1.configure(yscrollcommand=scrollbar1.set)
        self.bind_mousewheel(canvas1, scrollable_frame1)

        for module in available_modules[:15]:  # Limit display
            mod_frame = tk.Frame(scrollable_frame1, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
            mod_frame.pack(fill=tk.X, pady=3, padx=5)

            # Module icon
            icon_frame = tk.Frame(mod_frame, bg=COLORS['bg_light'])
            icon_frame.pack(side=tk.LEFT, padx=(10, 5), pady=8)

            icon = self.icon_manager.get_icon('module', module['id'], size='small')
            if icon:
                icon_label = tk.Label(icon_frame, image=icon, bg=COLORS['bg_light'])
                icon_label.image = icon
                icon_label.pack()
            else:
                symbol = get_symbol('module', module['id'])
                tk.Label(
                    icon_frame,
                    text=symbol,
                    font=('Arial', 14),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack()

            info = tk.Frame(mod_frame, bg=COLORS['bg_light'])
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=8)

            tk.Label(
                info,
                text=f"{module['name']} (T{module['tier']})",
                font=('Arial', 10, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            tk.Label(
                info,
                text=f"{module['type'].title()} | Level: {module['level_req']} | {module['cost']:,} CR",
                font=('Arial', 8),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            # Add module specs
            module_full_data = MODULES.get(module['id'], {})
            if module_full_data:
                specs_text = format_module_specs(module_full_data)
                tk.Label(
                    info,
                    text=specs_text,
                    font=('Arial', 8),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w', pady=(2, 0))

            self.create_button(
                mod_frame,
                "Buy",
                lambda m=module['id']: self.buy_module_action(m),
                width=8,
                style='success'
            ).pack(side=tk.RIGHT, padx=10)

        canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        # Right: Player's module inventory
        inv_panel, inv_content = self.create_panel(right_col, "Module Inventory")
        inv_panel.pack(fill=tk.BOTH, expand=True)

        module_inventory = {k: v for k, v in self.engine.player.ship_cargo.items() if k in MODULES}

        if module_inventory:
            canvas2 = tk.Canvas(inv_content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar2 = tk.Scrollbar(inv_content, orient="vertical", command=canvas2.yview)
            scrollable_frame2 = tk.Frame(canvas2, bg=COLORS['bg_medium'])

            scrollable_frame2.bind(
                "<Configure>",
                lambda e: canvas2.configure(scrollregion=(0, 0, canvas2.winfo_width(), scrollable_frame2.winfo_reqheight()))
            )

            canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
            canvas2.configure(yscrollcommand=scrollbar2.set)
            self.bind_mousewheel(canvas2, scrollable_frame2)

            for module_id, quantity in sorted(module_inventory.items()):
                module_data = MODULES[module_id]
                mod_frame = tk.Frame(scrollable_frame2, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                mod_frame.pack(fill=tk.X, pady=3, padx=5)

                info = tk.Frame(mod_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                tk.Label(
                    info,
                    text=f"{module_data['name']} x{quantity}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Add module specs
                specs_text = format_module_specs(module_data)
                tk.Label(
                    info,
                    text=specs_text,
                    font=('Arial', 8),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                value = self.engine.module_market.get_module_value(module_id)
                tk.Label(
                    info,
                    text=f"Sell value: {value:,} CR each",
                    font=('Arial', 8),
                    fg=COLORS['success'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                btn_frame = tk.Frame(mod_frame, bg=COLORS['bg_light'])
                btn_frame.pack(side=tk.RIGHT, padx=10)

                self.create_button(
                    btn_frame,
                    "Sell",
                    lambda m=module_id: self.sell_module_action(m),
                    width=8,
                    style='warning'
                ).pack(side=tk.LEFT, padx=2)

                self.create_button(
                    btn_frame,
                    "Install",
                    lambda m=module_id: self.install_module_action_from_market(m),
                    width=8,
                    style='success'
                ).pack(side=tk.LEFT, padx=2)

            canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                inv_content,
                text="No modules in inventory",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

    def buy_module_action(self, module_id):
        """Buy a module"""
        success, message = self.engine.buy_module(module_id)

        if success:
            messagebox.showinfo("Purchase Complete", message)
            self.update_top_bar()
            self.show_modules_view()
        else:
            messagebox.showerror("Purchase Failed", message)

    def sell_module_action(self, module_id):
        """Sell a module"""
        success, message = self.engine.sell_module(module_id)

        if success:
            messagebox.showinfo("Sale Complete", message)
            self.update_top_bar()
            self.show_modules_view()
        else:
            messagebox.showerror("Sale Failed", message)

    def install_module_action_from_market(self, module_id):
        """Install a module from modules market view"""
        # Check if player has the module in inventory
        if not self.engine.player.has_item(module_id, 1):
            messagebox.showerror("Installation Failed", "Module not found in inventory")
            return

        # Get module info
        if module_id not in MODULES:
            messagebox.showerror("Installation Failed", "Invalid module")
            return

        module_data = MODULES[module_id]
        module_type = module_data["type"]

        # Check if slots are full
        vessel = self.engine.vessel
        current_count = len(vessel.installed_modules[module_type])
        max_slots = vessel.module_slots[module_type]

        replace_module_id = None

        if current_count >= max_slots:
            # Slots are full, ask which module to replace
            installed_modules = vessel.installed_modules[module_type]

            if not installed_modules:
                messagebox.showerror("Installation Failed", f"No {module_type} slots available")
                return

            # Create selection dialog
            replace_window = tk.Toplevel(self.root)
            replace_window.title("Replace Module")
            replace_window.geometry("500x400")
            replace_window.configure(bg=COLORS['bg_dark'])
            replace_window.transient(self.root)
            replace_window.grab_set()

            tk.Label(
                replace_window,
                text=f"All {module_type} slots are full.\nSelect a module to replace:",
                font=('Arial', 11, 'bold'),
                fg=COLORS['text'],
                bg=COLORS['bg_dark']
            ).pack(pady=15)

            # Scrollable list of installed modules
            canvas = tk.Canvas(replace_window, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar = tk.Scrollbar(replace_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

            selected_module = [None]  # Use list to allow modification in nested function

            def select_and_close(mod_id):
                selected_module[0] = mod_id
                replace_window.destroy()

            # Display each installed module
            for installed_mod_id in installed_modules:
                if installed_mod_id in MODULES:
                    installed_mod_data = MODULES[installed_mod_id]

                    mod_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                    mod_frame.pack(fill=tk.X, padx=10, pady=5)

                    info_frame = tk.Frame(mod_frame, bg=COLORS['bg_light'])
                    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

                    tk.Label(
                        info_frame,
                        text=installed_mod_data['name'],
                        font=('Arial', 10, 'bold'),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                    # Show module specs
                    from utils import format_module_specs
                    specs_text = format_module_specs(installed_mod_data)
                    tk.Label(
                        info_frame,
                        text=specs_text,
                        font=('Arial', 8),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                    self.create_button(
                        mod_frame,
                        "Replace",
                        lambda m=installed_mod_id: select_and_close(m),
                        width=10,
                        style='warning'
                    ).pack(side=tk.RIGHT, padx=10, pady=10)

            # Cancel button
            button_frame = tk.Frame(replace_window, bg=COLORS['bg_dark'])
            button_frame.pack(pady=10)

            self.create_button(
                button_frame,
                "Cancel",
                replace_window.destroy,
                width=15,
                style='normal'
            ).pack()

            # Wait for window to close
            self.root.wait_window(replace_window)

            replace_module_id = selected_module[0]

            if replace_module_id is None:
                # User cancelled
                return

        # Try to install the module
        success, message, replaced_mod = self.engine.vessel.install_module(module_id, replace_module_id)

        if success:
            # Remove from inventory
            self.engine.player.remove_item(module_id, 1)

            # If a module was replaced, add it to station inventory
            if replaced_mod:
                station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
                if replaced_mod in station_inv:
                    station_inv[replaced_mod] += 1
                else:
                    station_inv[replaced_mod] = 1

                replaced_name = MODULES[replaced_mod]["name"]
                messagebox.showinfo("Module Installed",
                    f"{message}\n\n{replaced_name} moved to station inventory")
            else:
                messagebox.showinfo("Module Installed", message)

            self.update_top_bar()
            self.show_modules_view()
        else:
            messagebox.showerror("Installation Failed", message)

    def show_manufacturing_view(self, category='modules'):
        """Show manufacturing interface with category tabs"""
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        if "manufacturing" not in location_data.get("services", []):
            tk.Label(
                self.content_frame,
                text="No manufacturing facility at this location",
                font=('Arial', 14),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_dark']
            ).pack(expand=True)
            return

        # Category tabs
        tab_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'])
        tab_frame.pack(fill=tk.X, pady=(0, 10))

        categories = [
            ('Modules', 'modules'),
            ('Module Parts', 'module_components'),
            ('Ship Parts', 'ship_components'),
            ('Ships', 'ships')
        ]

        for label, cat in categories:
            style = 'success' if cat == category else 'normal'
            self.create_button(
                tab_frame,
                label,
                lambda c=cat: self.show_manufacturing_view(c),
                width=12,
                style=style
            ).pack(side=tk.LEFT, padx=2)

        panel, content = self.create_panel(self.content_frame, f"Manufacturing - {category.title()}")
        panel.pack(fill=tk.BOTH, expand=True)

        # Show active job if any
        active_job = self.engine.manufacturing.get_job_progress()
        if active_job:
            job_frame = tk.Frame(content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
            job_frame.pack(fill=tk.X, pady=10, padx=10)

            item_type_label = active_job.get('item_type', 'module').title()
            tk.Label(
                job_frame,
                text=f"Manufacturing {item_type_label}: {active_job['item_name']} x{active_job['quantity']}",
                font=('Arial', 12, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(pady=10)

            # Progress bar
            progress_outer = tk.Frame(job_frame, bg=COLORS['bg_dark'], width=400, height=25)
            progress_outer.pack(pady=5)
            progress_outer.pack_propagate(False)

            progress_width = int((active_job['progress'] / 100.0) * 400)
            progress_inner = tk.Frame(progress_outer, bg=COLORS['success'], width=progress_width, height=25)
            progress_inner.pack(side=tk.LEFT)

            tk.Label(
                job_frame,
                text=f"{active_job['progress']:.1f}% - {int(active_job['remaining_seconds'])}s remaining",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_light']
            ).pack(pady=10)

            return  # Don't show recipes while manufacturing

        # Show available recipes based on category
        from data import MANUFACTURING_RECIPES, MODULE_COMPONENT_RECIPES, COMPONENT_RECIPES, SHIP_RECIPES, MODULE_COMPONENTS

        canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        # Select recipes based on category
        if category == 'modules':
            recipes = MANUFACTURING_RECIPES
            data_source = MODULES
            item_type = 'module'
        elif category == 'module_components':
            # Module components (for crafting modules)
            recipes = MODULE_COMPONENT_RECIPES
            data_source = MODULE_COMPONENTS
            item_type = 'module_component'
        elif category == 'ship_components':
            # Ship components (for crafting ships)
            recipes = COMPONENT_RECIPES
            data_source = SHIP_COMPONENTS
            item_type = 'ship_component'
        else:  # ships
            recipes = SHIP_RECIPES
            data_source = VESSEL_CLASSES
            item_type = 'ship'

        for item_id, recipe in list(recipes.items())[:30]:  # Limit display
            item_data = data_source[item_id]

            # Check level requirement
            level_req = item_data.get('level_requirement', 1)
            player_level = self.engine.player.level
            skill_req = recipe.get('skill_requirement', 0)
            
            # Determine correct skill based on category
            if category == 'ships':
                skill_id = 'ship_construction'
                skill_display_name = 'Ship Construction'
            else:
                skill_id = 'module_manufacturing'
                skill_display_name = 'Module Manufacturing'
            
            player_skill = self.engine.player.get_skill_level(skill_id)

            # Determine if locked
            level_locked = player_level < level_req
            skill_locked = player_skill < skill_req
            is_locked = level_locked or skill_locked

            # Color coding
            if is_locked:
                frame_color = COLORS['bg_dark']
                name_color = COLORS['text_dim']
                border_color = COLORS['border']
            else:
                frame_color = COLORS['bg_light']
                name_color = COLORS['accent']
                border_color = COLORS['border_glow']

            recipe_frame = tk.Frame(scrollable_frame, bg=frame_color, relief=tk.RIDGE, bd=2, highlightbackground=border_color, highlightthickness=1)
            recipe_frame.pack(fill=tk.X, pady=5, padx=10)

            # Item info
            info = tk.Frame(recipe_frame, bg=frame_color)
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

            # Name with lock indicator
            name_text = item_data.get('name', item_id)
            if level_locked:
                name_text = f"🔒 {name_text} (Requires Level {level_req})"

            tk.Label(
                info,
                text=name_text,
                font=('Arial', 11, 'bold'),
                fg=name_color,
                bg=frame_color
            ).pack(anchor='w')

            # Requirements (materials or components)
            if 'materials' in recipe:
                req_text = "Materials: "
                for mat_id, qty in list(recipe['materials'].items())[:5]:  # Limit display
                    mat_name = RESOURCES.get(mat_id, {}).get('name', mat_id)
                    have = self.engine.player.ship_cargo.get(mat_id, 0)
                    req_text += f"{mat_name} ({have}/{qty}), "
                req_text = req_text.rstrip(', ')
            elif 'components' in recipe:
                components_list = recipe['components']
                total_components = len(components_list)

                # For ships, show detailed component breakdown
                if item_type == 'ship':
                    req_text = f"Ship Components ({total_components} required):\n"
                    all_have = True
                    missing_count = 0

                    for comp_id, qty in components_list.items():
                        # Get component name
                        if comp_id in SHIP_COMPONENTS:
                            comp_name = SHIP_COMPONENTS[comp_id].get('name', comp_id)
                            # Shorten the name for display
                            comp_short = comp_name.replace(' T1', '').replace(' T2', '').replace(' T3', '')
                            comp_short = comp_short.split()[-2:] if len(comp_short.split()) > 2 else comp_short.split()
                            comp_short = ' '.join(comp_short)
                        else:
                            comp_short = comp_id

                        have = self.engine.player.ship_cargo.get(comp_id, 0)
                        if have < qty:
                            all_have = False
                            missing_count += 1

                        status = "✓" if have >= qty else "✗"
                        req_text += f"  {status} {comp_short} ({have}/{qty})\n"

                    req_text = req_text.rstrip('\n')
                    if missing_count > 0:
                        req_text += f"\n⚠️ Missing {missing_count} component types"
                else:
                    # For modules, show compact list
                    req_text = f"Components ({total_components} required): "
                    all_have = True

                    for comp_id, qty in list(components_list.items())[:5]:  # Show up to 5
                        # Check both MODULE_COMPONENTS and SHIP_COMPONENTS
                        if comp_id in MODULE_COMPONENTS:
                            comp_name = MODULE_COMPONENTS[comp_id].get('name', comp_id).split()[0]
                        elif comp_id in SHIP_COMPONENTS:
                            comp_name = SHIP_COMPONENTS[comp_id].get('name', comp_id).split()[0]
                        else:
                            comp_name = comp_id

                        have = self.engine.player.ship_cargo.get(comp_id, 0)
                        if have < qty:
                            all_have = False
                        req_text += f"{comp_name} ({have}/{qty}), "

                    if total_components > 5:
                        req_text += f"... +{total_components - 5} more"
                    else:
                        req_text = req_text.rstrip(', ')

            # Use appropriate alignment for multi-line (ships) vs single-line (modules)
            label_justify = tk.LEFT if item_type == 'ship' else tk.LEFT
            tk.Label(
                info,
                text=req_text,
                font=('Consolas', 8) if item_type == 'ship' else ('Arial', 9),
                fg=COLORS['text'] if not is_locked else COLORS['text_dim'],
                bg=frame_color,
                wraplength=700,
                justify=label_justify
            ).pack(anchor='w', pady=2)

            # Level and skill requirements
            time_min = recipe['time'] // 60
            time_sec = recipe['time'] % 60

            req_parts = [f"Time: {time_min}m {time_sec}s"]

            # Level requirement with status
            if level_locked:
                req_parts.append(f"Level: {player_level}/{level_req} ❌")
            else:
                req_parts.append(f"Level: {level_req} ✓")

            # Skill requirement with status
            if skill_locked:
                req_parts.append(f"{skill_display_name}: {player_skill}/{skill_req} ❌")
            else:
                if skill_req > 0:
                    req_parts.append(f"{skill_display_name}: {skill_req} ✓")
                else:
                    req_parts.append(f"{skill_display_name}: None")

            requirements_text = " | ".join(req_parts)

            tk.Label(
                info,
                text=requirements_text,
                font=('Arial', 9),
                fg=COLORS['text_dim'],
                bg=frame_color
            ).pack(anchor='w')

            # Craft button
            if is_locked:
                tk.Label(
                    recipe_frame,
                    text="LOCKED",
                    font=('Arial', 9, 'bold'),
                    fg=COLORS['danger'],
                    bg=frame_color
                ).pack(side=tk.RIGHT, padx=15, pady=10)
            else:
                self.create_button(
                    recipe_frame,
                    "Craft",
                    lambda i=item_id: self.start_manufacturing(i),
                    width=10,
                    style='success'
                ).pack(side=tk.RIGHT, padx=15, pady=10)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works

    def start_manufacturing(self, module_id):
        """Start manufacturing a module"""
        success, message = self.engine.start_manufacturing(module_id, 1)

        if success:
            messagebox.showinfo("Manufacturing Started", message)
            self.show_manufacturing_view()
        else:
            messagebox.showerror("Manufacturing Failed", message)

    def save_and_exit(self):
        """Save the game and exit"""
        # Confirm with user
        if not messagebox.askyesno("Save & Exit", "Save your progress and exit the game?"):
            return

        # Stop the update thread
        self.update_running = False
        if hasattr(self, 'update_thread') and self.update_thread:
            self.update_thread.join(timeout=1.0)

        # Save the game
        try:
            success = self.engine.save_current_game()
            if success:
                messagebox.showinfo("Game Saved", "Your progress has been saved successfully!")
            else:
                messagebox.showwarning("Save Warning", "Game save may have failed. Check save file.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving game: {str(e)}")

        # Exit the application
        self.root.quit()
        self.root.destroy()

    def show_storage_view(self):
        """Show storage/inventory management"""
        self.clear_content()

        # Two column layout
        left_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        right_col = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Left: Ship cargo
        ship_panel, ship_content = self.create_panel(left_col, "Ship Cargo")
        ship_panel.pack(fill=tk.BOTH, expand=True)

        if self.engine.player.ship_cargo:
            for item_id, quantity in sorted(self.engine.player.ship_cargo.items()):
                if item_id in RESOURCES:
                    resource = RESOURCES[item_id]

                    item_frame = tk.Frame(ship_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                    item_frame.pack(fill=tk.X, pady=2, padx=5)

                    # Icon
                    icon = self.icon_manager.get_icon('resource', item_id, size='small', rarity=resource.get('rarity'))
                    if icon:
                        icon_label = tk.Label(item_frame, image=icon, bg=COLORS['bg_light'])
                        icon_label.image = icon
                        icon_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
                    else:
                        symbol = get_symbol('resource', item_id)
                        tk.Label(
                            item_frame,
                            text=symbol,
                            font=('Arial', 12),
                            fg=COLORS['accent'],
                            bg=COLORS['bg_light']
                        ).pack(side=tk.LEFT, padx=(10, 5), pady=5)

                    tk.Label(
                        item_frame,
                        text=f"{resource['name']}: {quantity}",
                        font=('Arial', 10),
                        fg=COLORS['text'],
                        bg=COLORS['bg_light']
                    ).pack(side=tk.LEFT, padx=5, pady=5)

                    self.create_button(
                        item_frame,
                        "→ Station",
                        lambda i=item_id: self.transfer_to_station_dialog(i),
                        width=10,
                        style='warning'
                    ).pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            tk.Label(
                ship_content,
                text="Ship cargo is empty",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

        # Right: Station storage
        station_panel, station_content = self.create_panel(right_col, f"Station Storage - {LOCATIONS[self.engine.player.location]['name']}")
        station_panel.pack(fill=tk.BOTH, expand=True)

        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)

        if station_inv:
            from data import COMMODITIES
            for item_id, quantity in sorted(station_inv.items()):
                # Check if it's a resource or commodity
                if item_id in RESOURCES:
                    item_data = RESOURCES[item_id]
                    item_type = 'resource'
                elif item_id in COMMODITIES:
                    item_data = COMMODITIES[item_id]
                    item_type = 'commodity'
                else:
                    continue  # Skip unknown items

                item_frame = tk.Frame(station_content, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                item_frame.pack(fill=tk.X, pady=2, padx=5)

                # Icon
                icon = self.icon_manager.get_icon(item_type, item_id, size='small', rarity=item_data.get('rarity'))
                if icon:
                    icon_label = tk.Label(item_frame, image=icon, bg=COLORS['bg_light'])
                    icon_label.image = icon
                    icon_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)
                else:
                    symbol = get_symbol(item_type, item_id)
                    tk.Label(
                        item_frame,
                        text=symbol,
                        font=('Arial', 12),
                        fg=COLORS['accent'],
                        bg=COLORS['bg_light']
                    ).pack(side=tk.LEFT, padx=(10, 5), pady=5)

                tk.Label(
                    item_frame,
                    text=f"{item_data['name']}: {quantity}",
                    font=('Arial', 10),
                    fg=COLORS['text'],
                    bg=COLORS['bg_light']
                ).pack(side=tk.LEFT, padx=5, pady=5)

                self.create_button(
                    item_frame,
                    "→ Ship",
                    lambda i=item_id: self.transfer_to_ship_dialog(i),
                    width=10,
                    style='success'
                ).pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            tk.Label(
                station_content,
                text="No items stored at this station",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

    def show_recycle_view(self):
        """Show recycling interface"""
        self.clear_content()

        location_data = LOCATIONS[self.engine.player.location]

        # Check if manufacturing facility available
        if "manufacturing" not in location_data.get("services", []):
            panel, content = self.create_panel(self.content_frame, "Recycling Center")
            panel.pack(fill=tk.BOTH, expand=True)

            tk.Label(
                content,
                text="⚠️ Recycling requires a Manufacturing facility",
                font=('Arial', 12),
                fg=COLORS['warning'],
                bg=COLORS['bg_medium']
            ).pack(pady=50)
            return

        # Info message
        info_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        tk.Label(
            info_frame,
            text="♻️ Break down components and ships for 80% materials back (random mix). Earn XP for recycling.",
            font=('Arial', 10),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10, padx=10)

        # Two columns
        columns = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        columns.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(columns, bg=COLORS['bg_dark'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_col = tk.Frame(columns, bg=COLORS['bg_dark'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Left: Recyclable components
        comp_panel, comp_content = self.create_panel(left_col, "Recycle Components")
        comp_panel.pack(fill=tk.BOTH, expand=True)

        recyclable = self.engine.recycling.get_recyclable_items(self.engine.player.ship_cargo)
        components = recyclable["components"]

        if components:
            canvas1 = tk.Canvas(comp_content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar1 = tk.Scrollbar(comp_content, orient="vertical", command=canvas1.yview)
            scrollable_frame1 = tk.Frame(canvas1, bg=COLORS['bg_medium'])

            scrollable_frame1.bind(
                "<Configure>",
                lambda e: canvas1.configure(scrollregion=(0, 0, canvas1.winfo_width(), scrollable_frame1.winfo_reqheight()))
            )

            canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
            canvas1.configure(yscrollcommand=scrollbar1.set)
            self.bind_mousewheel(canvas1, scrollable_frame1)

            for comp in components:
                comp_frame = tk.Frame(scrollable_frame1, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                comp_frame.pack(fill=tk.X, pady=3, padx=5)

                info = tk.Frame(comp_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                tk.Label(
                    info,
                    text=f"{comp['name']} (x{comp['quantity']})",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Show expected recovery
                preview = self.engine.recycling.preview_recycle_component(comp['id'])
                if preview:
                    mat_text = ", ".join([f"{qty}x {mat}" for mat, qty in preview.items()])
                    tk.Label(
                        info,
                        text=f"~{mat_text}",
                        font=('Arial', 8),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                self.create_button(
                    comp_frame,
                    "Recycle",
                    lambda c=comp['id']: self.recycle_component_action(c),
                    width=10,
                    style='warning'
                ).pack(side=tk.RIGHT, padx=10)

            canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                comp_content,
                text="No components to recycle",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

        # Right: Recyclable ships
        ship_panel, ship_content = self.create_panel(right_col, "Recycle Ships")
        ship_panel.pack(fill=tk.BOTH, expand=True)

        ships = recyclable["ships"]

        if ships:
            canvas2 = tk.Canvas(ship_content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar2 = tk.Scrollbar(ship_content, orient="vertical", command=canvas2.yview)
            scrollable_frame2 = tk.Frame(canvas2, bg=COLORS['bg_medium'])

            scrollable_frame2.bind(
                "<Configure>",
                lambda e: canvas2.configure(scrollregion=(0, 0, canvas2.winfo_width(), scrollable_frame2.winfo_reqheight()))
            )

            canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
            canvas2.configure(yscrollcommand=scrollbar2.set)
            self.bind_mousewheel(canvas2, scrollable_frame2)

            for ship in ships:
                ship_frame = tk.Frame(scrollable_frame2, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
                ship_frame.pack(fill=tk.X, pady=5, padx=5)

                info = tk.Frame(ship_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                tk.Label(
                    info,
                    text=f"{ship['name']} (x{ship['quantity']})",
                    font=('Arial', 11, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                # Show expected recovery
                preview = self.engine.recycling.preview_recycle_ship(ship['id'])
                if preview:
                    mat_text = ", ".join([f"{qty}x {mat}" for mat, qty in list(preview.items())[:3]])
                    more = f" +{len(preview)-3} more" if len(preview) > 3 else ""
                    tk.Label(
                        info,
                        text=f"~{mat_text}{more}",
                        font=('Arial', 8),
                        fg=COLORS['text_dim'],
                        bg=COLORS['bg_light']
                    ).pack(anchor='w')

                self.create_button(
                    ship_frame,
                    "Recycle",
                    lambda s=ship['id']: self.recycle_ship_action(s),
                    width=10,
                    style='warning'
                ).pack(side=tk.RIGHT, padx=10)

            canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                ship_content,
                text="No ships to recycle",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium']
            ).pack(pady=20)

    def show_refine_view(self):
        """Show ore refining interface"""
        self.clear_content()

        # Info message
        info_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        tk.Label(
            info_frame,
            text="⚗️ Refine raw ores into refined resources. Yield is RNG-based: Common ores = 80-95%, Rare ores = 50-65%",
            font=('Arial', 10),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10, padx=10)

        # Main panel
        panel, content = self.create_panel(self.content_frame, "Refine Raw Ores")
        panel.pack(fill=tk.BOTH, expand=True)

        # Get raw ores from ship cargo and station storage
        raw_ores_available = {}
        # From ship cargo
        for item_id, quantity in self.engine.player.ship_cargo.items():
            if item_id in RAW_RESOURCES:
                raw_ores_available[item_id] = {"ship": quantity, "station": 0}

        # From station storage at current location
        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
        for item_id, quantity in station_inv.items():
            if item_id in RAW_RESOURCES:
                if item_id in raw_ores_available:
                    raw_ores_available[item_id]["station"] = quantity
                else:
                    raw_ores_available[item_id] = {"ship": 0, "station": quantity}

        if raw_ores_available:
            canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
            scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), scrollable_frame.winfo_reqheight()))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            self.bind_mousewheel(canvas, scrollable_frame)

            for ore_id, quantities in sorted(raw_ores_available.items()):
                ore_data = RAW_RESOURCES[ore_id]
                refined_id = ore_data.get("refines_to")

                if not refined_id:
                    continue

                refined_data = RESOURCES[refined_id]
                rarity = ore_data.get("rarity", "common")
                min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

                total_qty = quantities["ship"] + quantities["station"]

                ore_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
                ore_frame.pack(fill=tk.X, pady=3, padx=5)

                info = tk.Frame(ore_frame, bg=COLORS['bg_light'])
                info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

                # Show total quantity with breakdown
                qty_breakdown = []
                if quantities["ship"] > 0:
                    qty_breakdown.append(f"Ship: {quantities['ship']}")
                if quantities["station"] > 0:
                    qty_breakdown.append(f"Station: {quantities['station']}")
                breakdown_text = " | ".join(qty_breakdown)

                tk.Label(
                    info,
                    text=f"{ore_data['name']} (x{total_qty}) - {breakdown_text}",
                    font=('Arial', 10, 'bold'),
                    fg=COLORS['accent'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                tk.Label(
                    info,
                    text=f"→ {refined_data['name']} | Yield: {int(min_yield*100)}-{int(max_yield*100)}% | Rarity: {rarity.replace('_', ' ').title()}",
                    font=('Arial', 8),
                    fg=COLORS['text_dim'],
                    bg=COLORS['bg_light']
                ).pack(anchor='w')

                self.create_button(
                    ore_frame,
                    "Refine",
                    lambda o=ore_id: self.refine_ore_dialog(o),
                    width=10,
                    style='success'
                ).pack(side=tk.RIGHT, padx=10)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Hidden - mouse wheel still works
        else:
            tk.Label(
                content,
                text="No raw ores to refine.\nGo mining to collect raw ores!",
                font=('Arial', 10),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_medium'],
                justify=tk.CENTER
            ).pack(pady=50)

    def refine_ore_dialog(self, ore_id):
        """Show dialog to refine ore"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Refine Ore")
        dialog.geometry("350x200")
        dialog.configure(bg=COLORS['bg_medium'])

        ore_data = RAW_RESOURCES[ore_id]
        refined_data = RESOURCES[ore_data.get("refines_to")]

        # Get total quantity from ship and station
        quantities = self.engine.player.get_total_accessible_quantity(ore_id)
        max_qty = quantities["total"]
        ship_qty = quantities["ship"]
        station_qty = quantities["station"]

        rarity = ore_data.get("rarity", "common")
        min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

        tk.Label(
            dialog,
            text=f"Refine {ore_data['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Show breakdown of available ore
        available_text = f"Available: {max_qty} units"
        if ship_qty > 0 and station_qty > 0:
            available_text += f"\n(Ship: {ship_qty} | Station: {station_qty})"
        elif station_qty > 0:
            available_text += f"\n(Station storage)"
        available_text += f"\nYield: {int(min_yield*100)}-{int(max_yield*100)}% → {refined_data['name']}"

        tk.Label(
            dialog,
            text=available_text,
            font=('Arial', 9),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=5)

        qty_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
        qty_frame.pack(pady=10)

        tk.Label(
            qty_frame,
            text="Quantity:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(side=tk.LEFT, padx=5)

        qty_entry = tk.Entry(qty_frame, width=10, font=('Arial', 10))
        qty_entry.pack(side=tk.LEFT, padx=5)
        qty_entry.insert(0, str(max_qty))

        def do_refine():
            try:
                quantity = int(qty_entry.get())
                if quantity <= 0:
                    messagebox.showerror("Invalid Quantity", "Quantity must be greater than 0")
                    return

                success, message = self.engine.refine_ore(ore_id, quantity)

                if success:
                    messagebox.showinfo("Refining Complete", message)
                    self.update_top_bar()
                    dialog.destroy()
                    self.show_refine_view()
                else:
                    messagebox.showerror("Refining Failed", message)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number")

        button_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
        button_frame.pack(pady=10)

        self.create_button(
            button_frame,
            "Refine",
            do_refine,
            width=10,
            style='success'
        ).pack(side=tk.LEFT, padx=5)

        self.create_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            width=10,
            style='danger'
        ).pack(side=tk.LEFT, padx=5)

    def recycle_component_action(self, comp_id):
        """Recycle a component"""
        # Confirm before recycling
        comp_name = SHIP_COMPONENTS[comp_id]["name"]
        if not messagebox.askyesno("Confirm Recycle", f"Recycle {comp_name} for materials?\n\nYou'll get ~80% of materials back as a random mix."):
            return

        success, message = self.engine.recycle_component(comp_id)

        if success:
            messagebox.showinfo("Recycling Complete", message)
            self.update_top_bar()
            self.show_recycle_view()
        else:
            messagebox.showerror("Recycling Failed", message)

    def recycle_ship_action(self, ship_id):
        """Recycle a ship"""
        # Confirm before recycling
        ship_name = VESSEL_CLASSES[ship_id]["name"]
        if not messagebox.askyesno("Confirm Recycle", f"Recycle {ship_name} for materials?\n\nYou'll get ~80% of materials back as a random mix."):
            return

        success, message = self.engine.recycle_ship(ship_id)

        if success:
            messagebox.showinfo("Recycling Complete", message)
            self.update_top_bar()
            self.show_recycle_view()
        else:
            messagebox.showerror("Recycling Failed", message)

    def transfer_to_station_dialog(self, item_id):
        """Transfer items to station"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Transfer to Station")
        dialog.geometry("300x150")
        dialog.configure(bg=COLORS['bg_medium'])

        resource = RESOURCES[item_id]
        max_qty = self.engine.player.ship_cargo[item_id]

        tk.Label(
            dialog,
            text=f"Transfer {resource['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            dialog,
            text=f"Available: {max_qty}",
            font=('Arial', 9),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        ).pack()

        quantity_var = tk.IntVar(value=max_qty)
        quantity_entry = tk.Entry(dialog, textvariable=quantity_var, justify='center')
        quantity_entry.pack(pady=5)

        def do_transfer():
            success, message = self.engine.transfer_to_station(item_id, quantity_var.get())
            dialog.destroy()
            if success:
                messagebox.showinfo("Transfer Complete", message)
                self.show_storage_view()
            else:
                messagebox.showerror("Transfer Failed", message)

        self.create_button(dialog, "Transfer", do_transfer, width=15, style='success').pack(pady=10)

    def transfer_to_ship_dialog(self, item_id):
        """Transfer items to ship"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Transfer to Ship")
        dialog.geometry("300x150")
        dialog.configure(bg=COLORS['bg_medium'])

        resource = RESOURCES[item_id]
        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
        max_qty = station_inv[item_id]

        tk.Label(
            dialog,
            text=f"Transfer {resource['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            dialog,
            text=f"Available: {max_qty}",
            font=('Arial', 9),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        ).pack()

        quantity_var = tk.IntVar(value=max_qty)
        quantity_entry = tk.Entry(dialog, textvariable=quantity_var, justify='center')
        quantity_entry.pack(pady=5)

        def do_transfer():
            success, message = self.engine.transfer_to_ship(item_id, quantity_var.get())
            dialog.destroy()
            if success:
                messagebox.showinfo("Transfer Complete", message)
                self.show_storage_view()
            else:
                messagebox.showerror("Transfer Failed", message)

        self.create_button(dialog, "Transfer", do_transfer, width=15, style='success').pack(pady=10)

    def travel_to(self, destination_id):
        """Initiate travel to a location with animation"""
        success, message, travel_info = self.engine.travel_to_location(destination_id)

        if success and travel_info:
            # Show travel animation overlay
            self.show_travel_animation(travel_info)
        else:
            messagebox.showerror("Travel Failed", message)
    
    def show_travel_animation(self, travel_info):
        """Show animated travel overlay with map"""
        # Create fullscreen overlay
        overlay = tk.Toplevel(self.root)
        overlay.title("Traveling...")
        overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")
        overlay.configure(bg=COLORS['bg_dark'])
        overlay.transient(self.root)
        overlay.grab_set()
        
        # Center the overlay
        overlay.update_idletasks()
        x = (overlay.winfo_screenwidth() // 2) - (overlay.winfo_width() // 2)
        y = (overlay.winfo_screenheight() // 2) - (overlay.winfo_height() // 2)
        overlay.geometry(f"+{x}+{y}")
        
        # Main container with two columns
        main_container = tk.Frame(overlay, bg=COLORS['bg_dark'])
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # LEFT COLUMN: Universe Map
        left_frame = tk.Frame(main_container, bg=COLORS['bg_dark'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Map panel with title
        map_panel_frame = tk.Frame(left_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=2)
        map_panel_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            map_panel_frame,
            text="⭐ Universe Map",
            font=('Arial', 14, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)
        
        # Create map content
        map_content_frame = tk.Frame(map_panel_frame, bg=COLORS['bg_dark'])
        map_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # RIGHT COLUMN: Travel Progress Info
        right_frame = tk.Frame(main_container, bg=COLORS['bg_dark'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Configure right frame width
        right_frame.config(width=400)
        right_frame.pack_propagate(False)
        
        # Force display update before creating heavy map
        overlay.update()
        
        # Title
        tk.Label(
            right_frame,
            text="🚀 TRAVELING",
            font=('Arial', 20, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        ).pack(pady=(0, 15))
        
        # Route info - more compact
        route_frame = tk.Frame(right_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=2)
        route_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            route_frame,
            text=f"From: {travel_info['origin_name']}",
            font=('Arial', 11),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=5)
        
        tk.Label(
            route_frame,
            text="▼",
            font=('Arial', 16),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=2)
        
        # Animated ship indicator
        ship_label = tk.Label(
            route_frame,
            text="🚀",
            font=('Arial', 30),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        )
        ship_label.pack(pady=5)
        
        tk.Label(
            route_frame,
            text="▼",
            font=('Arial', 16),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=2)
        
        tk.Label(
            route_frame,
            text=f"To: {travel_info['destination_name']}",
            font=('Arial', 11, 'bold'),
            fg=COLORS['success'],
            bg=COLORS['bg_medium']
        ).pack(pady=5)
        
        # COUNTDOWN TIMER - Large and prominent
        countdown_frame = tk.Frame(right_frame, bg=COLORS['bg_dark'], relief=tk.RIDGE, bd=3)
        countdown_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            countdown_frame,
            text="TIME REMAINING",
            font=('Arial', 10, 'bold'),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_dark']
        ).pack(pady=(10, 5))
        
        countdown_label = tk.Label(
            countdown_frame,
            text=f"{travel_info['travel_time']}s",
            font=('Arial', 48, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        )
        countdown_label.pack(pady=10)
        
        # Travel info - compact
        info_frame = tk.Frame(right_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, pady=15)
        
        from travel_system import format_travel_time
        
        tk.Label(
            info_frame,
            text=f"Distance: {travel_info['distance']} ls",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=3)
        
        tk.Label(
            info_frame,
            text=f"Total Time: {format_travel_time(travel_info['travel_time'])}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=3)
        
        danger_pct = int(travel_info['danger_level'] * 100)
        danger_color = COLORS['success'] if danger_pct < 30 else (COLORS['warning'] if danger_pct < 70 else COLORS['danger'])
        tk.Label(
            info_frame,
            text=f"Danger: {danger_pct}%",
            font=('Arial', 10),
            fg=danger_color,
            bg=COLORS['bg_light']
        ).pack(pady=3)
        
        # Progress bar
        progress_frame = tk.Frame(right_frame, bg=COLORS['bg_dark'])
        progress_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            progress_frame,
            text="Progress:",
            font=('Arial', 11, 'bold'),
            fg=COLORS['text'],
            bg=COLORS['bg_dark']
        ).pack()
        
        progress_bar = tk.Canvas(progress_frame, height=25, bg=COLORS['bg_medium'], highlightthickness=0)
        progress_bar.pack(fill=tk.X, pady=8)
        
        # ETA label
        eta_label = tk.Label(
            progress_frame,
            text=f"ETA: {format_travel_time(travel_info['travel_time'])}",
            font=('Arial', 13, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        )
        eta_label.pack(pady=5)
        
        # Cancel button
        button_frame = tk.Frame(right_frame, bg=COLORS['bg_dark'])
        button_frame.pack(pady=15)
        
        # Animation state
        animation_state = {
            'start_time': time.time(),
            'duration': travel_info['travel_time'],
            'cancelled': False,
            'ship_animation_frame': 0
        }

        def cancel_travel():
            animation_state['cancelled'] = True
            overlay.destroy()
            messagebox.showinfo("Travel Cancelled", "Travel was cancelled. You remain at your current location.")

        cancel_btn = self.create_button(
            button_frame,
            "Cancel Travel",
            cancel_travel,
            width=15,
            style='danger'
        )
        cancel_btn.pack()
        
        def update_animation():
            if animation_state['cancelled']:
                return
            
            elapsed = time.time() - animation_state['start_time']
            remaining = max(0, animation_state['duration'] - elapsed)
            progress = min(1.0, elapsed / animation_state['duration'])
            
            # Update countdown timer (large display)
            remaining_int = int(remaining)
            if remaining_int > 0:
                countdown_label.config(text=f"{remaining_int}s")
            else:
                countdown_label.config(text="0s", fg=COLORS['success'])
            
            # Update progress bar
            bar_width = progress_bar.winfo_width()
            if bar_width > 1:
                progress_bar.delete("all")
                filled_width = int(bar_width * progress)
                progress_bar.create_rectangle(
                    0, 0, filled_width, 30,
                    fill=COLORS['success'], outline=""
                )
                progress_bar.create_text(
                    bar_width // 2, 15,
                    text=f"{int(progress * 100)}%",
                    font=('Arial', 12, 'bold'),
                    fill=COLORS['text']
                )
            
            # Update ETA
            eta_label.config(text=f"ETA: {format_travel_time(int(remaining))}")
            
            # Animate ship (rotate icon)
            animation_state['ship_animation_frame'] += 1
            ship_icons = ["🚀", "🛸", "✈️", "🛩️"]
            ship_label.config(text=ship_icons[animation_state['ship_animation_frame'] % len(ship_icons)])
            
            # Check if travel complete
            if elapsed >= animation_state['duration']:
                complete_travel()
            else:
                overlay.after(100, update_animation)  # Update every 100ms
        
        def complete_travel():
            overlay.destroy()
            
            # Complete travel in engine
            success, message = self.engine.complete_travel(travel_info['destination'])
            
            if success:
                # Check for combat encounter
                if self.engine.current_combat:
                    messagebox.showinfo("Travel Complete", message)
                    self.show_combat_view()
                # Check for trader encounter
                elif self.engine.current_trader:
                    messagebox.showinfo("Travel Complete", message)
                    self.show_trader_encounter()
                else:
                    messagebox.showinfo("Travel Complete", message)
                    self.update_top_bar()
                    self.refresh_navigation()
                    self.show_travel_view()
            else:
                messagebox.showerror("Travel Error", message)
        
        # Load the universe map asynchronously after window displays
        # This prevents blocking and ensures immediate display
        def load_map():
            self.draw_universe_map(map_content_frame)
            overlay.update()
        
        # Start map loading after a brief delay
        overlay.after(50, load_map)
        
        # Start animation immediately
        overlay.after(100, update_animation)

    def scan_area(self):
        """Scan current area"""
        success, message = self.engine.scan_area()
        messagebox.showinfo("Scan Results", message)

    def mine_resources(self):
        """Mine resources"""
        success, message = self.engine.mine_resources()

        if success:
            # Always update top bar to reflect inventory changes
            self.update_top_bar()
            
            # Check for combat encounter FIRST
            if self.engine.current_combat:
                # Show mining results message which includes encounter notification
                messagebox.showinfo("Mining", message)
                # Then switch to combat view
                self.show_combat_view()
            # Check for trader encounter
            elif self.engine.current_trader:
                # Show mining results message which includes encounter notification
                messagebox.showinfo("Mining", message)
                # Then switch to trader view
                self.show_trader_encounter()
            else:
                # Only show normal mining results if no encounter
                messagebox.showinfo("Mining", message)
                # Refresh mining view to show updated stats
                self.show_mining_view()
        else:
            messagebox.showerror("Mining Failed", message)

    def scan_anomaly(self):
        """Scan anomalies for research data"""
        success, message = self.engine.scan_anomaly()

        if success:
            messagebox.showinfo("Anomaly Scan", message)
            self.update_top_bar()
        else:
            messagebox.showerror("Scan Failed", message)

    def deliver_cargo(self):
        """Deliver cargo for transport contracts"""
        success, message = self.engine.deliver_cargo()

        if success:
            messagebox.showinfo("Cargo Delivered", message)
            self.update_top_bar()
            self.show_status_view()  # Refresh to show updated cargo volume
        else:
            messagebox.showwarning("Delivery Failed", message)

    def buy_resource(self, resource_id):
        """Buy resource from market"""
        # Enhanced quantity dialog with destination selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Resource")
        dialog.geometry("350x220")
        dialog.configure(bg=COLORS['bg_medium'])

        resource = RESOURCES[resource_id]

        tk.Label(
            dialog,
            text=f"Buy {resource['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Destination selection
        tk.Label(
            dialog,
            text="Buy to:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(5, 0))

        dest_var = tk.StringVar(value="ship")
        dest_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
        dest_frame.pack(pady=5)

        tk.Radiobutton(
            dest_frame,
            text="Ship Cargo",
            variable=dest_var,
            value="ship",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium'],
            selectcolor=COLORS['bg_light']
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            dest_frame,
            text="Station Storage",
            variable=dest_var,
            value="station",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium'],
            selectcolor=COLORS['bg_light']
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            dialog,
            text="Quantity:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(10, 0))

        quantity_var = tk.IntVar(value=10)
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_buy():
            market = self.engine.economy.get_market(self.engine.player.location)
            trade_bonus = self.engine.player.get_skill_bonus("trade_proficiency", "buy_discount")

            success, message, cost = market.buy_from_market(
                resource_id, quantity_var.get(), self.engine.player.credits, trade_bonus
            )

            if success:
                self.engine.player.spend_credits(cost)
                
                # Add to the selected destination
                if dest_var.get() == "ship":
                    self.engine.player.add_item(resource_id, quantity_var.get())
                else:
                    # Add to station storage
                    station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
                    station_inv[resource_id] = station_inv.get(resource_id, 0) + quantity_var.get()
                
                dialog.destroy()
                self.update_top_bar()
                self.show_market_view(self.current_market_category)
            else:
                messagebox.showerror("Purchase Failed", message)

        self.create_button(dialog, "Buy", do_buy, width=15, style='success').pack(pady=10)

    def sell_resource(self, resource_id):
        """Sell resource to market"""
        # Check both ship cargo and station inventory
        ship_qty = self.engine.player.inventory.get(resource_id, 0)
        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
        station_qty = station_inv.get(resource_id, 0)

        if ship_qty == 0 and station_qty == 0:
            messagebox.showerror("Error", "You don't have this resource")
            return

        # Enhanced quantity dialog with source selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Sell Resource")
        dialog.geometry("350x250")
        dialog.configure(bg=COLORS['bg_medium'])

        resource = RESOURCES[resource_id]

        tk.Label(
            dialog,
            text=f"Sell {resource['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Source selection
        tk.Label(
            dialog,
            text="Sell from:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(5, 0))

        source_var = tk.StringVar(value="ship" if ship_qty > 0 else "station")
        source_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
        source_frame.pack(pady=5)

        def update_quantity_max():
            if source_var.get() == "ship":
                quantity_var.set(ship_qty)
            else:
                quantity_var.set(station_qty)

        if ship_qty > 0:
            tk.Radiobutton(
                source_frame,
                text=f"Ship Cargo ({ship_qty})",
                variable=source_var,
                value="ship",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                selectcolor=COLORS['bg_light'],
                command=update_quantity_max
            ).pack(side=tk.LEFT, padx=10)

        if station_qty > 0:
            tk.Radiobutton(
                source_frame,
                text=f"Station Storage ({station_qty})",
                variable=source_var,
                value="station",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                selectcolor=COLORS['bg_light'],
                command=update_quantity_max
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            dialog,
            text="Quantity:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(10, 0))

        quantity_var = tk.IntVar(value=ship_qty if ship_qty > 0 else station_qty)
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_sell():
            quantity = quantity_var.get()
            source = source_var.get()

            # Check if we have enough in the selected source
            if source == "ship":
                if ship_qty < quantity:
                    messagebox.showerror("Error", "Insufficient quantity in ship cargo")
                    return
            else:
                if station_qty < quantity:
                    messagebox.showerror("Error", "Insufficient quantity in station storage")
                    return

            market = self.engine.economy.get_market(self.engine.player.location)
            trade_bonus = self.engine.player.get_skill_bonus("trade_proficiency", "sell_bonus")
            tax_reduction = self.engine.player.get_skill_bonus("trade_proficiency", "tax_reduction")

            success, message, payment = market.sell_to_market(
                resource_id, quantity, trade_bonus, tax_reduction
            )

            if success:
                # Remove from the correct inventory
                if source == "ship":
                    self.engine.player.remove_item(resource_id, quantity)
                else:
                    if station_inv[resource_id] >= quantity:
                        station_inv[resource_id] -= quantity
                        if station_inv[resource_id] == 0:
                            del station_inv[resource_id]

                self.engine.player.add_credits(payment)
                dialog.destroy()
                self.update_top_bar()
                self.show_market_view(self.current_market_category)
            else:
                messagebox.showerror("Sale Failed", message)

        self.create_button(dialog, "Sell", do_sell, width=15, style='warning').pack(pady=10)

    def buy_commodity(self, commodity_id):
        """Buy commodity from market"""
        from data import COMMODITIES

        # Simple quantity dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Buy Commodity")
        dialog.geometry("300x150")
        dialog.configure(bg=COLORS['bg_medium'])

        commodity = COMMODITIES[commodity_id]

        tk.Label(
            dialog,
            text=f"Buy {commodity['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            dialog,
            text="Quantity:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack()

        quantity_var = tk.IntVar(value=10)
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_buy():
            success, message = self.engine.buy_commodity(commodity_id, quantity_var.get())

            if success:
                dialog.destroy()
                self.update_top_bar()
                self.show_market_view(self.current_market_category)
            else:
                messagebox.showerror("Purchase Failed", message)

        self.create_button(dialog, "Buy", do_buy, width=15, style='success').pack(pady=10)

    def sell_commodity(self, commodity_id):
        """Sell commodity to market"""
        from data import COMMODITIES

        # Check both ship cargo and station inventory
        ship_qty = self.engine.player.inventory.get(commodity_id, 0)
        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
        station_qty = station_inv.get(commodity_id, 0)

        if ship_qty == 0 and station_qty == 0:
            messagebox.showerror("Error", "You don't have this commodity")
            return

        # Enhanced quantity dialog with source selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Sell Commodity")
        dialog.geometry("350x250")
        dialog.configure(bg=COLORS['bg_medium'])

        commodity = COMMODITIES[commodity_id]

        tk.Label(
            dialog,
            text=f"Sell {commodity['name']}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        # Source selection
        tk.Label(
            dialog,
            text="Sell from:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(5, 0))

        source_var = tk.StringVar(value="ship" if ship_qty > 0 else "station")
        source_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
        source_frame.pack(pady=5)

        def update_quantity_max():
            if source_var.get() == "ship":
                quantity_var.set(ship_qty)
            else:
                quantity_var.set(station_qty)

        if ship_qty > 0:
            tk.Radiobutton(
                source_frame,
                text=f"Ship Cargo ({ship_qty})",
                variable=source_var,
                value="ship",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                selectcolor=COLORS['bg_light'],
                command=update_quantity_max
            ).pack(side=tk.LEFT, padx=10)

        if station_qty > 0:
            tk.Radiobutton(
                source_frame,
                text=f"Station Storage ({station_qty})",
                variable=source_var,
                value="station",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_medium'],
                selectcolor=COLORS['bg_light'],
                command=update_quantity_max
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            dialog,
            text="Quantity:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(10, 0))

        quantity_var = tk.IntVar(value=ship_qty if ship_qty > 0 else station_qty)
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_sell():
            quantity = quantity_var.get()
            source = source_var.get()

            # Check if we have enough in the selected source
            if source == "ship":
                if ship_qty < quantity:
                    messagebox.showerror("Error", "Insufficient quantity in ship cargo")
                    return
                # Use engine method for ship cargo
                success, message = self.engine.sell_commodity(commodity_id, quantity)
            else:
                if station_qty < quantity:
                    messagebox.showerror("Error", "Insufficient quantity in station storage")
                    return
                # Sell directly from station inventory
                success, message, revenue = self.engine.commodity_market.sell_commodity(
                    self.engine.player.location,
                    commodity_id,
                    quantity
                )
                if success:
                    # Remove from station inventory
                    if station_inv[commodity_id] >= quantity:
                        station_inv[commodity_id] -= quantity
                        if station_inv[commodity_id] == 0:
                            del station_inv[commodity_id]
                    # Add credits
                    self.engine.player.add_credits(revenue)

            if success:
                dialog.destroy()
                self.update_top_bar()
                self.show_market_view(self.current_market_category)
            else:
                messagebox.showerror("Sale Failed", message)

        self.create_button(dialog, "Sell", do_sell, width=15, style='warning').pack(pady=10)

    def load_from_station(self, item_id):
        """Load items from station storage to ship cargo"""
        from data import COMMODITIES, RESOURCES, MODULES

        station_inv = self.engine.player.get_station_inventory(self.engine.player.location)
        station_qty = station_inv.get(item_id, 0)

        if station_qty == 0:
            messagebox.showerror("Error", "No items in station storage")
            return

        # Determine item name and type
        item_name = None
        item_volume = 1  # Default volume

        if item_id in COMMODITIES:
            item_name = COMMODITIES[item_id]['name']
            item_volume = COMMODITIES[item_id].get('volume', 1)
        elif item_id in RESOURCES:
            item_name = RESOURCES[item_id]['name']
            item_volume = RESOURCES[item_id].get('volume', 1)
        elif item_id in MODULES:
            item_name = MODULES[item_id]['name']
            item_volume = MODULES[item_id].get('volume', 10)
        else:
            item_name = item_id
            item_volume = 1

        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Load to Ship")
        dialog.geometry("350x200")
        dialog.configure(bg=COLORS['bg_medium'])

        tk.Label(
            dialog,
            text=f"Load {item_name}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            dialog,
            text=f"Available in station: {station_qty}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack()

        tk.Label(
            dialog,
            text="Quantity to load:",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack(pady=(10, 0))

        quantity_var = tk.IntVar(value=min(station_qty, 10))
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_load():
            quantity = quantity_var.get()

            if quantity <= 0:
                messagebox.showerror("Error", "Invalid quantity")
                return

            if quantity > station_qty:
                messagebox.showerror("Error", f"Only {station_qty} available in station storage")
                return

            # Check cargo space
            current_cargo = self.engine.player.get_cargo_used()
            max_cargo = self.engine.player.get_cargo_capacity()
            needed_space = quantity * item_volume

            if current_cargo + needed_space > max_cargo:
                max_loadable = int((max_cargo - current_cargo) / item_volume)
                messagebox.showerror("Error", f"Insufficient cargo space. Can only load {max_loadable} units")
                return

            # Transfer from station to ship
            station_inv[item_id] -= quantity
            if station_inv[item_id] == 0:
                del station_inv[item_id]

            # Add to ship cargo
            self.engine.player.inventory[item_id] = self.engine.player.inventory.get(item_id, 0) + quantity

            dialog.destroy()
            self.update_top_bar()
            self.show_market_view(self.current_market_category)
            messagebox.showinfo("Success", f"Loaded {quantity} {item_name} to ship cargo")

        self.create_button(dialog, "Load", do_load, width=15, style='success').pack(pady=10)

    def train_skill(self, skill_id):
        """Start training a skill"""
        success, message = self.engine.player.start_skill_training(skill_id)

        if success:
            messagebox.showinfo("Training Started", message)
            # Refresh skills view to show training status
            category = SKILLS[skill_id]["category"]
            self.show_skills_view(category)
        else:
            messagebox.showerror("Training Failed", message)

    def accept_contract(self, contract):
        """Accept a contract"""
        self.engine.contract_board.accept_contract(contract.contract_id, self.engine.player)
        
        # Show different messages based on contract type
        if contract.objectives.get("type") == "transport_cargo":
            item_type = contract.objectives.get("item_type", "resource")
            item_id = contract.objectives.get("resource_id")
            quantity = contract.objectives.get("quantity", 0)
            
            # Get item name
            if item_type == "commodity":
                from data import COMMODITIES
                item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
            else:
                item_name = RESOURCES.get(item_id, {}).get("name", item_id)
            
            messagebox.showinfo(
                "Contract Accepted", 
                f"Accepted: {contract.name}\n\n{quantity}x {item_name} has been placed in station storage.\n\nLoad them onto your ship and deliver to the destination!"
            )
        else:
            messagebox.showinfo("Contract Accepted", f"Accepted: {contract.name}")
        
        self.show_contracts_view()

    def complete_delivery_contract(self, contract):
        """Complete a delivery contract by depositing cargo at destination"""
        success, message = self.engine.contract_board.complete_delivery_contract(contract.contract_id, self.engine.player)
        
        if success:
            # Get reward
            reward = self.engine.contract_board.complete_contract(contract.contract_id)
            if reward:
                self.engine.player.add_credits(reward)
                contract_xp = int(reward / 10)
                self.engine.player.add_experience(contract_xp)
                self.engine.player.stats['contracts_completed'] += 1
                messagebox.showinfo(
                    "Delivery Complete!",
                    f"{message}\n\nReward: {reward:,} CR + {contract_xp} XP"
                )
            else:
                messagebox.showinfo("Delivery Complete!", message)
            
            # Refresh status view to update contracts
            self.show_status_view()
        else:
            messagebox.showerror("Delivery Failed", message)

    def abandon_contract(self, contract):
        """Abandon an active contract"""
        if messagebox.askyesno("Confirm", f"Abandon contract: {contract.name}?"):
            self.engine.contract_board.abandon_contract(contract.contract_id)
            self.show_status_view()

    def show_trader_encounter(self):
        """Show trader encounter dialog"""
        trader = self.engine.current_trader
        if not trader:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Trader Encounter")
        dialog.geometry("600x500")
        dialog.configure(bg=COLORS['bg_dark'])

        # Header
        header_frame = tk.Frame(dialog, bg=COLORS['bg_medium'], height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"📡 Trader Encountered: {trader['name']}",
            font=('Arial', 16, 'bold'),
            fg=COLORS['success'],
            bg=COLORS['bg_medium']
        ).pack(pady=5)

        tk.Label(
            header_frame,
            text=f"Ship: {trader['vessel'].class_name}",
            font=('Arial', 12),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium']
        ).pack()

        # Inventory preview
        info_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)

        tk.Label(
            info_frame,
            text="Trader's Inventory:",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        ).pack(anchor='w', pady=5)

        # Scrollable inventory list
        inv_canvas = tk.Canvas(info_frame, bg=COLORS['bg_medium'], height=200, highlightthickness=0)
        inv_scrollbar = tk.Scrollbar(info_frame, orient='vertical', command=inv_canvas.yview)
        inv_frame = tk.Frame(inv_canvas, bg=COLORS['bg_medium'])

        inv_canvas.configure(yscrollcommand=inv_scrollbar.set)
        # inv_scrollbar.pack(side='right', fill='y')  # Hidden - mouse wheel still works
        inv_canvas.pack(side='left', fill='both', expand=True)
        inv_canvas.create_window((0, 0), window=inv_frame, anchor='nw')

        # Display trader's inventory
        for item_id, quantity in sorted(trader['inventory'].items()):
            item_name = self.engine._get_item_name(item_id)
            item_frame = tk.Frame(inv_frame, bg=COLORS['bg_light'])
            item_frame.pack(fill='x', padx=5, pady=2)

            tk.Label(
                item_frame,
                text=f"  {item_name} x{quantity}",
                font=('Arial', 10),
                fg=COLORS['text'],
                bg=COLORS['bg_light'],
                anchor='w'
            ).pack(side='left', fill='x', expand=True, padx=5, pady=3)

        inv_frame.update_idletasks()
        inv_canvas.configure(scrollregion=inv_canvas.bbox('all'))

        # Credits display
        tk.Label(
            info_frame,
            text=f"Trader Credits: {trader['credits']:,} CR",
            font=('Arial', 11),
            fg=COLORS['warning'],
            bg=COLORS['bg_dark']
        ).pack(pady=10)

        # Action buttons
        button_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        button_frame.pack(fill='x', padx=10, pady=10)

        def do_trade():
            dialog.destroy()
            self.show_trader_trade_interface()

        def do_attack():
            result = messagebox.askyesno(
                "Attack Trader",
                f"Are you sure you want to attack {trader['name']}?\n\nThis will start combat and may be dangerous!",
                icon='warning'
            )
            if result:
                dialog.destroy()
                attack_result = self.engine.attack_trader()
                if attack_result:
                    messagebox.showinfo("Combat Started", "Engaging trader in combat!")
                    self.show_combat_view()

        def dismiss():
            success, message = self.engine.dismiss_trader()
            dialog.destroy()
            if success and "Traveled to" in message:
                # Travel was completed after trader encounter
                messagebox.showinfo("Travel", message)
                self.update_top_bar()
                self.refresh_navigation()
                self.show_travel_view()
            else:
                # Just dismissed trader during mining
                self.show_status_view()

        self.create_button(button_frame, "💱 Trade", do_trade, width=15, style='success').pack(side='left', padx=5)
        self.create_button(button_frame, "⚔️ Attack", do_attack, width=15, style='danger').pack(side='left', padx=5)
        self.create_button(button_frame, "Dismiss", dismiss, width=15, style='normal').pack(side='left', padx=5)

    def show_trader_trade_interface(self):
        """Show trading interface with trader"""
        trader = self.engine.current_trader
        if not trader:
            messagebox.showerror("Error", "Trader is no longer available")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Trading with {trader['name']}")
        dialog.geometry("900x600")
        dialog.configure(bg=COLORS['bg_dark'])

        # Header
        header_frame = tk.Frame(dialog, bg=COLORS['bg_medium'], height=60)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"Trading with {trader['name']}",
            font=('Arial', 16, 'bold'),
            fg=COLORS['success'],
            bg=COLORS['bg_medium']
        ).pack(side='left', padx=10, pady=10)

        tk.Label(
            header_frame,
            text=f"Your Credits: {self.engine.player.credits:,} CR  |  Trader Credits: {trader['credits']:,} CR",
            font=('Arial', 11),
            fg=COLORS['warning'],
            bg=COLORS['bg_medium']
        ).pack(side='right', padx=10, pady=10)

        # Two-column layout
        main_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left side - Buy from trader
        buy_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        buy_frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(
            buy_frame,
            text="Buy from Trader (20% markup)",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        buy_canvas = tk.Canvas(buy_frame, bg=COLORS['bg_medium'], highlightthickness=0)
        buy_scrollbar = tk.Scrollbar(buy_frame, orient='vertical', command=buy_canvas.yview)
        buy_list_frame = tk.Frame(buy_canvas, bg=COLORS['bg_medium'])

        buy_canvas.configure(yscrollcommand=buy_scrollbar.set)
        # buy_scrollbar.pack(side='right', fill='y')  # Hidden - mouse wheel still works
        buy_canvas.pack(side='left', fill='both', expand=True)
        buy_canvas.create_window((0, 0), window=buy_list_frame, anchor='nw')

        # Populate buy list
        for item_id, quantity in sorted(trader['inventory'].items()):
            if quantity <= 0:
                continue

            item_name = self.engine._get_item_name(item_id)
            base_price = self.engine._get_item_base_price(item_id)
            buy_price = int(base_price * 1.2)  # 20% markup

            item_frame = tk.Frame(buy_list_frame, bg=COLORS['bg_light'])
            item_frame.pack(fill='x', padx=5, pady=2)

            info_text = f"{item_name}\n{buy_price:,} CR each | Stock: {quantity}"
            tk.Label(
                item_frame,
                text=info_text,
                font=('Arial', 9),
                fg=COLORS['text'],
                bg=COLORS['bg_light'],
                anchor='w',
                justify='left'
            ).pack(side='left', fill='x', expand=True, padx=5, pady=3)

            self.create_button(
                item_frame,
                "Buy",
                lambda i=item_id: self.buy_from_trader(i, dialog),
                width=8,
                style='success'
            ).pack(side='right', padx=5, pady=2)

        buy_list_frame.update_idletasks()
        buy_canvas.configure(scrollregion=buy_canvas.bbox('all'))

        # Right side - Sell to trader
        sell_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        sell_frame.pack(side='right', fill='both', expand=True, padx=5)

        tk.Label(
            sell_frame,
            text="Sell to Trader (20% markdown)",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        sell_canvas = tk.Canvas(sell_frame, bg=COLORS['bg_medium'], highlightthickness=0)
        sell_scrollbar = tk.Scrollbar(sell_frame, orient='vertical', command=sell_canvas.yview)
        sell_list_frame = tk.Frame(sell_canvas, bg=COLORS['bg_medium'])

        sell_canvas.configure(yscrollcommand=sell_scrollbar.set)
        # sell_scrollbar.pack(side='right', fill='y')  # Hidden - mouse wheel still works
        sell_canvas.pack(side='left', fill='both', expand=True)
        sell_canvas.create_window((0, 0), window=sell_list_frame, anchor='nw')

        # Populate sell list with player's ship cargo
        for item_id, quantity in sorted(self.engine.player.ship_cargo.items()):
            if quantity <= 0:
                continue

            item_name = self.engine._get_item_name(item_id)
            base_price = self.engine._get_item_base_price(item_id)
            sell_price = int(base_price * 0.8)  # 20% markdown

            item_frame = tk.Frame(sell_list_frame, bg=COLORS['bg_light'])
            item_frame.pack(fill='x', padx=5, pady=2)

            info_text = f"{item_name}\n{sell_price:,} CR each | You have: {quantity}"
            tk.Label(
                item_frame,
                text=info_text,
                font=('Arial', 9),
                fg=COLORS['text'],
                bg=COLORS['bg_light'],
                anchor='w',
                justify='left'
            ).pack(side='left', fill='x', expand=True, padx=5, pady=3)

            self.create_button(
                item_frame,
                "Sell",
                lambda i=item_id: self.sell_to_trader(i, dialog),
                width=8,
                style='warning'
            ).pack(side='right', padx=5, pady=2)

        sell_list_frame.update_idletasks()
        sell_canvas.configure(scrollregion=sell_canvas.bbox('all'))

        # Close button
        button_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        button_frame.pack(fill='x', padx=10, pady=10)

        def close_trade():
            success, message = self.engine.dismiss_trader()
            dialog.destroy()
            if success and "Traveled to" in message:
                # Travel was completed after trader encounter
                messagebox.showinfo("Travel", message)
                self.update_top_bar()
                self.refresh_navigation()
                self.show_travel_view()
            else:
                # Just dismissed trader during mining
                self.show_status_view()

        self.create_button(button_frame, "Close", close_trade, width=15, style='normal').pack()

    def buy_from_trader(self, item_id, parent_dialog):
        """Buy item from trader"""
        trader = self.engine.current_trader
        if not trader:
            return

        # Quantity dialog
        qty_dialog = tk.Toplevel(parent_dialog)
        qty_dialog.title("Buy Item")
        qty_dialog.geometry("300x150")
        qty_dialog.configure(bg=COLORS['bg_medium'])

        item_name = self.engine._get_item_name(item_id)
        max_qty = trader['inventory'].get(item_id, 0)

        tk.Label(
            qty_dialog,
            text=f"Buy {item_name}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            qty_dialog,
            text=f"Quantity (max {max_qty}):",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack()

        quantity_var = tk.IntVar(value=1)
        quantity_entry = tk.Entry(
            qty_dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_buy():
            success, message = self.engine.trade_with_trader(item_id, quantity_var.get(), is_buying=True)
            if success:
                qty_dialog.destroy()
                parent_dialog.destroy()
                messagebox.showinfo("Purchase Successful", message)
                self.update_top_bar()
                # Reopen trade interface if trader still has items
                if self.engine.current_trader:
                    self.show_trader_trade_interface()
            else:
                messagebox.showerror("Purchase Failed", message)

        self.create_button(qty_dialog, "Buy", do_buy, width=15, style='success').pack(pady=10)

    def sell_to_trader(self, item_id, parent_dialog):
        """Sell item to trader"""
        trader = self.engine.current_trader
        if not trader:
            return

        # Quantity dialog
        qty_dialog = tk.Toplevel(parent_dialog)
        qty_dialog.title("Sell Item")
        qty_dialog.geometry("300x150")
        qty_dialog.configure(bg=COLORS['bg_medium'])

        item_name = self.engine._get_item_name(item_id)
        max_qty = self.engine.player.ship_cargo.get(item_id, 0)

        tk.Label(
            qty_dialog,
            text=f"Sell {item_name}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        ).pack(pady=10)

        tk.Label(
            qty_dialog,
            text=f"Quantity (max {max_qty}):",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_medium']
        ).pack()

        quantity_var = tk.IntVar(value=1)
        quantity_entry = tk.Entry(
            qty_dialog,
            textvariable=quantity_var,
            font=('Arial', 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            justify='center'
        )
        quantity_entry.pack(pady=5)

        def do_sell():
            success, message = self.engine.trade_with_trader(item_id, quantity_var.get(), is_buying=False)
            if success:
                qty_dialog.destroy()
                parent_dialog.destroy()
                messagebox.showinfo("Sale Successful", message)
                self.update_top_bar()
                # Reopen trade interface if trader still exists
                if self.engine.current_trader:
                    self.show_trader_trade_interface()
            else:
                messagebox.showerror("Sale Failed", message)

        self.create_button(qty_dialog, "Sell", do_sell, width=15, style='warning').pack(pady=10)

    def show_combat_view(self):
        """Show combat interface"""
        self.clear_content()

        combat = self.engine.current_combat

        panel, content = self.create_panel(self.content_frame, "COMBAT ENGAGED")
        panel.pack(fill=tk.BOTH, expand=True)

        # Combat status
        status = combat.get_combat_status()

        status_frame = tk.Frame(content, bg=COLORS['bg_medium'])
        status_frame.pack(fill=tk.X, pady=20, padx=20)

        # Player status
        player_frame = tk.Frame(status_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
        player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            player_frame,
            text="YOUR VESSEL",
            font=('Arial', 12, 'bold'),
            fg=COLORS['success'],
            bg=COLORS['bg_light']
        ).pack(pady=10)

        tk.Label(
            player_frame,
            text=f"Hull: {status['player']['hull']}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=5)

        tk.Label(
            player_frame,
            text=f"Shields: {status['player']['shields']}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=5)

        # Enemy status
        enemy_frame = tk.Frame(status_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=2)
        enemy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            enemy_frame,
            text=status['enemy']['name'].upper(),
            font=('Arial', 12, 'bold'),
            fg=COLORS['danger'],
            bg=COLORS['bg_light']
        ).pack(pady=10)

        tk.Label(
            enemy_frame,
            text=f"Hull: {status['enemy']['hull']}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=5)

        tk.Label(
            enemy_frame,
            text=f"Shields: {status['enemy']['shields']}",
            font=('Arial', 10),
            fg=COLORS['text'],
            bg=COLORS['bg_light']
        ).pack(pady=5)

        # Combat log
        log_frame = tk.Frame(content, bg=COLORS['bg_dark'], relief=tk.SUNKEN, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        tk.Label(
            log_frame,
            text="Combat Log",
            font=('Arial', 11, 'bold'),
            fg=COLORS['accent'],
            bg=COLORS['bg_dark']
        ).pack(pady=10)

        self.combat_log = scrolledtext.ScrolledText(
            log_frame,
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            font=('Courier', 9),
            height=10,
            state='disabled'
        )
        self.combat_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Display recent log
        for entry in combat.get_combat_log(10):
            self.add_combat_log(entry)

        # Action buttons
        action_frame = tk.Frame(content, bg=COLORS['bg_medium'])
        action_frame.pack(pady=20)

        self.create_button(
            action_frame,
            "ATTACK",
            self.combat_attack,
            width=20,
            style='danger'
        ).pack(side=tk.LEFT, padx=10)

        self.create_button(
            action_frame,
            "RETREAT",
            self.combat_retreat,
            width=20,
            style='warning'
        ).pack(side=tk.LEFT, padx=10)

    def add_combat_log(self, message):
        """Add message to combat log"""
        if hasattr(self, 'combat_log'):
            self.combat_log.configure(state='normal')
            self.combat_log.insert(tk.END, f"{message}\n")
            self.combat_log.see(tk.END)
            self.combat_log.configure(state='disabled')

    def combat_attack(self):
        """Execute attack in combat"""
        combat = self.engine.current_combat
        skill_bonus = self.engine.player.get_skill_bonus("weapons_mastery", "damage")

        result = combat.player_attack(0, skill_bonus)
        self.add_combat_log(result['message'])

        if combat.is_active:
            enemy_result = combat.enemy_attack()
            self.add_combat_log(enemy_result['message'])

            if enemy_result.get("player_destroyed"):
                # Handle ship destruction and respawn
                # Clear pending travel since player is respawning at a different location
                self.engine.pending_travel_destination = None
                success, respawn_msg = self.engine.handle_ship_destruction()
                messagebox.showwarning("SHIP DESTROYED", respawn_msg)
                self.update_top_bar()
                self.show_status_view()
                return

        if result.get("enemy_destroyed"):
            credits_reward = combat.rewards["credits"]
            xp_reward = combat.rewards["xp"]
            loot = combat.rewards.get("loot", {})

            # Track level before adding XP
            old_level = self.engine.player.level

            self.engine.player.add_credits(credits_reward)
            self.engine.player.add_experience(xp_reward)
            self.engine.player.stats["enemies_destroyed"] += 1

            # Give loot to player
            loot_messages = []
            cargo_capacity = self.engine.vessel.cargo_capacity if self.engine.vessel else None
            for item_id, quantity in loot.items():
                success, message = self.engine.player.add_item(item_id, quantity, cargo_capacity)
                if success:
                    # Get item name for display
                    from data import MODULES, RESOURCES, COMMODITIES
                    if item_id in MODULES:
                        item_name = MODULES[item_id]["name"]
                    elif item_id in RESOURCES:
                        item_name = RESOURCES[item_id]["name"]
                    elif item_id in COMMODITIES:
                        item_name = COMMODITIES[item_id]["name"]
                    else:
                        item_name = item_id

                    loot_messages.append(f"{quantity}x {item_name}")
                    self.add_combat_log(f"LOOT: +{quantity}x {item_name}")
                else:
                    self.add_combat_log(f"Cargo full! Lost {quantity}x {item_id}")

            # Update contract progress for combat objectives
            for contract in self.engine.contract_board.active_contracts:
                if contract.objectives.get("type") == "destroy_enemies":
                    completed = contract.update_progress({"enemies_destroyed": 1})
                    if completed:
                        # Auto-pay immediately
                        self.engine.player.add_credits(contract.reward)
                        contract_xp = int(contract.reward / 10)
                        self.engine.player.add_experience(contract_xp)
                        self.engine.player.stats['contracts_completed'] += 1
                        self.add_combat_log(f"CONTRACT COMPLETE! {contract.name} | +{contract.reward:,} CR +{contract_xp} XP")

            self.add_combat_log(f"VICTORY! Earned {credits_reward:,} CR + {xp_reward} XP")
            self.engine.current_combat = None

            # Check for level up
            if self.engine.player.level > old_level:
                levels_gained = self.engine.player.level - old_level
                messagebox.showinfo(
                    "LEVEL UP!",
                    f"Congratulations! You reached Level {self.engine.player.level}!\n"
                    f"({'Multiple' if levels_gained > 1 else 'One'} level{'s' if levels_gained > 1 else ''} gained!)"
                )

            # Build victory message with loot
            victory_msg = f"Enemy destroyed!\n\nRewards:\n{credits_reward:,} CR\n{xp_reward} XP"
            if loot_messages:
                victory_msg += "\n\nLoot:\n" + "\n".join(loot_messages)
            else:
                victory_msg += "\n\nNo loot dropped"

            messagebox.showinfo("Victory!", victory_msg)
            self.update_top_bar()

            # Check for pending travel after combat
            if self.engine.pending_travel_destination:
                destination_id = self.engine.pending_travel_destination
                self.engine.pending_travel_destination = None

                # Complete the travel
                self.engine.player.location = destination_id
                self.engine.player.stats["distance_traveled"] += 100
                self.engine.player.visited_locations.add(destination_id)
                self.engine.contract_board.generate_contracts(destination_id)

                from data import LOCATIONS
                dest_name = LOCATIONS[destination_id]["name"]
                messagebox.showinfo("Travel", f"Traveled to {dest_name}")
                self.refresh_navigation()
                self.show_travel_view()
            else:
                self.show_status_view()
        else:
            combat.next_turn()
            self.show_combat_view()

    def combat_retreat(self):
        """Attempt to retreat from combat"""
        combat = self.engine.current_combat
        result = combat.attempt_retreat()
        self.add_combat_log(result['message'])

        if result.get('retreated'):
            self.engine.current_combat = None
            # Clear pending travel if retreating from combat (don't complete the travel)
            self.engine.pending_travel_destination = None
            messagebox.showinfo("Retreat", "Successfully retreated from combat")
            self.show_status_view()
        elif 'enemy_attack' in result:
            enemy_result = result['enemy_attack']
            self.add_combat_log(enemy_result['message'])

            # Check if player was destroyed during failed retreat
            if enemy_result.get("player_destroyed"):
                # Clear pending travel since player is respawning at a different location
                self.engine.pending_travel_destination = None
                success, respawn_msg = self.engine.handle_ship_destruction()
                messagebox.showwarning("SHIP DESTROYED", respawn_msg)
                self.update_top_bar()
                self.show_status_view()
                return

            self.show_combat_view()

    def save_game(self):
        """Save current game"""
        if self.engine.save_current_game():
            messagebox.showinfo("Save Game", "Game saved successfully!")
        else:
            messagebox.showerror("Save Error", "Failed to save game")

    def update_top_bar(self):
        """Update top bar info"""
        if hasattr(self, 'player_name_label'):
            self.player_name_label.config(text=f"CMDR {self.engine.player.name.upper()}")
            self.level_label.config(text=f"LVL {self.engine.player.level}")

            # Update XP display
            xp_progress = (self.engine.player.experience / self.engine.player.experience_to_next) * 100
            self.xp_label.config(text=f"{int(xp_progress)}%")
            self.xp_progress_bar.config(width=int(xp_progress))

            self.credits_label.config(text=f"{self.engine.player.credits:,} CR")
            self.location_label.config(text=f"{LOCATIONS[self.engine.player.location]['name'].upper()}")

            # Update cargo display with color coding
            if hasattr(self, 'cargo_label'):
                cargo_used = self.engine.player.get_cargo_volume()
                cargo_capacity = self.engine.vessel.cargo_capacity
                cargo_percent = (cargo_used / cargo_capacity * 100) if cargo_capacity > 0 else 0
                cargo_color = COLORS['success'] if cargo_percent < 70 else COLORS['warning'] if cargo_percent < 90 else COLORS['danger']
                self.cargo_label.config(
                    text=f"{cargo_used:.0f}/{cargo_capacity:.0f} ({cargo_percent:.0f}%)",
                    fg=cargo_color
                )

    def show_notification(self, message: str, notification_type: str = "info"):
        """Show a notification that fades out after a few seconds"""
        if not self.notification_container:
            return

        # Color based on type
        color_map = {
            "info": COLORS['accent'],
            "success": COLORS['success'],
            "warning": COLORS['warning'],
            "danger": COLORS['danger']
        }
        color = color_map.get(notification_type, COLORS['accent'])

        # Create notification frame
        notif_frame = tk.Frame(
            self.notification_container,
            bg=COLORS['bg_light'],
            relief=tk.RIDGE,
            bd=2,
            highlightthickness=2,
            highlightbackground=color
        )
        notif_frame.pack(fill=tk.X, pady=2)

        # Icon based on type
        icon_map = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "danger": "✗"
        }
        icon = icon_map.get(notification_type, "•")

        # Create label
        label = tk.Label(
            notif_frame,
            text=f"{icon} {message}",
            font=('Arial', 10, 'bold'),
            fg=color,
            bg=COLORS['bg_light'],
            padx=15,
            pady=8
        )
        label.pack()

        # Store reference
        self.active_notifications.append(notif_frame)

        # Auto-dismiss after 5 seconds
        def dismiss():
            if notif_frame.winfo_exists():
                notif_frame.destroy()
                if notif_frame in self.active_notifications:
                    self.active_notifications.remove(notif_frame)
                # Force refresh the notification container to clear visual artifacts
                if self.notification_container and self.notification_container.winfo_exists():
                    self.notification_container.update_idletasks()

        self.root.after(5000, dismiss)

    def check_skill_completions(self):
        """Check for newly completed skills and show notifications"""
        if not self.engine.player:
            return

        # Get current training state
        current_training = set()
        if self.engine.player.skill_training:
            for training in self.engine.player.skill_training:
                current_training.add(training["skill_id"])

        # Detect completed skills (was training, now not)
        completed = self.last_training_state - current_training

        # Show notifications for completed skills
        for skill_id in completed:
            if skill_id in SKILLS:
                skill_name = SKILLS[skill_id]["name"]
                level = self.engine.player.get_skill_level(skill_id)
                self.root.after(0, lambda sn=skill_name, lv=level:
                    self.show_notification(f"{sn} trained to level {lv}!", "success"))

        # Update state
        self.last_training_state = current_training

    def game_update_loop(self):
        """Background thread to update game state"""
        while self.update_running:
            if self.engine.player:
                self.engine.update_game_state()

                # Check for skill completions and show notifications
                self.check_skill_completions()

                # Update UI on main thread
                self.root.after(0, self.update_top_bar)

                # Update status training panel if on status view (live progress bars)
                if hasattr(self, 'current_view') and self.current_view == "status":
                    self.root.after(0, self.update_status_training_panel)

            time.sleep(1)

    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        """Handle window close"""
        self.update_running = False

        if self.engine.player:
            if messagebox.askyesno("Quit", "Save game before exiting?"):
                self.engine.save_current_game()

        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = VoidDominionGUI(root)
    app.run()


if __name__ == "__main__":
    main()
