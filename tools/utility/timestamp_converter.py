"""
Timestamp Converter - Convert between Unix timestamps and human-readable dates.

Supports seconds/milliseconds auto-detection, bidirectional conversion,
and displays current timestamp with auto-refresh.
"""

import customtkinter as ctk
from tkinter import messagebox
import uuid
import json
import time
from datetime import datetime


def create_ui(frame, COLORS, FONTS):
    """Build the Timestamp Converter GUI inside the given frame."""

    current_epoch = [None]
    running = [True]

    def destroy_ui():
        running[0] = False

    frame.destroy_ui = destroy_ui

    # --- Header ---
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    ctk.CTkLabel(header, text="Timestamp Converter", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w")
    ctk.CTkLabel(header, text="Convert between Unix timestamps and human-readable dates", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")

    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    # === Column 1: Unix -> Human ===
    col1 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    col1.pack(side="left", fill="both", expand=True, padx=(0, 8))

    ctk.CTkLabel(col1, text="Unix Timestamp to Human Date", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    ctk.CTkLabel(col1, text="Enter Unix timestamp (seconds or milliseconds):", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15)
    ts_entry = ctk.CTkEntry(col1, placeholder_text="e.g. 1700000000", font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    ts_entry.pack(fill="x", padx=15, pady=(2, 10))

    outputs_unix = {}

    def convert_unix_to_human():
        raw = ts_entry.get().strip()
        if not raw:
            messagebox.showwarning("Input Required", "Please enter a Unix timestamp.")
            return
        try:
            val = float(raw)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric timestamp.")
            return

        if val > 1e12:
            epoch = val / 1000.0
        else:
            epoch = val

        dt_utc = datetime.utcfromtimestamp(epoch)
        dt_local = datetime.fromtimestamp(epoch)

        results = {
            "ISO Format": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "Human Readable (UTC)": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "Human Readable (Local)": dt_local.strftime("%Y-%m-%d %H:%M:%S"),
            "Date Only": dt_utc.strftime("%Y-%m-%d"),
            "Time Only": dt_utc.strftime("%H:%M:%S"),
        }

        for key, val_text in results.items():
            if key in outputs_unix:
                outputs_unix[key].configure(state="normal")
                outputs_unix[key].delete("1.0", "end")
                outputs_unix[key].insert("1.0", val_text)
                outputs_unix[key].configure(state="disabled")

    ctk.CTkButton(col1, text="Convert", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=convert_unix_to_human).pack(fill="x", padx=15, pady=(0, 10))

    for label_text in ["ISO Format", "Human Readable (UTC)", "Human Readable (Local)", "Date Only", "Time Only"]:
        row = ctk.CTkFrame(col1, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(row, text=label_text + ":", font=FONTS["body"], text_color=COLORS["text_dim"], width=140, anchor="w").pack(side="left")
        txt = ctk.CTkTextbox(row, height=28, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"], activate_scrollbars=False)
        txt.pack(side="left", fill="x", expand=True, padx=(4, 4))
        txt.configure(state="disabled")
        outputs_unix[label_text] = txt

        def copy_cb(t=txt):
            t.configure(state="normal")
            val = t.get("1.0", "end").strip()
            t.configure(state="disabled")
            if val:
                frame.clipboard_clear()
                frame.clipboard_append(val)

        ctk.CTkButton(row, text="Copy", width=50, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_cb).pack(side="left")

    # === Column 2: Human -> Unix ===
    col2 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    col2.pack(side="left", fill="both", expand=True, padx=8)

    ctk.CTkLabel(col2, text="Human Date to Unix Timestamp", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    ctk.CTkLabel(col2, text="Enter date (YYYY-MM-DD HH:MM:SS):", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15)
    date_entry = ctk.CTkEntry(col2, placeholder_text="e.g. 2025-01-01 12:00:00", font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    date_entry.pack(fill="x", padx=15, pady=(2, 10))

    output_human = {}

    def convert_human_to_unix():
        raw = date_entry.get().strip()
        if not raw:
            messagebox.showwarning("Input Required", "Please enter a date string.")
            return
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(raw, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Format", "Use YYYY-MM-DD HH:MM:SS or YYYY-MM-DD")
                return

        epoch_seconds = dt.timestamp()

        results = {
            "Seconds": str(int(epoch_seconds)),
            "Milliseconds": str(int(epoch_seconds * 1000)),
            "Microseconds": str(int(epoch_seconds * 1_000_000)),
            "ISO Format": dt.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        for key, val_text in results.items():
            if key in output_human:
                output_human[key].configure(state="normal")
                output_human[key].delete("1.0", "end")
                output_human[key].insert("1.0", val_text)
                output_human[key].configure(state="disabled")

    ctk.CTkButton(col2, text="Convert", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=convert_human_to_unix).pack(fill="x", padx=15, pady=(0, 10))

    for label_text in ["Seconds", "Milliseconds", "Microseconds", "ISO Format"]:
        row = ctk.CTkFrame(col2, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(row, text=label_text + ":", font=FONTS["body"], text_color=COLORS["text_dim"], width=110, anchor="w").pack(side="left")
        txt = ctk.CTkTextbox(row, height=28, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"], activate_scrollbars=False)
        txt.pack(side="left", fill="x", expand=True, padx=(4, 4))
        txt.configure(state="disabled")
        output_human[label_text] = txt

        def copy_cb(t=txt):
            t.configure(state="normal")
            val = t.get("1.0", "end").strip()
            t.configure(state="disabled")
            if val:
                frame.clipboard_clear()
                frame.clipboard_append(val)

        ctk.CTkButton(row, text="Copy", width=50, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_cb).pack(side="left")

    # === Column 3: Current Timestamp ===
    col3 = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    col3.pack(side="left", fill="both", expand=True, padx=(8, 0))

    ctk.CTkLabel(col3, text="Current Timestamp", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    current_outputs = {}

    for label_text in ["Unix (seconds)", "Unix (milliseconds)", "ISO Format", "UTC Time", "Local Time"]:
        row = ctk.CTkFrame(col3, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(row, text=label_text + ":", font=FONTS["body"], text_color=COLORS["text_dim"], width=130, anchor="w").pack(side="left")
        txt = ctk.CTkTextbox(row, height=28, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"], activate_scrollbars=False)
        txt.pack(side="left", fill="x", expand=True, padx=(4, 4))
        txt.configure(state="disabled")
        current_outputs[label_text] = txt

        def copy_cb(t=txt):
            t.configure(state="normal")
            val = t.get("1.0", "end").strip()
            t.configure(state="disabled")
            if val:
                frame.clipboard_clear()
                frame.clipboard_append(val)

        ctk.CTkButton(row, text="Copy", width=50, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_cb).pack(side="left")

    def refresh_current():
        if not running[0]:
            return
        now = time.time()
        dt_utc = datetime.utcfromtimestamp(now)
        dt_local = datetime.fromtimestamp(now)

        vals = {
            "Unix (seconds)": str(int(now)),
            "Unix (milliseconds)": str(int(now * 1000)),
            "ISO Format": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "UTC Time": dt_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "Local Time": dt_local.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for key, val_text in vals.items():
            if key in current_outputs:
                current_outputs[key].configure(state="normal")
                current_outputs[key].delete("1.0", "end")
                current_outputs[key].insert("1.0", val_text)
                current_outputs[key].configure(state="disabled")

        frame.after(1000, refresh_current)

    refresh_current()
