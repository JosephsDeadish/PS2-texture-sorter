#!/usr/bin/env python3
"""
Demo script to visualize the new System & Debug section in Settings
This creates a mock settings window showing the new features
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Simulate the directory paths
HOME = Path.home()
CONFIG_DIR = HOME / ".ps2_texture_sorter"
LOGS_DIR = CONFIG_DIR / "logs"
CACHE_DIR = CONFIG_DIR / "cache"

def create_demo_window():
    """Create a demo window showing the new System & Debug section"""
    
    root = tk.Tk()
    root.title("Settings - System & Debug Section Demo")
    root.geometry("900x600")
    
    # Title
    title = tk.Label(root, text="🐼 Application Settings 🐼", font=("Arial", 18, "bold"))
    title.pack(pady=15)
    
    # Create a frame to hold the scrollable content
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Add some dummy sections to show context
    sections = [
        ("⚡ Performance Settings", "bg1"),
        ("🎨 Appearance & Customization", "bg2"),
        ("📁 File Handling", "bg1"),
        ("📋 Logging", "bg2"),
        ("🔔 Notifications", "bg1"),
    ]
    
    colors = {"bg1": "#e0e0e0", "bg2": "#f0f0f0"}
    
    for section_name, bg_color in sections:
        frame = tk.Frame(scrollable_frame, bg=colors[bg_color], relief="ridge", borderwidth=2)
        frame.pack(fill="x", padx=10, pady=5)
        label = tk.Label(frame, text=section_name, font=("Arial", 12, "bold"), 
                        bg=colors[bg_color], anchor="w")
        label.pack(anchor="w", padx=10, pady=5)
        content = tk.Label(frame, text="   [Settings content here...]", 
                          bg=colors[bg_color], anchor="w", fg="gray")
        content.pack(anchor="w", padx=20, pady=3)
    
    # === NEW SYSTEM & DEBUG SECTION ===
    system_frame = tk.Frame(scrollable_frame, bg="#fff0f0", relief="ridge", borderwidth=3)
    system_frame.pack(fill="x", padx=10, pady=10)
    
    # Section header with highlight
    header = tk.Label(system_frame, text="🛠️ System & Debug  [NEW!]", 
                     font=("Arial", 14, "bold"), bg="#fff0f0", fg="#d00000")
    header.pack(anchor="w", padx=10, pady=5)
    
    # Description
    desc = tk.Label(system_frame, 
                   text="Access application directories and diagnostic information",
                   font=("Arial", 9, "italic"), bg="#fff0f0", fg="#555")
    desc.pack(anchor="w", padx=20, pady=(0, 5))
    
    # Buttons frame
    buttons_frame = tk.Frame(system_frame, bg="#fff0f0")
    buttons_frame.pack(fill="x", padx=10, pady=5)
    
    def show_action(action):
        result = tk.Label(system_frame, text=f"✅ {action}", 
                         font=("Arial", 9), bg="#e0ffe0", fg="green")
        result.pack(anchor="w", padx=20, pady=2)
        root.after(3000, result.destroy)
    
    btn1 = tk.Button(buttons_frame, text="📁 Open Logs Directory", 
                    command=lambda: show_action(f"Opened: {LOGS_DIR}"),
                    bg="#4CAF50", fg="white", font=("Arial", 10), 
                    relief="raised", padx=10, pady=8, cursor="hand2")
    btn1.pack(side="left", padx=5)
    
    btn2 = tk.Button(buttons_frame, text="📁 Open Config Directory", 
                    command=lambda: show_action(f"Opened: {CONFIG_DIR}"),
                    bg="#2196F3", fg="white", font=("Arial", 10), 
                    relief="raised", padx=10, pady=8, cursor="hand2")
    btn2.pack(side="left", padx=5)
    
    btn3 = tk.Button(buttons_frame, text="📁 Open Cache Directory", 
                    command=lambda: show_action(f"Opened: {CACHE_DIR}"),
                    bg="#FF9800", fg="white", font=("Arial", 10), 
                    relief="raised", padx=10, pady=8, cursor="hand2")
    btn3.pack(side="left", padx=5)
    
    # Directory paths display
    paths_frame = tk.Frame(system_frame, bg="#f8f8f8", relief="sunken", borderwidth=1)
    paths_frame.pack(fill="x", padx=10, pady=5)
    
    paths_title = tk.Label(paths_frame, text="Application Data Locations:", 
                          font=("Arial", 10, "bold"), bg="#f8f8f8")
    paths_title.pack(anchor="w", padx=10, pady=(5, 0))
    
    paths = [
        ("• Logs:", str(LOGS_DIR)),
        ("• Config:", str(CONFIG_DIR)),
        ("• Cache:", str(CACHE_DIR))
    ]
    
    for label, path in paths:
        path_frame = tk.Frame(paths_frame, bg="#f8f8f8")
        path_frame.pack(fill="x", padx=20)
        
        tk.Label(path_frame, text=label, font=("Arial", 9), 
                bg="#f8f8f8", width=10, anchor="w").pack(side="left")
        tk.Label(path_frame, text=path, font=("Arial", 9), 
                bg="#f8f8f8", fg="#666").pack(side="left", anchor="w")
    
    tk.Label(paths_frame, text=" ", bg="#f8f8f8").pack(pady=(0, 5))
    
    # Add a note about the feature
    note_frame = tk.Frame(system_frame, bg="#fffacd", relief="ridge", borderwidth=1)
    note_frame.pack(fill="x", padx=10, pady=5)
    
    note = tk.Label(note_frame, 
                   text="ℹ️  These buttons will open the directories in your file explorer.\n"
                        "Use this to access crash logs, configuration files, and cached data.",
                   font=("Arial", 9), bg="#fffacd", fg="#333", justify="left")
    note.pack(padx=10, pady=8)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
    scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 20))
    
    # Save button at bottom
    save_btn = tk.Button(root, text="💾 Save Settings", 
                        font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                        padx=20, pady=10, cursor="hand2")
    save_btn.pack(pady=10)
    
    # Instructions label
    info = tk.Label(root, 
                   text="This demo shows the new System & Debug section in the Settings window.\n"
                        "Click the buttons to see how they work!",
                   font=("Arial", 9, "italic"), fg="gray")
    info.pack(pady=(0, 10))
    
    root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("Settings Window - System & Debug Section Demo")
    print("=" * 60)
    print()
    print("This demo shows the NEW System & Debug section that has been")
    print("added to the Settings window.")
    print()
    print("Features demonstrated:")
    print("  • Button to open Logs directory")
    print("  • Button to open Config directory")
    print("  • Button to open Cache directory")
    print("  • Display of directory paths")
    print()
    print("Opening demo window...")
    print()
    
    create_demo_window()
