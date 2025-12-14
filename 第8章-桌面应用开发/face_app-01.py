import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
import os


class FaceApp(tk.Tk):
    """
    AI Face Recognition System - Main Window
    Layout (Frame + Grid):
      - Top: Control buttons (Open Image, Start Camera, Stop Camera, Detect Face)
      - Bottom-Left: Image display area (static image or camera frames)
      - Right: Log output area (status/info)
    Features:
      - Window resizes responsively, image keeps aspect ratio.
      - Open Image loads via Pillow and fits display region.
      - Start Camera uses OpenCV with Tkinter after() for non-blocking UI.
      - Stop Camera safely releases resources.
      - Detect Face: placeholder (message box + log).
    """

    def __init__(self):
        super().__init__()
        self.title("AI Face Recognition System")
        self.minsize(900, 600)

        # State
        self.cap = None
        self.camera_running = False
        self.current_image = None  # PIL.Image for last opened image
        self.current_frame = None  # last camera frame (PIL.Image)
        self._imgtk_ref = None     # keep a reference to avoid GC

        # Face detector (OpenCV Haar Cascade)
        self.face_cascade = cv2.CascadeClassifier(
            os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        )
        if self.face_cascade.empty():
            self._log("Warning: Failed to load Haar cascade for face detection.")

        # Build UI
        self._build_layout()
        self._configure_grid_weights()

        # Handle resize to keep image aspect ratio
        self.bind("<Configure>", self._on_window_resize)

    # -----------------------------
    # UI Construction
    # -----------------------------
    def _build_layout(self):
        # Root grid: 2 columns (left: content, right: logs), multiple rows
        # Row 0: button bar (left), Row 1: image area (left)
        # Right column spans rows 0..1 for logs

        # Left container frame
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Right (logs) frame
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Top: Control buttons
        self.controls_frame = tk.Frame(self.left_frame)
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        # Buttons (horizontally)
        self.btn_open = tk.Button(self.controls_frame, text="Open Image", command=self.on_open_image, width=15)
        self.btn_start_cam = tk.Button(self.controls_frame, text="Start Camera", command=self.on_start_camera, width=15)
        self.btn_stop_cam = tk.Button(self.controls_frame, text="Stop Camera", command=self.on_stop_camera, width=15)
        self.btn_detect = tk.Button(self.controls_frame, text="Detect Face", command=self.on_detect_face, width=15)

        self.btn_open.grid(row=0, column=0, padx=(0, 6))
        self.btn_start_cam.grid(row=0, column=1, padx=6)
        self.btn_stop_cam.grid(row=0, column=2, padx=6)
        self.btn_detect.grid(row=0, column=3, padx=(6, 0))

        # Bottom: Image display area
        self.display_frame = tk.Frame(self.left_frame, bg="#222222", relief="sunken", borderwidth=1)
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Use a Label to render images
        self.image_label = tk.Label(self.display_frame, bg="#000000")
        # Pack the label centered; expand to allow proper centering
        self.image_label.pack(expand=True)

        # Logs area (right)
        self.log_label = tk.Label(self.right_frame, text="Logs", anchor="w")
        self.log_label.pack(side="top", anchor="w", padx=8, pady=(8, 0))

        self.log_text = scrolledtext.ScrolledText(self.right_frame, wrap="word", height=10, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Initial log
        self._log("Application started.")

    def _configure_grid_weights(self):
        # Root grid
        self.grid_columnconfigure(0, weight=3)  # left content
        self.grid_columnconfigure(1, weight=2)  # right logs
        self.grid_rowconfigure(0, weight=0)     # top row (buttons) - will be inside left_frame
        self.grid_rowconfigure(1, weight=1)     # image row grows

        # Left frame grid
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=0)  # controls
        self.left_frame.grid_rowconfigure(1, weight=1)  # display grows

        # Right frame uses pack with expand

    # -----------------------------
    # Event Handlers
    # -----------------------------
    def on_open_image(self):
        if self.camera_running:
            self._log("Camera is running. Stopping camera before opening image...")
            self._stop_camera_internal()

        filetypes = [
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"),
            ("All Files", "*.*"),
        ]
        initial_dir = os.getcwd()
        path = filedialog.askopenfilename(title="Open Image", filetypes=filetypes, initialdir=initial_dir)
        if not path:
            self._log("Open Image canceled.")
            return

        try:
            img = Image.open(path)
            # Convert to RGB or L
            if img.mode not in ("RGB", "L"):
                # If has alpha, convert to RGB; otherwise default to RGB
                img = img.convert("RGB")

            self.current_image = img
            self._log(f"Loaded image: {os.path.basename(path)} ({img.mode}, {img.size[0]}x{img.size[1]})")

            # Display to fit area
            self._render_image_to_display(img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")
            self._log(f"Error opening image: {e}")

    def on_start_camera(self):
        if self.camera_running:
            self._log("Camera already running.")
            return

        # Attempt to open default camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if hasattr(cv2, "CAP_DSHOW") else cv2.VideoCapture(0)
        if not self.cap or not self.cap.isOpened():
            self._log("Failed to open camera 0.")
            messagebox.showerror("Camera Error", "Unable to open camera (index 0).")
            self.cap = None
            return

        self.camera_running = True
        self._log("Camera started.")
        self._update_camera_frame()

    def on_stop_camera(self):
        if not self.camera_running:
            self._log("Camera is not running.")
            return
        self._stop_camera_internal()
        self._log("Camera stopped.")

    def on_detect_face(self):
        """
        Run face detection on the currently displayed image.
        - If camera is running, uses the latest frame.
        - Otherwise, uses the last opened static image.
        Draws bounding boxes on a copy, renders it, and logs results.
        """
        # Select source image (PIL)
        src_img = None
        if self.camera_running and self.current_frame is not None:
            src_img = self.current_frame.copy()
        elif self.current_image is not None:
            src_img = self.current_image.copy()

        if src_img is None:
            messagebox.showwarning("Detect Face", "No image available. Open an image or start the camera first.")
            self._log("Detect Face: no image/frame available.")
            return

        # Ensure cascade is ready
        if not hasattr(self, "face_cascade") or self.face_cascade is None or self.face_cascade.empty():
            messagebox.showerror("Detect Face", "Face detector is not available.")
            self._log("Detect Face error: cascade not loaded.")
            return

        try:
            # Convert PIL (RGB or L) to numpy array
            if src_img.mode not in ("RGB", "L"):
                src_img = src_img.convert("RGB")

            rgb = np.array(src_img)  # RGB order
            # Get grayscale for detection
            if src_img.mode == "L":
                gray = rgb  # already single channel
            else:
                gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

            # Improve detection robustness slightly
            gray_eq = cv2.equalizeHist(gray)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray_eq,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )

            # Draw rectangles on a display copy (keep RGB)
            draw_rgb = rgb.copy() if src_img.mode != "L" else cv2.cvtColor(rgb, cv2.COLOR_GRAY2RGB)
            for (x, y, w, h) in faces:
                cv2.rectangle(draw_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)  # red boxes

            # Convert back to PIL and render
            out_pil = Image.fromarray(draw_rgb)
            self._render_image_to_display(out_pil)

            # Keep as current image preview if camera is not running
            if not self.camera_running:
                self.current_image = out_pil

            count = 0 if faces is None else len(faces)
            self._log(f"Face detection complete. Faces found: {count}")
            if count == 0:
                messagebox.showinfo("Detect Face", "No faces detected.")
        except Exception as e:
            messagebox.showerror("Detect Face", f"Face detection failed:\n{e}")
            self._log(f"Detect Face error: {e}")

    # -----------------------------
    # Camera Handling
    # -----------------------------
    def _stop_camera_internal(self):
        self.camera_running = False
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    def _update_camera_frame(self):
        if not self.camera_running or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self._log("Failed to read frame from camera.")
            # Try again shortly; if persistent, user can stop.
            self.after(100, self._update_camera_frame)
            return

        # Convert BGR (OpenCV) to RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        self.current_frame = pil_img

        # Render to display area with aspect fit
        self._render_image_to_display(pil_img)

        # Schedule next frame
        self.after(30, self._update_camera_frame)  # ~33 fps

    # -----------------------------
    # Rendering
    # -----------------------------
    def _render_image_to_display(self, img: Image.Image):
        """
        Render PIL.Image to display_frame, maintaining aspect ratio and fitting within frame.
        """
        disp_w, disp_h = self._get_display_size()
        if disp_w <= 1 or disp_h <= 1:
            # Display frame not ready yet; schedule a retry
            self.after(50, lambda: self._render_image_to_display(img))
            return

        # Compute aspect-fit size
        img_w, img_h = img.size
        scale = min(disp_w / img_w, disp_h / img_h)
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))

        resized = img.resize((new_w, new_h), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(resized)

        self._imgtk_ref = imgtk  # keep reference
        self.image_label.configure(image=imgtk)
        self.image_label.image = imgtk  # bind to label to prevent GC
        # With pack(), label is centered automatically

    def _get_display_size(self):
        # Available size inside display_frame (avoid update_idletasks to prevent Configure loops)
        w = self.display_frame.winfo_width()
        h = self.display_frame.winfo_height()
        # Fallback when not yet laid out
        if w <= 1 or h <= 1:
            # Use a fraction of the window as an initial guess
            w = max(300, int(self.winfo_width() * 0.6))
            h = max(200, int(self.winfo_height() * 0.6))
        return w, h

    def _on_window_resize(self, event):
        """
        When window resizes, re-render current image/frame to keep aspect ratio.
        """
        # Prefer showing live frame if camera running, otherwise current_image
        if self.camera_running and self.current_frame is not None:
            self._render_image_to_display(self.current_frame)
        elif self.current_image is not None:
            self._render_image_to_display(self.current_image)

    # -----------------------------
    # Logging
    # -----------------------------
    def _log(self, msg: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")


if __name__ == "__main__":
    app = FaceApp()
    app.mainloop()
