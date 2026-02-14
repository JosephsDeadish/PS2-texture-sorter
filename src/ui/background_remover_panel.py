"""
Background Remover UI Panel
Provides UI for AI-based background removal with edge refinement controls
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import List, Optional, Callable
import logging
from PIL import Image

from src.tools.background_remover import BackgroundRemover, check_dependencies

logger = logging.getLogger(__name__)


class BackgroundRemoverPanel(ctk.CTkFrame):
    """
    UI panel for background removal operations with one-click processing,
    batch support, and edge refinement controls.
    """
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Initialize background remover
        self.remover = BackgroundRemover()
        self.selected_files: List[str] = []
        self.output_directory: Optional[str] = None
        self.processing_thread = None
        
        self._create_widgets()
        self._check_availability()
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🎭 AI Background Remover",
            font=("Arial Bold", 18)
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = ctk.CTkLabel(
            self,
            text="One-click subject isolation with transparent PNG export",
            font=("Arial", 12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Status frame
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Checking dependencies...",
            font=("Arial", 11)
        )
        self.status_label.pack(pady=5)
        
        # File selection frame
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(file_frame, text="📁 Input Files:", font=("Arial Bold", 12)).pack(anchor="w", padx=10, pady=(10, 5))
        
        btn_frame = ctk.CTkFrame(file_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.select_files_btn = ctk.CTkButton(
            btn_frame,
            text="Select Images",
            command=self._select_files,
            width=150
        )
        self.select_files_btn.pack(side="left", padx=5)
        
        self.select_folder_btn = ctk.CTkButton(
            btn_frame,
            text="Select Folder",
            command=self._select_folder,
            width=150
        )
        self.select_folder_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear Selection",
            command=self._clear_selection,
            width=150,
            fg_color="gray40"
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # File list
        self.file_list_label = ctk.CTkLabel(
            file_frame,
            text="No files selected",
            font=("Arial", 10),
            text_color="gray"
        )
        self.file_list_label.pack(anchor="w", padx=10, pady=5)
        
        # Output directory frame
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(output_frame, text="📂 Output Directory:", font=("Arial Bold", 12)).pack(anchor="w", padx=10, pady=(10, 5))
        
        output_btn_frame = ctk.CTkFrame(output_frame)
        output_btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.select_output_btn = ctk.CTkButton(
            output_btn_frame,
            text="Select Output Folder",
            command=self._select_output_directory,
            width=200
        )
        self.select_output_btn.pack(side="left", padx=5)
        
        self.output_label = ctk.CTkLabel(
            output_btn_frame,
            text="(Same as input)",
            font=("Arial", 10),
            text_color="gray"
        )
        self.output_label.pack(side="left", padx=10)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(settings_frame, text="⚙️ Settings:", font=("Arial Bold", 12)).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Edge refinement slider
        edge_frame = ctk.CTkFrame(settings_frame)
        edge_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(edge_frame, text="Edge Refinement:", width=120).pack(side="left", padx=5)
        
        self.edge_slider = ctk.CTkSlider(
            edge_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            command=self._on_edge_refinement_change
        )
        self.edge_slider.set(0.5)
        self.edge_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.edge_value_label = ctk.CTkLabel(edge_frame, text="50%", width=50)
        self.edge_value_label.pack(side="left", padx=5)
        
        # Model selection
        model_frame = ctk.CTkFrame(settings_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(model_frame, text="AI Model:", width=120).pack(side="left", padx=5)
        
        self.model_var = ctk.StringVar(value="u2net")
        self.model_menu = ctk.CTkOptionMenu(
            model_frame,
            variable=self.model_var,
            values=self.remover.get_supported_models(),
            command=self._on_model_change
        )
        self.model_menu.pack(side="left", fill="x", expand=True, padx=5)
        
        # Alpha matting checkbox
        self.alpha_matting_var = ctk.BooleanVar(value=False)
        self.alpha_matting_check = ctk.CTkCheckBox(
            settings_frame,
            text="Enable Alpha Matting (Better edges, slower)",
            variable=self.alpha_matting_var
        )
        self.alpha_matting_check.pack(anchor="w", padx=10, pady=5)
        
        # Progress frame
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="",
            font=("Arial", 10)
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        self.process_btn = ctk.CTkButton(
            action_frame,
            text="🚀 Remove Backgrounds",
            command=self._process_images,
            height=40,
            font=("Arial Bold", 14),
            fg_color="#2B7A0B",
            hover_color="#1F5808"
        )
        self.process_btn.pack(fill="x", padx=10, pady=5)
        
        self.cancel_btn = ctk.CTkButton(
            action_frame,
            text="Cancel",
            command=self._cancel_processing,
            height=30,
            fg_color="gray40",
            state="disabled"
        )
        self.cancel_btn.pack(fill="x", padx=10, pady=5)
    
    def _check_availability(self):
        """Check if background removal is available."""
        deps = check_dependencies()
        
        if deps['rembg']:
            self.status_label.configure(
                text="✓ AI Background Removal Available",
                text_color="green"
            )
        else:
            self.status_label.configure(
                text="✗ Background removal not available. Install with: pip install rembg",
                text_color="red"
            )
            self.process_btn.configure(state="disabled")
            self.select_files_btn.configure(state="disabled")
            self.select_folder_btn.configure(state="disabled")
        
        if not deps['opencv']:
            logger.warning("OpenCV not available - advanced edge refinement disabled")
    
    def _select_files(self):
        """Open file dialog to select images."""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self._update_file_list()
    
    def _select_folder(self):
        """Open folder dialog to select all images in a folder."""
        folder = filedialog.askdirectory(title="Select Folder with Images")
        
        if folder:
            folder_path = Path(folder)
            image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
            self.selected_files = [
                str(f) for f in folder_path.iterdir()
                if f.suffix.lower() in image_extensions
            ]
            self._update_file_list()
    
    def _clear_selection(self):
        """Clear selected files."""
        self.selected_files = []
        self._update_file_list()
    
    def _update_file_list(self):
        """Update the file list label."""
        count = len(self.selected_files)
        if count == 0:
            self.file_list_label.configure(text="No files selected", text_color="gray")
        elif count == 1:
            filename = Path(self.selected_files[0]).name
            self.file_list_label.configure(
                text=f"1 file selected: {filename}",
                text_color="white"
            )
        else:
            self.file_list_label.configure(
                text=f"{count} files selected",
                text_color="white"
            )
    
    def _select_output_directory(self):
        """Select output directory."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        
        if folder:
            self.output_directory = folder
            self.output_label.configure(
                text=f".../{Path(folder).name}",
                text_color="white"
            )
    
    def _on_edge_refinement_change(self, value):
        """Handle edge refinement slider change."""
        value = float(value)
        self.remover.set_edge_refinement(value)
        self.edge_value_label.configure(text=f"{int(value * 100)}%")
    
    def _on_model_change(self, model_name):
        """Handle model selection change."""
        success = self.remover.change_model(model_name)
        if not success:
            messagebox.showerror("Error", f"Failed to load model: {model_name}")
    
    def _process_images(self):
        """Start background removal processing."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select images to process")
            return
        
        # Disable buttons
        self.process_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.select_files_btn.configure(state="disabled")
        self.select_folder_btn.configure(state="disabled")
        
        # Start async processing
        self.processing_thread = self.remover.batch_process_async(
            input_paths=self.selected_files,
            output_dir=self.output_directory,
            progress_callback=self._on_progress,
            completion_callback=self._on_completion,
            alpha_matting=self.alpha_matting_var.get()
        )
    
    def _on_progress(self, current: int, total: int, filename: str):
        """Handle progress updates."""
        progress = current / total
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"Processing {current}/{total}: {filename}"
        )
    
    def _on_completion(self, results):
        """Handle processing completion."""
        # Re-enable buttons
        self.process_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.select_files_btn.configure(state="normal")
        self.select_folder_btn.configure(state="normal")
        
        # Show results
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        total_time = sum(r.processing_time for r in results)
        
        self.progress_label.configure(
            text=f"Complete! {successful} successful, {failed} failed ({total_time:.1f}s total)"
        )
        
        messagebox.showinfo(
            "Processing Complete",
            f"Background removal complete!\n\n"
            f"Successful: {successful}\n"
            f"Failed: {failed}\n"
            f"Total time: {total_time:.1f} seconds"
        )
    
    def _cancel_processing(self):
        """Cancel ongoing processing."""
        self.remover.cancel_processing()
        self.progress_label.configure(text="Cancelling...")
        self.cancel_btn.configure(state="disabled")


def open_background_remover_dialog(parent=None):
    """Open background remover as a standalone dialog."""
    dialog = ctk.CTkToplevel(parent)
    dialog.title("AI Background Remover")
    dialog.geometry("700x800")
    
    if parent:
        dialog.transient(parent)
    
    panel = BackgroundRemoverPanel(dialog)
    panel.pack(fill="both", expand=True, padx=10, pady=10)
    
    return dialog


if __name__ == "__main__":
    # Test the panel
    app = ctk.CTk()
    app.title("Background Remover Test")
    app.geometry("700x800")
    
    panel = BackgroundRemoverPanel(app)
    panel.pack(fill="both", expand=True, padx=10, pady=10)
    
    app.mainloop()
