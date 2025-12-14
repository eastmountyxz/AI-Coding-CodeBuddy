import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from typing import Tuple, Optional

# Pillow resampling compatibility
try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS  # Pillow >= 9.1.0
except AttributeError:
    RESAMPLE_LANCZOS = getattr(Image, "LANCZOS", Image.BICUBIC)


class ImageApp(tk.Tk):
    """
    AI Image Processing System main window.
    Layout:
      - Top: controls frame with 8 buttons
      - Bottom: image display area
    """

    def __init__(self):
        super().__init__()

        # Window config
        self.title("AI Image Processing System")
        self.minsize(900, 600)

        # State
        self.original_image = None  # PIL.Image
        self._photo_image = None  # ImageTk.PhotoImage cache to avoid GC
        self._current_image_path = None

        # Build UI
        self._build_ui()

        # Bind resize to keep image fitted
        self.image_frame.bind("<Configure>", self._on_image_frame_resize)

    # ---------------------------
    # UI Construction
    # ---------------------------
    def _build_ui(self):
        # Top frame for buttons
        self.controls_frame = tk.Frame(self, padx=10, pady=10)
        self.controls_frame.grid(row=0, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Bottom frame for image display
        self.image_frame = tk.Frame(self, bg="#f5f5f5", padx=10, pady=10)
        self.image_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        # Controls
        self._create_buttons(self.controls_frame)

        # Image holder
        self.image_label = tk.Label(self.image_frame, bg="#e9e9e9", anchor="center")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # Placeholder text when no image
        self._set_placeholder_text()

    def _create_buttons(self, parent: tk.Frame):
        # Button specs: (text, command)
        buttons = [
            ("Open Image", self._on_open_image),
            ("Grayscale", self._on_grayscale),
            ("Translate", lambda: self._show_unimplemented("Translate")),
            ("Threshold", self._on_threshold),
            ("Histogram Equalization", lambda: self._show_unimplemented("Histogram Equalization")),
            ("Sobel Sharpen", lambda: self._show_unimplemented("Sobel Sharpen")),
            ("Mean Filter", lambda: self._show_unimplemented("Mean Filter")),
            ("Canny Edge", lambda: self._show_unimplemented("Canny Edge")),
        ]

        # Create buttons in a single row
        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(parent, text=text, command=cmd, width=18)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            parent.grid_columnconfigure(i, weight=0)

        # Stretch right side
        parent.grid_columnconfigure(len(buttons), weight=1)

    # ---------------------------
    # Event Handlers
    # ---------------------------
    def _on_open_image(self):
        """Open local image and display, scaling to fit the image area while keeping aspect ratio."""
        filetypes = [
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tif *.webp"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("Bitmap", "*.bmp"),
            ("GIF", "*.gif"),
            ("TIFF", "*.tif *.tiff"),
            ("WEBP", "*.webp"),
            ("All Files", "*.*"),
        ]
        filepath = filedialog.askopenfilename(
            title="Select an image",
            filetypes=filetypes,
        )
        if not filepath:
            return

        try:
            image = Image.open(filepath)
            # Convert to RGB to avoid mode issues (e.g., palette or RGBA)
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            self.original_image = image
            self._current_image_path = filepath
            self._display_image_to_fit()
            self._set_window_subtitle(os.path.basename(filepath))
        except Exception as e:
            messagebox.showerror("Open Image Error", f"Failed to open image:\n{e}")

    def _on_image_frame_resize(self, _event):
        """Refresh display when the image area is resized."""
        if self.original_image is not None:
            self._display_image_to_fit()

    # ---------------------------
    # Processing Actions (implemented)
    # ---------------------------
    def _on_grayscale(self):
        """
        Convert current image to grayscale and display.
        Replaces current working image for subsequent operations.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        try:
            gray = self.original_image.convert("L")
            self.original_image = gray
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Grayscale Error", f"Failed to process image:\n{e}")

    def _on_threshold(self):
        """
        Apply simple global thresholding to the image.
        Prompts user for threshold value in [0, 255].
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return

        # Ask user for threshold; default 128
        t = simpledialog.askinteger(
            "Threshold", "Enter threshold (0-255):", minvalue=0, maxvalue=255, initialvalue=128
        )
        if t is None:
            return  # user cancelled

        try:
            # Ensure grayscale first
            gray = self.original_image.convert("L")
            # Map pixels to 0/255 based on threshold
            def _th(p, thr=t):
                return 255 if p >= thr else 0

            binary = gray.point(_th, mode="L")
            self.original_image = binary
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Threshold Error", f"Failed to apply threshold:\n{e}")

    # ---------------------------
    # Helpers
    # ---------------------------
    def _set_window_subtitle(self, filename: str):
        base_title = "AI Image Processing System"
        if filename:
            self.title(f"{base_title} - {filename}")
        else:
            self.title(base_title)

    def _set_placeholder_text(self):
        self.image_label.config(text="No image loaded.\nClick 'Open Image' to select an image.", fg="#666666", font=("Segoe UI", 12))

    def _clear_placeholder_text(self):
        self.image_label.config(text="")

    def _show_unimplemented(self, feature_name: str):
        messagebox.showinfo("Not Implemented", f"{feature_name} is not implemented yet.\nThis is a placeholder action.")

    def _display_image_to_fit(self):
        """Scale and display the current image to fit the image_frame."""
        if self.original_image is None:
            self._set_placeholder_text()
            return

        frame_w = max(1, self.image_frame.winfo_width() - 20)  # subtract padding
        frame_h = max(1, self.image_frame.winfo_height() - 20)

        # On first render, before layout is stabilized, fallback to some default
        if frame_w <= 1 or frame_h <= 1:
            frame_w, frame_h = 800, 500

        fitted = self._resize_to_fit(self.original_image, (frame_w, frame_h))
        self._update_image_label(fitted)

    @staticmethod
    def _resize_to_fit(img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """Resize PIL image to fit into target_size (w, h) with aspect ratio preserved."""
        tw, th = target_size
        iw, ih = img.size

        # Compute scale while preserving aspect ratio
        scale = min(tw / iw, th / ih) if iw and ih else 1.0
        new_w = max(1, int(iw * scale))
        new_h = max(1, int(ih * scale))

        # Use high-quality downsampling
        return img.resize((new_w, new_h), RESAMPLE_LANCZOS)

    def _update_image_label(self, pil_image: Image.Image):
        """Update the label widget with a PIL image."""
        self._clear_placeholder_text()
        self._photo_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=self._photo_image)

    # ---------------------------
    # Entry
    # ---------------------------
def main():
    app = ImageApp()
    app.mainloop()


if __name__ == "__main__":
    main()
