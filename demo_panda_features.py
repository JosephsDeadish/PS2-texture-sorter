"""
Demo application for new panda features
Shows mini-games, widgets, closet, and multi-language support
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import tkinter as tk
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
except ImportError:
    ctk = None
    print("Warning: customtkinter not available, using standard tkinter")

from src.features.minigame_system import MiniGameManager
from src.features.panda_widgets import WidgetCollection
from src.features.panda_closet import PandaCloset
from src.features.translation_manager import TranslationManager, Language
from src.features.hotkey_manager import HotkeyManager
from src.ui.minigame_panel import MiniGamePanel
from src.ui.widgets_panel import WidgetsPanel
from src.ui.closet_panel import ClosetPanel
from src.ui.hotkey_settings_panel import HotkeySettingsPanel


class PandaFeaturesDemo(ctk.CTk if ctk else tk.Tk):
    """Demo application for panda features."""
    
    def __init__(self):
        """Initialize demo app."""
        super().__init__()
        
        self.title("Panda Features Demo - PS2 Texture Sorter")
        self.geometry("1200x800")
        
        # Initialize systems
        self.minigame_manager = MiniGameManager()
        self.widget_collection = WidgetCollection()
        self.panda_closet = PandaCloset()
        self.translation_manager = TranslationManager()
        self.hotkey_manager = HotkeyManager()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create UI widgets."""
        # Title bar
        title_frame = ctk.CTkFrame(self) if ctk else tk.Frame(self)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            title_frame,
            text="🐼 Panda Features Demo",
            font=("Arial", 24, "bold")
        ) if ctk else tk.Label(
            title_frame,
            text="🐼 Panda Features Demo",
            font=("Arial", 24, "bold")
        )
        title.pack(side="left", padx=20)
        
        # Language selector
        lang_label = ctk.CTkLabel(
            title_frame,
            text="Language:",
            font=("Arial", 12)
        ) if ctk else tk.Label(
            title_frame,
            text="Language:",
            font=("Arial", 12)
        )
        lang_label.pack(side="right", padx=5)
        
        self.lang_var = tk.StringVar(value="en")
        if ctk:
            lang_menu = ctk.CTkOptionMenu(
                title_frame,
                variable=self.lang_var,
                values=["en", "es", "fr"],
                command=self._change_language
            )
        else:
            lang_menu = tk.OptionMenu(
                title_frame,
                self.lang_var,
                "en", "es", "fr",
                command=self._change_language
            )
        lang_menu.pack(side="right", padx=5)
        
        # Tabview for different features
        if ctk:
            self.tabview = ctk.CTkTabview(self)
            self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            
            # Add tabs
            self.tabview.add("Mini-Games")
            self.tabview.add("Widgets")
            self.tabview.add("Closet")
            self.tabview.add("Hotkeys")
            self.tabview.add("About")
            
            # Populate tabs
            self.minigame_panel = MiniGamePanel(
                self.tabview.tab("Mini-Games"),
                self.minigame_manager
            )
            self.minigame_panel.pack(fill="both", expand=True)
            
            self.widgets_panel = WidgetsPanel(
                self.tabview.tab("Widgets"),
                self.widget_collection
            )
            self.widgets_panel.pack(fill="both", expand=True)
            
            self.closet_panel = ClosetPanel(
                self.tabview.tab("Closet"),
                self.panda_closet
            )
            self.closet_panel.pack(fill="both", expand=True)
            
            self.hotkey_panel = HotkeySettingsPanel(
                self.tabview.tab("Hotkeys"),
                self.hotkey_manager
            )
            self.hotkey_panel.pack(fill="both", expand=True)
            
            self._create_about_tab(self.tabview.tab("About"))
        else:
            # Fallback to notebook for regular tkinter
            import tkinter.ttk as ttk
            self.notebook = ttk.Notebook(self)
            self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            
            # Create frames for each tab
            minigame_frame = tk.Frame(self.notebook)
            widgets_frame = tk.Frame(self.notebook)
            closet_frame = tk.Frame(self.notebook)
            hotkey_frame = tk.Frame(self.notebook)
            about_frame = tk.Frame(self.notebook)
            
            self.notebook.add(minigame_frame, text="Mini-Games")
            self.notebook.add(widgets_frame, text="Widgets")
            self.notebook.add(closet_frame, text="Closet")
            self.notebook.add(hotkey_frame, text="Hotkeys")
            self.notebook.add(about_frame, text="About")
            
            # Populate tabs
            self.minigame_panel = MiniGamePanel(minigame_frame, self.minigame_manager)
            self.minigame_panel.pack(fill="both", expand=True)
            
            self.widgets_panel = WidgetsPanel(widgets_frame, self.widget_collection)
            self.widgets_panel.pack(fill="both", expand=True)
            
            self.closet_panel = ClosetPanel(closet_frame, self.panda_closet)
            self.closet_panel.pack(fill="both", expand=True)
            
            self.hotkey_panel = HotkeySettingsPanel(hotkey_frame, self.hotkey_manager)
            self.hotkey_panel.pack(fill="both", expand=True)
            
            self._create_about_tab(about_frame)
    
    def _create_about_tab(self, parent):
        """Create the about tab."""
        about_text = """
🐼 PS2 Texture Sorter - Panda Features

This demo showcases the new features added to the PS2 Texture Sorter:

✨ Features Implemented:

1. 🎮 Mini-Games System
   - Panda Click Challenge: Click as fast as you can!
   - Panda Memory Match: Match emoji pairs
   - Panda Reflex Test: Test your reaction time
   - Difficulty levels: Easy, Medium, Hard, Extreme
   - XP and currency rewards

2. 🎾 Panda Widgets
   - Interactive toys (ball, stick, plushie, etc.)
   - Food items (bamboo, treats, etc.)
   - Accessories (sunglasses, bowtie, etc.)
   - Rarity system (Common to Legendary)
   - Track usage statistics

3. 👔 Panda Closet
   - Customize fur style and color
   - Dress up with clothing, hats, shoes
   - Add accessories
   - Save and load appearances
   - Purchase system with currency

4. ⌨️ Customizable Hotkeys
   - Rebind keyboard shortcuts
   - Category-based organization
   - Conflict detection
   - Save/load configurations

5. 🌍 Multi-Language Support
   - English, Spanish, French translations
   - Easy language switching
   - Extensible translation system

6. 🎨 Additional Panda Animations
   - Playing, eating, customizing
   - Sleeping, gaming, thinking
   - Integrated with widget interactions

Author: Dead On The Inside / JosephsDeadish
Repository: github.com/JosephsDeadish/PS2-texture-sorter
"""
        
        text_widget = ctk.CTkTextbox(
            parent,
            font=("Arial", 12),
            wrap="word"
        ) if ctk else tk.Text(
            parent,
            font=("Arial", 12),
            wrap="word"
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        text_widget.insert("1.0", about_text)
        
        if ctk:
            text_widget.configure(state="disabled")
        else:
            text_widget.config(state="disabled")
    
    def _change_language(self, lang_code: str):
        """Change the application language."""
        lang_map = {
            'en': Language.ENGLISH,
            'es': Language.SPANISH,
            'fr': Language.FRENCH
        }
        
        language = lang_map.get(lang_code, Language.ENGLISH)
        self.translation_manager.set_language(language)
        
        print(f"Language changed to: {language.value}")
        # In a full implementation, this would update all UI text


def main():
    """Run the demo application."""
    app = PandaFeaturesDemo()
    app.mainloop()


if __name__ == '__main__':
    main()
