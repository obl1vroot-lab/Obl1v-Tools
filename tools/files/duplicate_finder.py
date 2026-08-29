"""Duplicate Finder - Scan folders for duplicate files based on content hashing."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import hashlib
import threading
from collections import defaultdict


def create_ui(frame, COLORS, FONTS):
    folder_path = ctk.StringVar()
    status_var = ctk.StringVar(value="Ready")
    progress_var = ctk.DoubleVar(value=0)
    scan_running = False

    def browse_folder():
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            folder_path.set(path)
            status_var.set(f"Selected: {path}")

    def scan_duplicates():
        path = folder_path.get()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        nonlocal scan_running
        if scan_running:
            return
        scan_running = True
        scan_btn.configure(state="disabled")
        output_box.delete("1.0", "end")
        output_box.insert("end", "Scanning...\n")
        progress_var.set(0)

        def worker():
            try:
                file_hashes = defaultdict(list)
                all_files = []
                for root, dirs, files in os.walk(path):
                    for fname in files:
                        fpath = os.path.join(root, fname)
                        if os.path.isfile(fpath):
                            all_files.append(fpath)

                total = len(all_files)
                if total == 0:
                    frame.after(0, lambda: output_box.replace("1.0", "end", "No files found.\n"))
                    frame.after(0, lambda: status_var.set("No files found"))
                    frame.after(0, lambda: scan_btn.configure(state="normal"))
                    scan_running = False
                    return

                for i, fpath in enumerate(all_files):
                    try:
                        h = hashlib.md5()
                        with open(fpath, "rb") as f:
                            while chunk := f.read(8192):
                                h.update(chunk)
                        file_hashes[h.hexdigest()].append(fpath)
                    except (PermissionError, OSError):
                        pass
                    if i % 50 == 0:
                        frame.after(0, lambda v=(i / total) * 100: progress_var.set(v))

                progress_var.set(100)
                duplicates = {k: v for k, v in file_hashes.items() if len(v) > 1}

                if not duplicates:
                    frame.after(0, lambda: output_box.replace("1.0", "end", "No duplicate files found.\n"))
                    frame.after(0, lambda: status_var.set("Scan complete - no duplicates"))
                else:
                    lines = []
                    for h, files in sorted(duplicates.items(), key=lambda x: -len(x[1])):
                        lines.append(f"--- Hash: {h[:16]}... ({len(files)} files) ---")
                        for fpath in files:
                            size = os.path.getsize(fpath)
                            lines.append(f"  {size:>12,} bytes  {fpath}")
                        lines.append("")
                    frame.after(0, lambda: output_box.replace("1.0", "end", "\n".join(lines)))
                    frame.after(0, lambda: status_var.set(f"Found {len(duplicates)} duplicate groups"))
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Error", str(e)))
                frame.after(0, lambda: status_var.set("Error"))
            finally:
                frame.after(0, lambda: scan_btn.configure(state="normal"))
                scan_running = False

        threading.Thread(target=worker, daemon=True).start()

    # Title
    ctk.CTkLabel(frame, text="Duplicate Finder", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(frame, text="Find duplicate files by content hash", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(0, 10))

    # Folder selection
    folder_frame = ctk.CTkFrame(frame, fg_color="transparent")
    folder_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkEntry(folder_frame, textvariable=folder_path, font=FONTS["mono_small"], placeholder_text="No folder selected...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(folder_frame, text="Browse", command=browse_folder, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], width=100).pack(side="right")

    # Scan button
    scan_btn = ctk.CTkButton(frame, text="Scan for Duplicates", command=scan_duplicates, font=FONTS["button"],
                             fg_color=COLORS["accent"], hover_color=COLORS["green"])
    scan_btn.pack(fill="x", padx=15, pady=(0, 10))

    # Progress bar
    ctk.CTkProgressBar(frame, variable=progress_var, fg_color=COLORS["bg_input"],
                       progress_color=COLORS["green"]).pack(fill="x", padx=15, pady=(0, 10))

    # Output area
    output_box = ctk.CTkTextbox(frame, font=FONTS["mono_small"], fg_color=COLORS["bg_input"],
                                border_color=COLORS["border"], border_width=1, text_color=COLORS["text"],
                                wrap="word", height=300)
    output_box.pack(fill="both", expand=True, padx=15, pady=(0, 5))

    # Status
    ctk.CTkLabel(frame, textvariable=status_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(5, 15))
