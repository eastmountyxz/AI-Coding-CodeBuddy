import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageOps, ImageFilter
from typing import Tuple, Optional

# Optional OpenCV/NumPy for advanced processing
try:
    import cv2
    import numpy as np
    _HAS_CV2 = True
except Exception:
    cv2 = None  # type: ignore
    np = None  # type: ignore
    _HAS_CV2 = False

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
            ("Translate", self._on_translate),
            ("Threshold", self._on_threshold),
            ("Histogram Equalization", self._on_hist_equalize),
            ("Sobel Sharpen", self._on_sobel_sharpen),
            ("Mean Filter", self._on_mean_filter),
            ("Canny Edge", self._on_canny_edge),
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

    def _ensure_cv2(self) -> bool:
        """
        Ensure OpenCV is available; otherwise display a hint.
        """
        if not _HAS_CV2:
            messagebox.showerror(
                "Dependency Missing",
                "OpenCV (cv2) is required for this operation.\n"
                "Install with: pip install opencv-python numpy"
            )
            return False
        return True

    @staticmethod
    def _pil_to_cv_gray(img: Image.Image):
        """
        Convert PIL Image to OpenCV grayscale uint8 ndarray.
        """
        if img.mode != "L":
            gray = img.convert("L")
        else:
            gray = img
        return np.array(gray, dtype=np.uint8)

    @staticmethod
    def _cv_to_pil_gray(arr) -> Image.Image:
        """
        Convert OpenCV grayscale ndarray to PIL Image (mode 'L').
        """
        return Image.fromarray(arr, mode="L")

    def _on_sobel_sharpen(self):
        """
        Apply Sobel-based sharpening:
        - Compute Sobel gradients on grayscale
        - Combine gradients into an edge map
        - Blend the edge map with the original grayscale to enhance details
        Result is displayed and stored as the current image.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        if not self._ensure_cv2():
            return
        try:
            gray = self._pil_to_cv_gray(self.original_image)
            # Sobel gradients
            gx = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
            gy = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3)
            abs_gx = cv2.convertScaleAbs(gx)
            abs_gy = cv2.convertScaleAbs(gy)
            edge = cv2.addWeighted(abs_gx, 0.5, abs_gy, 0.5, 0)

            # Sharpen by blending original with edge map
            sharpen = cv2.addWeighted(gray, 1.0, edge, 0.7, 0)

            result = self._cv_to_pil_gray(sharpen)
            self.original_image = result
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Sobel Sharpen Error", f"Failed to apply Sobel sharpening:\n{e}")

    def _on_canny_edge(self):
        """
        Apply Canny edge detection:
        - Ask user for lower/upper thresholds
        - Run cv2.Canny on grayscale
        Result is a binary edge map.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        if not self._ensure_cv2():
            return

        # Ask thresholds
        low = simpledialog.askinteger(
            "Canny Edge", "Enter lower threshold (0-255):", minvalue=0, maxvalue=255, initialvalue=100
        )
        if low is None:
            return
        high = simpledialog.askinteger(
            "Canny Edge", "Enter upper threshold (0-255):", minvalue=0, maxvalue=255, initialvalue=200
        )
        if high is None:
            return
        if high < low:
            messagebox.showwarning("Invalid Input", "Upper threshold must be >= lower threshold.")
            return

        try:
            gray = self._pil_to_cv_gray(self.original_image)
            edges = cv2.Canny(gray, threshold1=low, threshold2=high)
            result = self._cv_to_pil_gray(edges)
            self.original_image = result
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Canny Error", f"Failed to apply Canny edge detection:\n{e}")

    # ---------------------------
    # Additional Processing Actions
    # ---------------------------
    def _on_translate(self):
        """
        Translate the image by (dx, dy) pixels.
        Uses PIL paste onto a new canvas with the same size.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return

        dx = simpledialog.askinteger("Translate", "Enter dx (pixels, negative allowed):", initialvalue=50, minvalue=-10000, maxvalue=10000)
        if dx is None:
            return
        dy = simpledialog.askinteger("Translate", "Enter dy (pixels, negative allowed):", initialvalue=50, minvalue=-10000, maxvalue=10000)
        if dy is None:
            return

        try:
            src = self.original_image
            # Background color: black for both L and RGB
            bg = 0 if src.mode == "L" else (0, 0, 0)
            canvas = Image.new(src.mode, src.size, bg)
            # Paste handles clipping automatically for negative offsets
            canvas.paste(src, (dx, dy))
            self.original_image = canvas
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Translate Error", f"Failed to translate image:\n{e}")

    def _on_hist_equalize(self):
        """
        Histogram equalization.
        - Grayscale: direct equalize.
        - RGB: convert to YCbCr, equalize Y channel, then convert back to RGB.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return

        try:
            img = self.original_image
            if img.mode == "L":
                eq = ImageOps.equalize(img)
            else:
                # Process luminance only for color image
                ycbcr = img.convert("YCbCr")
                y, cb, cr = ycbcr.split()
                y_eq = ImageOps.equalize(y)
                eq = Image.merge("YCbCr", (y_eq, cb, cr)).convert("RGB")
            self.original_image = eq
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Histogram Equalization Error", f"Failed to equalize histogram:\n{e}")

    def _on_mean_filter(self):
        """
        Mean filter with a user-defined kernel size (odd).
        Implemented via PIL BoxBlur where radius r = (k-1)//2.
        """
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return

        k = simpledialog.askinteger("Mean Filter", "Kernel size (odd, >=1):", minvalue=1, maxvalue=99, initialvalue=3)
        if k is None:
            return
        # Ensure odd kernel size
        if k % 2 == 0:
            k += 1

        try:
            radius = (k - 1) // 2
            filtered = self.original_image.filter(ImageFilter.BoxBlur(radius))
            self.original_image = filtered
            self._display_image_to_fit()
        except Exception as e:
            messagebox.showerror("Mean Filter Error", f"Failed to apply mean filter:\n{e}")

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
