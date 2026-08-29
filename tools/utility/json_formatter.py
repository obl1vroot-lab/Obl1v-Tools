"""
JSON Formatter / Validator - Format, minify, and validate JSON data.

Provides a clean interface for pasting JSON, formatting it with
configurable indentation, minifying, and validating with error details.
"""

import customtkinter as ctk
from tkinter import messagebox
import uuid
import json
import time
from datetime import datetime


def create_ui(frame, COLORS, FONTS):
    """Build the JSON Formatter GUI inside the given frame."""

    # --- Header ---
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    ctk.CTkLabel(header, text="JSON Formatter / Validator", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w")
    ctk.CTkLabel(header, text="Format, minify, and validate JSON data", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")

    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    # === Top: Input ===
    input_card = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    input_card.pack(fill="both", expand=True, pady=(0, 8))

    in_header = ctk.CTkFrame(input_card, fg_color="transparent")
    in_header.pack(fill="x", padx=15, pady=(15, 5))
    ctk.CTkLabel(in_header, text="Input JSON", font=FONTS["heading"], text_color=COLORS["text"]).pack(side="left")

    def clear_input():
        input_box.configure(state="normal")
        input_box.delete("1.0", "end")

    ctk.CTkButton(in_header, text="Clear", width=60, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["red"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=clear_input).pack(side="right")

    input_box = ctk.CTkTextbox(input_card, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"])
    input_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # === Middle: Action bar ===
    action_bar = ctk.CTkFrame(content, fg_color="transparent")
    action_bar.pack(fill="x", pady=(0, 8))

    # Indent selector
    indent_frame = ctk.CTkFrame(action_bar, fg_color="transparent")
    indent_frame.pack(side="left")
    ctk.CTkLabel(indent_frame, text="Indent:", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(side="left", padx=(0, 4))
    indent_var = ctk.StringVar(value="4")
    indent_menu = ctk.CTkOptionMenu(indent_frame, variable=indent_var, values=["2", "4", "8"], width=60, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], button_color=COLORS["accent"], button_hover_color=COLORS["green"], dropdown_fg_color=COLORS["bg_card"], text_color=COLORS["text"])
    indent_menu.pack(side="left")

    def get_input():
        return input_box.get("1.0", "end").strip()

    def format_json():
        raw = get_input()
        if not raw:
            messagebox.showwarning("Input Required", "Please paste some JSON to format.")
            return
        try:
            parsed = json.loads(raw)
            indent = int(indent_var.get())
            formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("1.0", formatted)
            output_box.configure(state="disabled")
            status_label.configure(text="Formatted successfully", text_color=COLORS["green"])
        except json.JSONDecodeError as e:
            status_label.configure(text=f"Error at line {e.lineno}, col {e.colno}: {e.msg}", text_color=COLORS["red"])
            messagebox.showerror("Invalid JSON", f"Line {e.lineno}, Column {e.colno}\n{e.msg}")

    def minify_json():
        raw = get_input()
        if not raw:
            messagebox.showwarning("Input Required", "Please paste some JSON to minify.")
            return
        try:
            parsed = json.loads(raw)
            minified = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("1.0", minified)
            output_box.configure(state="disabled")
            status_label.configure(text="Minified successfully", text_color=COLORS["green"])
        except json.JSONDecodeError as e:
            status_label.configure(text=f"Error at line {e.lineno}, col {e.colno}: {e.msg}", text_color=COLORS["red"])
            messagebox.showerror("Invalid JSON", f"Line {e.lineno}, Column {e.colno}\n{e.msg}")

    def validate_json():
        raw = get_input()
        if not raw:
            messagebox.showwarning("Input Required", "Please paste some JSON to validate.")
            return
        try:
            json.loads(raw)
            status_label.configure(text="Valid JSON", text_color=COLORS["green"])
        except json.JSONDecodeError as e:
            status_label.configure(text=f"Invalid at line {e.lineno}, col {e.colno}: {e.msg}", text_color=COLORS["red"])

    btn_style = dict(font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"])
    ctk.CTkButton(action_bar, text="Format", command=format_json, **btn_style).pack(side="left", padx=(0, 6))
    ctk.CTkButton(action_bar, text="Minify", command=minify_json, **btn_style).pack(side="left", padx=(0, 6))
    ctk.CTkButton(action_bar, text="Validate", command=validate_json, **btn_style).pack(side="left", padx=(0, 6))

    # === Bottom: Output ===
    output_card = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    output_card.pack(fill="both", expand=True)

    out_header = ctk.CTkFrame(output_card, fg_color="transparent")
    out_header.pack(fill="x", padx=15, pady=(15, 5))
    ctk.CTkLabel(out_header, text="Output", font=FONTS["heading"], text_color=COLORS["text"]).pack(side="left")

    def copy_output():
        val = output_box.get("1.0", "end").strip()
        if val:
            frame.clipboard_clear()
            frame.clipboard_append(val)

    ctk.CTkButton(out_header, text="Copy", width=60, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_output).pack(side="right")

    output_box = ctk.CTkTextbox(output_card, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"])
    output_box.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    output_box.configure(state="disabled")

    # Status bar
    status_label = ctk.CTkLabel(content, text="Ready", font=FONTS["mono_small"], text_color=COLORS["text_dim"], anchor="w")
    status_label.pack(fill="x", pady=(4, 0))
