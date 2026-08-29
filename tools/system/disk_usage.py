"""
Disk Usage Analyzer Tool
Analyzes disk usage of folders, showing folder sizes and largest files.
"""

import customtkinter as ctk
import psutil
import platform
import os
import threading


def create_ui(frame, COLORS, FONTS):
    scanning = False
    scan_thread = None

    def format_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / 1024**2:.1f} MB"
        else:
            return f"{size_bytes / 1024**3:.2f} GB"

    def browse_folder():
        from tkinter import filedialog
        folder = filedialog.askdirectory(title="Select Folder to Analyze")
        if folder:
            folder_var.set(folder)
            start_scan(folder)

    def start_scan(path):
        nonlocal scanning, scan_thread
        if scanning:
            return
        scanning = True
        status_label.configure(text="Scanning...", text_color=COLORS["yellow"])
        progress_bar.set(0)
        scan_btn.configure(state="disabled")

        def scan():
            results = {"total_size": 0, "file_count": 0, "folder_count": 0, "folders": [], "largest": []}
            try:
                for root, dirs, files in os.walk(path):
                    for d in dirs:
                        try:
                            dp = os.path.join(root, d)
                            size = get_dir_size(dp)
                            rel = os.path.relpath(dp, path)
                            results["folders"].append((rel, size))
                            results["folder_count"] += 1
                        except (PermissionError, OSError):
                            continue

                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            size = os.path.getsize(fp)
                            results["total_size"] += size
                            results["file_count"] += 1
                            rel = os.path.relpath(fp, path)
                            results["largest"].append((rel, size))
                        except (PermissionError, OSError):
                            continue

                    frame.after(0, lambda: progress_bar.set(min(0.95, results["file_count"] / max(1, results["file_count"] + 50))))

            except Exception as e:
                frame.after(0, lambda: status_label.configure(text=f"Error: {e}", text_color=COLORS["red"]))
                return

            results["folders"].sort(key=lambda x: x[1], reverse=True)
            results["largest"].sort(key=lambda x: x[1], reverse=True)
            results["largest"] = results["largest"][:10]
            frame.after(0, lambda: display_results(results))

        def get_dir_size(start_path):
            total = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        total += os.path.getsize(fp)
                    except (PermissionError, OSError):
                        continue
            return total

        scan_thread = threading.Thread(target=scan, daemon=True)
        scan_thread.start()

    def display_results(results):
        nonlocal scanning
        scanning = False
        scan_btn.configure(state="normal")
        progress_bar.set(1.0)
        status_label.configure(text="Scan complete", text_color=COLORS["green"])

        for widget in results_frame.winfo_children():
            widget.destroy()

        stats_card = ctk.CTkFrame(results_frame, fg_color=COLORS["bg_card"], corner_radius=10)
        stats_card.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(stats_card, text="Summary", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(10, 5))

        for label, value in [("Total Size", format_size(results["total_size"])),
                              ("Files", str(results["file_count"])),
                              ("Folders", str(results["folder_count"]))]:
            row = ctk.CTkFrame(stats_card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, font=FONTS["body"], text_color=COLORS["text_dim"], width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=FONTS["mono"], text_color=COLORS["text"]).pack(side="left")

        largest_card = ctk.CTkFrame(results_frame, fg_color=COLORS["bg_card"], corner_radius=10)
        largest_card.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(largest_card, text="Top 10 Largest Files", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(10, 5))

        for i, (fpath, fsize) in enumerate(results["largest"]):
            bg = COLORS["bg_input"] if i % 2 == 0 else COLORS["bg_card"]
            row = ctk.CTkFrame(largest_card, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=10, pady=1)

            ctk.CTkLabel(row, text=format_size(fsize), font=FONTS["mono_small"], text_color=COLORS["accent"], width=90, anchor="w").pack(side="left", padx=5, pady=3)
            display_path = fpath if len(fpath) <= 60 else "..." + fpath[-57:]
            ctk.CTkLabel(row, text=display_path, font=FONTS["mono_small"], text_color=COLORS["text"], anchor="w").pack(side="left", fill="x", expand=True, padx=5, pady=3)

        top_folders_card = ctk.CTkFrame(results_frame, fg_color=COLORS["bg_card"], corner_radius=10)
        top_folders_card.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(top_folders_card, text="Top 10 Largest Folders", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(10, 5))

        for i, (fpath, fsize) in enumerate(results["folders"][:10]):
            bg = COLORS["bg_input"] if i % 2 == 0 else COLORS["bg_card"]
            row = ctk.CTkFrame(top_folders_card, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=10, pady=1)

            ctk.CTkLabel(row, text=format_size(fsize), font=FONTS["mono_small"], text_color=COLORS["yellow"], width=90, anchor="w").pack(side="left", padx=5, pady=3)
            display_path = fpath if len(fpath) <= 60 else "..." + fpath[-57:]
            ctk.CTkLabel(row, text=display_path, font=FONTS["mono_small"], text_color=COLORS["text"], anchor="w").pack(side="left", fill="x", expand=True, padx=5, pady=3)

    top_bar = ctk.CTkFrame(frame, fg_color="transparent")
    top_bar.pack(fill="x", padx=15, pady=(15, 5))
    ctk.CTkLabel(top_bar, text="Disk Usage Analyzer", font=FONTS["title"], text_color=COLORS["text"]).pack(side="left")

    input_bar = ctk.CTkFrame(frame, fg_color="transparent")
    input_bar.pack(fill="x", padx=15, pady=(5, 5))

    folder_var = ctk.StringVar()
    ctk.CTkEntry(input_bar, textvariable=folder_var, placeholder_text="Select a folder to analyze...",
                  font=FONTS["body"], fg_color=COLORS["bg_input"], border_color=COLORS["border"],
                  text_color=COLORS["text"], width=450).pack(side="left", padx=(0, 10))

    scan_btn = ctk.CTkButton(input_bar, text="Browse & Scan", font=FONTS["button"],
                              fg_color=COLORS["accent"], hover_color=COLORS["border"],
                              text_color=COLORS["text"], command=browse_folder, width=130)
    scan_btn.pack(side="right")

    status_label = ctk.CTkLabel(frame, text="Select a folder to begin", font=FONTS["body"], text_color=COLORS["text_dim"])
    status_label.pack(anchor="w", padx=20, pady=(5, 2))

    progress_bar = ctk.CTkProgressBar(frame, fg_color=COLORS["bg_input"], progress_color=COLORS["accent"])
    progress_bar.pack(fill="x", padx=20, pady=(0, 5))
    progress_bar.set(0)

    results_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", scrollbar_button_color=COLORS["border"])
    results_frame.pack(fill="both", expand=True, padx=5, pady=(0, 15))
