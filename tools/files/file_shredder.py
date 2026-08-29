"""File Shredder - Securely delete files by overwriting with random data before removal."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import hashlib
import threading
import secrets


def create_ui(frame, COLORS, FONTS):
    file_path = ctk.StringVar()
    passes_var = ctk.StringVar(value="3")
    status_var = ctk.StringVar(value="Ready")
    progress_var = ctk.DoubleVar(value=0)

    def browse_file():
        path = filedialog.askopenfilename(title="Select File to Shred")
        if path:
            file_path.set(path)
            progress_var.set(0)
            status_var.set(f"Selected: {os.path.basename(path)}")

    def shred_file():
        path = file_path.get()
        if not path or not os.path.isfile(path):
            messagebox.showerror("Error", "Please select a valid file.")
            return

        try:
            num_passes = int(passes_var.get())
            if num_passes not in (1, 3, 7):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Passes must be 1, 3, or 7.")
            return

        size = os.path.getsize(path)
        msg = (
            f"WARNING: This will permanently destroy the file:\n\n"
            f"{os.path.basename(path)}\n"
            f"Size: {size:,} bytes\n"
            f"Passes: {num_passes}\n\n"
            f"This operation CANNOT be undone."
        )
        if not messagebox.askyesno("Confirm Shred", msg):
            return

        status_var.set("Shredding...")
        shred_btn.configure(state="disabled")
        progress_var.set(0)

        def worker():
            try:
                file_size = os.path.getsize(path)
                with open(path, "r+b") as f:
                    for p in range(num_passes):
                        f.seek(0)
                        written = 0
                        while written < file_size:
                            chunk_size = min(8192, file_size - written)
                            f.write(secrets.token_bytes(chunk_size))
                            written += chunk_size
                            current_progress = ((p + written / file_size) / num_passes) * 100
                            frame.after(0, lambda v=current_progress: progress_var.set(v))
                        f.flush()
                        os.fsync(f.fileno())

                os.remove(path)

                def done():
                    progress_var.set(100)
                    status_var.set("File shredded and deleted")
                    messagebox.showinfo("Shred Complete", f"File has been securely deleted.\n{num_passes} pass(es) completed.")
                    file_path.set("")

                frame.after(0, done)
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Error", str(e)))
                frame.after(0, lambda: status_var.set("Error"))
            finally:
                frame.after(0, lambda: shred_btn.configure(state="normal"))

        threading.Thread(target=worker, daemon=True).start()

    # Title
    ctk.CTkLabel(frame, text="Secure File Shredder", font=FONTS["title"], text_color=COLORS["red"]).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(frame, text="Permanently destroy files by overwriting with random data", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(0, 10))

    # File selection
    file_frame = ctk.CTkFrame(frame, fg_color="transparent")
    file_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkEntry(file_frame, textvariable=file_path, font=FONTS["mono_small"], placeholder_text="No file selected...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(file_frame, text="Browse", command=browse_file, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], width=100).pack(side="right")

    # Pass selector
    pass_frame = ctk.CTkFrame(frame, fg_color="transparent")
    pass_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkLabel(pass_frame, text="Overwrite passes:", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left", padx=(0, 10))
    for p in ("1", "3", "7"):
        ctk.CTkRadioButton(pass_frame, text=f"{p} pass{'es' if p != '1' else ''}", variable=passes_var, value=p,
                           font=FONTS["body"], text_color=COLORS["text"],
                           fg_color=COLORS["red"], hover_color="#cc0000").pack(side="left", padx=8)

    # Warning
    warning_frame = ctk.CTkFrame(frame, fg_color="#330000", border_color=COLORS["red"], border_width=1)
    warning_frame.pack(fill="x", padx=15, pady=(0, 10))
    ctk.CTkLabel(warning_frame, text="WARNING: Shredded files are permanently deleted and CANNOT be recovered.",
                 font=FONTS["body"], text_color=COLORS["red"]).pack(padx=10, pady=8)

    # Shred button
    shred_btn = ctk.CTkButton(frame, text="SHRED FILE", command=shred_file, font=FONTS["button"],
                              fg_color=COLORS["red"], hover_color="#cc0000", height=40)
    shred_btn.pack(fill="x", padx=15, pady=(0, 10))

    # Progress
    ctk.CTkProgressBar(frame, variable=progress_var, fg_color=COLORS["bg_input"],
                       progress_color=COLORS["red"]).pack(fill="x", padx=15, pady=(0, 10))

    # Status
    ctk.CTkLabel(frame, textvariable=status_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(5, 15))
