"""
Scrollable Tab View Widget
A custom tabview that supports scrolling when too many tabs are present
"""

import customtkinter as ctk
from typing import Dict, List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class ScrollableTabView(ctk.CTkFrame):
    """
    A tabview that supports horizontal scrolling for many tabs.
    Uses arrow buttons to scroll through tabs when they don't all fit.
    """
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tabs: Dict[str, ctk.CTkFrame] = {}
        self.tab_buttons: Dict[str, ctk.CTkButton] = {}
        self.current_tab: Optional[str] = None
        self.visible_tab_range = [0, 10]  # Show first 10 tabs
        self.max_visible_tabs = 10
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the scrollable tab structure."""
        # Top bar with scroll buttons and tab buttons
        self.tab_bar = ctk.CTkFrame(self, height=40)
        self.tab_bar.pack(side="top", fill="x", padx=2, pady=2)
        
        # Left scroll button
        self.scroll_left_btn = ctk.CTkButton(
            self.tab_bar,
            text="◀",
            width=30,
            command=self._scroll_left,
            fg_color="gray30",
            hover_color="gray20"
        )
        self.scroll_left_btn.pack(side="left", padx=2)
        
        # Tab button container (scrollable)
        self.tab_button_frame = ctk.CTkFrame(self.tab_bar)
        self.tab_button_frame.pack(side="left", fill="x", expand=True, padx=2)
        
        # Right scroll button
        self.scroll_right_btn = ctk.CTkButton(
            self.tab_bar,
            text="▶",
            width=30,
            command=self._scroll_right,
            fg_color="gray30",
            hover_color="gray20"
        )
        self.scroll_right_btn.pack(side="right", padx=2)
        
        # Content area where tab content is displayed
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True)
        
        # Update scroll button states
        self._update_scroll_buttons()
    
    def add(self, name: str) -> ctk.CTkFrame:
        """
        Add a new tab.
        
        Args:
            name: Name of the tab
            
        Returns:
            Frame for the tab content
        """
        # Create tab content frame
        tab_frame = ctk.CTkFrame(self.content_frame)
        self.tabs[name] = tab_frame
        
        # Create tab button
        tab_button = ctk.CTkButton(
            self.tab_button_frame,
            text=name,
            command=lambda: self.set(name),
            width=120,
            height=32,
            corner_radius=6
        )
        self.tab_buttons[name] = tab_button
        
        # Update button visibility
        self._update_visible_tabs()
        
        # If this is the first tab, select it
        if len(self.tabs) == 1:
            self.set(name)
        
        return tab_frame
    
    def set(self, name: str):
        """
        Switch to a specific tab.
        
        Args:
            name: Name of the tab to switch to
        """
        if name not in self.tabs:
            logger.warning(f"Tab '{name}' not found")
            return
        
        # Hide current tab
        if self.current_tab and self.current_tab in self.tabs:
            self.tabs[self.current_tab].pack_forget()
            # Reset button color
            if self.current_tab in self.tab_buttons:
                self.tab_buttons[self.current_tab].configure(
                    fg_color=["gray75", "gray25"],
                    hover_color=["gray70", "gray30"]
                )
        
        # Show new tab
        self.current_tab = name
        self.tabs[name].pack(fill="both", expand=True)
        
        # Highlight button
        if name in self.tab_buttons:
            self.tab_buttons[name].configure(
                fg_color=["#3B8ED0", "#1F6AA5"],
                hover_color=["#36719F", "#144870"]
            )
        
        # Ensure tab is visible
        self._ensure_tab_visible(name)
    
    def get(self, name: str) -> Optional[ctk.CTkFrame]:
        """Get a tab frame by name."""
        return self.tabs.get(name)
    
    def _scroll_left(self):
        """Scroll tabs to the left (show earlier tabs)."""
        if self.visible_tab_range[0] > 0:
            self.visible_tab_range[0] -= 1
            self.visible_tab_range[1] -= 1
            self._update_visible_tabs()
    
    def _scroll_right(self):
        """Scroll tabs to the right (show later tabs)."""
        if self.visible_tab_range[1] < len(self.tabs):
            self.visible_tab_range[0] += 1
            self.visible_tab_range[1] += 1
            self._update_visible_tabs()
    
    def _update_visible_tabs(self):
        """Update which tab buttons are visible based on scroll position."""
        tab_names = list(self.tabs.keys())
        
        # Hide all buttons first
        for button in self.tab_buttons.values():
            button.pack_forget()
        
        # Show only visible range
        start, end = self.visible_tab_range
        for i in range(start, min(end, len(tab_names))):
            if tab_names[i] in self.tab_buttons:
                self.tab_buttons[tab_names[i]].pack(side="left", padx=2)
        
        self._update_scroll_buttons()
    
    def _update_scroll_buttons(self):
        """Enable/disable scroll buttons based on position."""
        # Disable left if at start
        if self.visible_tab_range[0] == 0:
            self.scroll_left_btn.configure(state="disabled")
        else:
            self.scroll_left_btn.configure(state="normal")
        
        # Disable right if at end
        if self.visible_tab_range[1] >= len(self.tabs):
            self.scroll_right_btn.configure(state="disabled")
        else:
            self.scroll_right_btn.configure(state="normal")
    
    def _ensure_tab_visible(self, name: str):
        """Ensure a specific tab button is visible."""
        tab_names = list(self.tabs.keys())
        if name not in tab_names:
            return
        
        tab_index = tab_names.index(name)
        
        # If tab is before visible range, scroll to it
        if tab_index < self.visible_tab_range[0]:
            self.visible_tab_range[0] = tab_index
            self.visible_tab_range[1] = tab_index + self.max_visible_tabs
            self._update_visible_tabs()
        # If tab is after visible range, scroll to it
        elif tab_index >= self.visible_tab_range[1]:
            self.visible_tab_range[1] = tab_index + 1
            self.visible_tab_range[0] = max(0, self.visible_tab_range[1] - self.max_visible_tabs)
            self._update_visible_tabs()


class CompactTabView(ctk.CTkFrame):
    """
    A compact tabview that uses a dropdown selector for many tabs.
    Better for very large numbers of tabs (15+).
    """
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tabs: Dict[str, ctk.CTkFrame] = {}
        self.current_tab: Optional[str] = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the compact tab structure."""
        # Top bar with dropdown selector
        self.tab_bar = ctk.CTkFrame(self, height=40)
        self.tab_bar.pack(side="top", fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(
            self.tab_bar,
            text="Tab:",
            font=("Arial Bold", 12)
        ).pack(side="left", padx=5)
        
        # Dropdown for tab selection
        self.tab_dropdown = ctk.CTkOptionMenu(
            self.tab_bar,
            values=["Select a tab..."],
            command=self._on_tab_selected,
            width=200
        )
        self.tab_dropdown.pack(side="left", padx=5)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True)
    
    def add(self, name: str) -> ctk.CTkFrame:
        """Add a new tab."""
        # Create tab content frame
        tab_frame = ctk.CTkFrame(self.content_frame)
        self.tabs[name] = tab_frame
        
        # Update dropdown
        self.tab_dropdown.configure(values=list(self.tabs.keys()))
        
        # If this is the first tab, select it
        if len(self.tabs) == 1:
            self.set(name)
            self.tab_dropdown.set(name)
        
        return tab_frame
    
    def set(self, name: str):
        """Switch to a specific tab."""
        if name not in self.tabs:
            return
        
        # Hide current tab
        if self.current_tab and self.current_tab in self.tabs:
            self.tabs[self.current_tab].pack_forget()
        
        # Show new tab
        self.current_tab = name
        self.tabs[name].pack(fill="both", expand=True)
        self.tab_dropdown.set(name)
    
    def get(self, name: str) -> Optional[ctk.CTkFrame]:
        """Get a tab frame by name."""
        return self.tabs.get(name)
    
    def _on_tab_selected(self, value: str):
        """Handle tab selection from dropdown."""
        self.set(value)
