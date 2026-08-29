"""File Hasher - Calculate file hashes using MD5, SHA1, SHA256, or SHA512 algorithms."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import hashlib
import threading


def create_ui(frame, COLORS, FONTS):
    file_path = ctk.StringVar()
    algorithm = ctk.StringVar(value="sha256")
    result_var = ctk.StringVar()
    status_var = ctk.StringVar(value="Ready")

    def browse_file():
        path = filedialog.askopenfilename(title="Select File")
        if path:
            file_path.set(path)
            result_var.set("")
            status_var.set(f"Selected: {os.path.basename(path)}")

    def copy_result():
        frame.clipboard_clear()
        frame.clipboard_append(result_var.get())
        status_var.set("Hash copied to clipboard")

    def calculate_hash():
        path = file_path.get()
        if not path or not os.path.isfile(path):
            messagebox.showerror("Error", "Please select a valid file.")
            return

        result_var.set("")
        status_var.set("Calculating hash...")
        calc_btn.configure(state="disabled")

        def worker():
            try:
                h = hashlib.new(algorithm.get())
                with open(path, "rb") as f:
                    while chunk := f.read(8192):
                        h.update(chunk)
                result = h.hexdigest()
                frame.after(0, lambda: result_var.set(result))
                frame.after(0, lambda: status_var.set(f"{algorithm.get().upper()} hash calculated"))
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Error", str(e)))
                frame.after(0, lambda: status_var.set("Error"))
            finally:
                frame.after(0, lambda: calc_btn.configure(state="normal"))

        threading.Thread(target=worker, daemon=True).start()

    # Title
    ctk.CTkLabel(frame, text="File Hasher", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(frame, text="Calculate cryptographic hashes of files", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(0, 10))

    # File selection
    file_frame = ctk.CTkFrame(frame, fg_color="transparent")
    file_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkEntry(file_frame, textvariable=file_path, font=FONTS["mono_small"], placeholder_text="No file selected...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(file_frame, text="Browse", command=browse_file, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], width=100).pack(side="right")

    # Algorithm selection
    algo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    algo_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkLabel(algo_frame, text="Algorithm:", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left", padx=(0, 10))
    for algo in ["md5", "sha1", "sha256", "sha512"]:
        ctk.CTkRadioButton(algo_frame, text=algo.upper(), variable=algorithm, value=algo,
                           font=FONTS["body"], text_color=COLORS["text"],
                           fg_color=COLORS["accent"], hover_color=COLORS["green"]).pack(side="left", padx=5)

    # Calculate button
    calc_btn = ctk.CTkButton(frame, text="Calculate Hash", command=calculate_hash, font=FONTS["button"],
                             fg_color=COLORS["accent"], hover_color=COLORS["green"])
    calc_btn.pack(fill="x", padx=15, pady=(0, 10))

    # Result
    result_frame = ctk.CTkFrame(frame, fg_color="transparent")
    result_frame.pack(fill="x", padx=15, pady=(0, 5))

    ctk.CTkEntry(result_frame, textvariable=result_var, font=FONTS["mono"], placeholder_text="Hash will appear here...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["green"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(result_frame, text="Copy", command=copy_result, font=FONTS["button"],
                  fg_color=COLORS["bg_card"], border_color=COLORS["border"], border_width=1,
                  text_color=COLORS["text"], hover_color=COLORS["accent"], width=80).pack(side="right")

    # Status
    ctk.CTkLabel(frame, textvariable=status_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(5, 15))
